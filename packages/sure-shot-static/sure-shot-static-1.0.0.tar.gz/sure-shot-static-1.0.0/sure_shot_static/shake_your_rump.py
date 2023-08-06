#!/usr/bin/env python
# -*- coding: utf-8 -*-
import os
import logging
import re

import magic
import brotli

from sure_shot_static.intergalactic import TentativeUploader


PATTERN_PORTIONS = r"(?P<trunk>.*?)\.(?P<ext>[^\.]*?)(\.(?P<compressed_ext>gz|br)|)$"
REGEX_PORTIONS = re.compile(PATTERN_PORTIONS)

root_abs = os.path.abspath("public")


log = logging.getLogger("s3ync")


def simple_brotli(source, target=None):
    """
    Helper method for brotli compression of a local file

    Args:
        source (str): source path
        target (str, optional): target path. Defaults to None.
    """
    if target is None:
        target = source + ".br"

    with open(source, "rb") as src, open(target, "wb") as tgt:
        tgt.write(brotli.compress(src.read()))


def sources(top_dog=None):
    if top_dog is None:
        top_dog = root_abs

    #  dirpath, dirnames, filenames
    for root, _, files in os.walk(top_dog):
        for filename in files:
            abs_path = os.path.normpath(os.path.join(root, filename))
            rel_path = os.path.relpath(abs_path, top_dog)
            yield (abs_path, rel_path)


def brotli_compressor(abs_path, rel_path, gdict):
    """
    Brotli compress a file if the compressed version is not yet created.

    Args:
        abs_path (str): uncompressed file
        rel_path (str): relative uncompressed file path
        gdict (dict): key/value pairs of file pattern matcher

    Returns:
        dict: extended key/value pairs of file pattern matcher
    """
    compressed = "{trunk}.{ext}.br".format(**gdict)
    gdict["compressed_ext"] = "br"

    if not os.path.isfile(compressed):
        simple_brotli(abs_path, compressed)
        assert os.path.isfile(compressed)

    log.debug(
        "{!s}: {:d} => {:d}".format(
            rel_path, os.path.getsize(abs_path), os.path.getsize(compressed)
        )
    )

    return gdict


# MIME type overrides
mime_override = dict(
    js="text/javascript",
    css="text/css",
    woff="font/woff",
    woff2="font/woff",
    ttf="font/ttf",
)

# encoding type override for compressed files
content_type = dict(br="br")

# file extensions that should be compressed
compressable = (
    "css",
    "js",
)

# required environment keys
required_env_keys = (
    "AWS_ACCESS_KEY_ID",
    "AWS_SECRET_ACCESS_KEY",
    "AWS_DEFAULT_REGION",
    "STATIC_ASSETS_BUCKET",
)
bucket = os.environ.get("STATIC_ASSETS_BUCKET", "time-to-get-ill")


def shake_your_rump():
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s %(levelname)-8s %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S",
    )

    cache_time = 3600 * 24 * 333

    for env_key in required_env_keys:
        if not os.environ.get(env_key):
            log.warning("Environment key {!r} is not defined ..".format(env_key))

    if not os.path.isdir(root_abs):
        log.error("{!r} needs to be existing ...".format(root_abs))
    assert os.path.isdir(root_abs)

    mr_t = TentativeUploader(bucket=bucket)

    log.info("-" * 100)
    log.info(
        "Trying to push contents of {!r} to {!s} ({!s})".format(
            root_abs, mr_t.base_arn, mr_t.base_url
        )
    )
    log.info("-" * 100)
    log.info("")

    seen = set()

    for abs_path, rel_path in sources():
        matcher = REGEX_PORTIONS.match(abs_path)
        ext = None

        if matcher:
            gdict = matcher.groupdict()
            ext = gdict.get("ext")

            if ext in compressable and not gdict.get("compressed_ext"):
                gdict = brotli_compressor(abs_path, rel_path, gdict)
                abs_path += ".{compressed_ext}".format(**gdict)
                rel_path += ".{compressed_ext}".format(**gdict)
        else:
            gdict = dict()

        if rel_path in seen:
            continue

        if ext in mime_override:
            mime_type = mime_override[ext]
        else:
            mime_type = magic.from_file(abs_path, mime=True)

        description = mime_type
        if gdict.get("compressed_ext"):
            description = "{:s} ({:s})".format(mime_type, gdict.get("compressed_ext"))
        log.info(" + {:60s} {:s}".format(rel_path, description))

        content_encoding = None
        if gdict.get("compressed_ext"):
            content_encoding = content_type[gdict.get("compressed_ext")]

        mr_t.push(
            rel_path=rel_path,
            abs_path=abs_path,
            mime_type=mime_type,
            content_encoding=content_encoding,
            cache_time=cache_time,
        )

        log.info("")
        seen.add(rel_path)
