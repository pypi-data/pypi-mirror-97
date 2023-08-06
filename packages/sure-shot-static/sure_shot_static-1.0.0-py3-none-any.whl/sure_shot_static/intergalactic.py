#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Cache-Control Header

    * https://www.w3.org/Protocols/rfc2616/rfc2616-sec14.html#sec14.9
    * https://developer.mozilla.org/en-US/docs/Web/HTTP/Headers/Cache-Control#revalidation_and_reloading

HEAD response

    * see https://docs.aws.amazon.com/AmazonS3/latest/API/RESTCommonResponseHeaders.html

"""
import os
import logging
import hashlib

import boto3
import botocore

logging.getLogger("botocore").setLevel(logging.WARNING)

DEFAULT_BUCKET = os.environ.get("STATIC_ASSETS_BUCKET", "time-to-get-ill")


def md5_sum(local_fn):
    """
    Return MD5 sum of file *local_fn*.
    """
    handle = open(local_fn, "rb")
    md5sum = hashlib.md5(handle.read()).hexdigest()
    handle.close()
    return md5sum


class TentativeUploader:
    def __init__(self, *args, **kwargs):
        self.log = logging.getLogger(__name__)
        self.cache_time = kwargs.get("cache_time", 3600 * 24 * 333)
        self.bucket = kwargs.get("bucket", DEFAULT_BUCKET)
        self._session = boto3.session.Session()

    @property
    def base_url(self):
        return "https://{bucket}.s3.{region_name}.amazonaws.com".format(
            bucket=self.bucket, region_name=self._session.region_name
        )

    @property
    def base_arn(self):
        return "arn:aws:s3:::{bucket}".format(bucket=self.bucket)

    def push(self, rel_path, abs_path, mime_type, **kwargs):
        need_push = True
        head_response = None
        cache_time = kwargs.get("cache_time", self.cache_time)
        client = boto3.client("s3")
        cache_control = ["public", "max-age={:d}".format(cache_time)]
        if kwargs.get("immutable", True):
            cache_control.append("immutable")

        upload_args = {
            "Key": rel_path,
            "ACL": "public-read",
            "Bucket": self.bucket,
            "CacheControl": ", ".join(cache_control),
            "ContentType": mime_type,
        }

        if kwargs.get("content_encoding"):
            upload_args["ContentEncoding"] = kwargs.get("content_encoding")

        self.log.debug(" ? Check Your Head ...")

        try:
            head_response = client.head_object(Bucket=self.bucket, Key=rel_path)
            # self.log.info(head_response)
        except botocore.exceptions.ClientError as bex:
            if bex.response["ResponseMetadata"]["HTTPStatusCode"] == 404:
                pass
            elif bex.response["ResponseMetadata"]["HTTPStatusCode"] == 403:
                self.log.error(
                    "You Gotta Fight For Your Right To ... {what:8} {rel_path!r}: {Code} {Message}".format(
                        what="get head", rel_path=rel_path, **bex.response["Error"]
                    )
                )
            else:
                raise

        if head_response:
            need_push = False

            try:
                md5_digest = md5_sum(abs_path)
                key = "ETag"
                self.log.debug(
                    "   {:20}: me={!r} -- them={!r}".format(
                        key, md5_digest, head_response.get(key)
                    )
                )

                if md5_digest not in head_response["ETag"]:
                    need_push = True
            except Exception as exc:
                self.log.warning("MD5 sum/ETag comparison failed: {!s}".format(exc))

            if need_push is False:
                same_size = os.path.getsize(abs_path) == head_response["ContentLength"]
                if not same_size:
                    self.log.debug("   Size differs ...")
                    need_push = True

            if need_push is False:
                for key in ("CacheControl", "ContentType"):
                    self.log.debug(
                        "   {:20}: me={!r} -- them={!r}".format(
                            key, upload_args.get(key), head_response.get(key)
                        )
                    )

                    if upload_args.get(key) != head_response.get(key):
                        need_push = True
                        break

        if not need_push:
            self.log.info("   No update needed ...")
            return True

        succeeded = False
        with open(abs_path, "rb") as src:
            try:
                client.put_object(Body=src, **upload_args)
                succeeded = True
            except botocore.exceptions.ClientError as bex:
                if bex.response["ResponseMetadata"]["HTTPStatusCode"] == 403:
                    self.log.error(
                        "You Gotta Fight For Your Right To ... {what:8} {rel_path!r}: {Code} {Message}".format(
                            what="put", rel_path=rel_path, **bex.response["Error"]
                        )
                    )
                else:
                    raise

        if succeeded:
            self.log.info(" = {:s}/{:s}".format(self.base_url, rel_path))

        return succeeded
