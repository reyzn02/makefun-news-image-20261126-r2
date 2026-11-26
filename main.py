#!/usr/bin/env python3
"""Entry point for the make.fun news-image-20261126 entry.

Copies the pre-drawn front page (entry.png, in this repository) to the
output directory the grader provides, then proves the copy is intact:
PNG magic bytes first, then a byte-for-byte SHA-256 match against the
source. Any mismatch or missing file fails loudly (exit 1) instead of
leaving a partial entry behind.

Standard library only. No network, no environment secrets, no writes
outside the output directory.
"""
import hashlib
import os
import sys

SOURCE_NAME = "entry.png"
OUTPUT_NAME = "entry.png"
PNG_MAGIC = b"\x89PNG\r\n\x1a\n"


def sha256_of(path):
    digest = hashlib.sha256()
    with open(path, "rb") as handle:
        for chunk in iter(lambda: handle.read(65536), b""):
            digest.update(chunk)
    return digest.hexdigest()


def main():
    here = os.path.dirname(os.path.abspath(__file__))
    source = os.path.join(here, SOURCE_NAME)
    out_dir = os.environ.get("MAKEFUN_OUTPUT_DIR", "/output")
    target = os.path.join(out_dir, OUTPUT_NAME)

    if not os.path.isfile(source):
        print("error: %s not found in repository" % source, file=sys.stderr)
        return 1

    with open(source, "rb") as handle:
        data = handle.read()
    if data[:8] != PNG_MAGIC:
        print("error: %s is not a PNG (bad magic bytes)" % source,
              file=sys.stderr)
        return 1
    if len(data) > 1048576:
        print("error: %s is %d bytes, over the 1 MiB cap"
              % (source, len(data)), file=sys.stderr)
        return 1

    os.makedirs(out_dir, exist_ok=True)
    with open(target, "wb") as handle:
        handle.write(data)

    with open(target, "rb") as handle:
        copied = handle.read()
    if copied[:8] != PNG_MAGIC:
        print("error: copied file is not a PNG", file=sys.stderr)
        return 1
    if hashlib.sha256(copied).hexdigest() != hashlib.sha256(data).hexdigest():
        print("error: copied file differs from source (SHA-256 mismatch)",
              file=sys.stderr)
        return 1

    print("wrote %s (%d bytes, sha256 %s)"
          % (target, len(copied), hashlib.sha256(copied).hexdigest()))
    return 0


if __name__ == "__main__":
    sys.exit(main())
