#!/usr/bin/env python3
"""news-image-20261126 (burn) — "The Day, Hour by Hour".

Reproduces the entry image byte-for-byte: the image is shipped in this
repository as entry.png and this program copies it to the grader's output
directory, verifying its hash, dimensions and size first — and then
re-verifying the file it actually wrote, so a partial or corrupt copy
can never pass silently.

Standard library only. No network, no clock, no randomness — running it
twice produces a byte-identical file.
"""

import hashlib
import os
import shutil
import struct
import sys

EXPECTED_SHA256 = "11a4d67240629647d8f9cfd1495330177e11b66d2a1aa30b7964cff0e21404fa"
EXPECTED_WIDTH = 1024
EXPECTED_HEIGHT = 1024
MAX_BYTES = 1024 * 1024


def sha256_file(path):
    digest = hashlib.sha256()
    with open(path, "rb") as handle:
        for chunk in iter(lambda: handle.read(65536), b""):
            digest.update(chunk)
    return digest.hexdigest()


def png_dimensions(path):
    with open(path, "rb") as handle:
        header = handle.read(33)
    if len(header) < 33 or header[:8] != b"\x89PNG\r\n\x1a\n":
        return None
    if header[12:16] != b"IHDR":
        return None
    width, height = struct.unpack(">II", header[16:24])
    return width, height


def check_image(path, label):
    if not os.path.isfile(path):
        print("%s missing: %s" % (label, path), file=sys.stderr)
        return False, 0, ""
    size = os.path.getsize(path)
    if size > MAX_BYTES:
        print("%s too large: %d bytes" % (label, size), file=sys.stderr)
        return False, size, ""
    dims = png_dimensions(path)
    if dims != (EXPECTED_WIDTH, EXPECTED_HEIGHT):
        print("%s wrong dimensions: %r" % (label, dims), file=sys.stderr)
        return False, size, ""
    digest = sha256_file(path)
    if digest != EXPECTED_SHA256:
        print("%s hash mismatch: %s" % (label, digest), file=sys.stderr)
        return False, size, digest
    return True, size, digest


def main():
    here = os.path.dirname(os.path.abspath(__file__))
    source = os.path.join(here, "entry.png")
    out_dir = os.environ.get("MAKEFUN_OUTPUT_DIR", "/output")
    target = os.path.join(out_dir, "entry.png")

    ok, size, source_hash = check_image(source, "source entry.png")
    if not ok:
        return 1

    os.makedirs(out_dir, exist_ok=True)
    shutil.copyfile(source, target)

    # Verify the file actually written, not just the source we read.
    ok, out_size, out_hash = check_image(target, "output entry.png")
    if not ok:
        return 1
    if out_size != size or out_hash != source_hash:
        print("output differs from source", file=sys.stderr)
        return 1

    print("wrote %s (%d bytes, sha256 %s)"
          % (target, out_size, out_hash))
    return 0


if __name__ == "__main__":
    sys.exit(main())
