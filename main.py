#!/usr/bin/env python3
"""news-image-20261126 (burn) — "The Day, Hour by Hour".

Writes the pre-rendered image entry.png (1024x1024) that sits next to
this script into $MAKEFUN_OUTPUT_DIR/entry.png (or /output/entry.png
when the variable is unset), then proves the written file is exactly
the expected image: same bytes, same SHA-256, same dimensions, same
size. Any mismatch aborts with a non-zero exit code.
The image is verified twice: the bundled source is checked before
anything is written, and the written file is checked again afterwards,
so neither a swapped source nor a truncated write can slip through.
Standard library only; the run is deterministic.
"""

import hashlib
import os
import struct
import sys

WANT_SHA256 = "11a4d67240629647d8f9cfd1495330177e11b66d2a1aa30b7964cff0e21404fa"
WANT_WIDTH = 1024
WANT_HEIGHT = 1024
WANT_BYTES = 142445


def die(reason):
    sys.stderr.write("FAIL: %s\n" % reason)
    sys.exit(1)


def read_png_size(blob):
    if blob[:8] != b"\x89PNG\r\n\x1a\n":
        die("bad PNG signature")
    if blob[12:16] != b"IHDR":
        die("missing IHDR chunk")
    return struct.unpack(">II", blob[16:24])


def check(blob, label):
    got_sha = hashlib.sha256(blob).hexdigest()
    if got_sha != WANT_SHA256:
        die("%s sha256 is %s, want %s" % (label, got_sha, WANT_SHA256))
    w, h = read_png_size(blob)
    if (w, h) != (WANT_WIDTH, WANT_HEIGHT):
        die("%s is %dx%d, want %dx%d" % (label, w, h, WANT_WIDTH, WANT_HEIGHT))
    if len(blob) != WANT_BYTES:
        die("%s is %d bytes, want %d" % (label, len(blob), WANT_BYTES))
    return w, h, got_sha


def run():
    base = os.path.dirname(os.path.abspath(__file__))
    src = os.path.join(base, "entry.png")
    target_dir = os.environ.get("MAKEFUN_OUTPUT_DIR", "/output")
    os.makedirs(target_dir, exist_ok=True)
    dst = os.path.join(target_dir, "entry.png")

    if not os.path.isfile(src):
        die("source image missing: %s" % src)
    with open(src, "rb") as f:
        payload = f.read()
    check(payload, "source")
    with open(dst, "wb") as f:
        f.write(payload)
    with open(dst, "rb") as f:
        out = f.read()

    if out != payload:
        die("output bytes differ from source bytes")
    w, h, sha = check(out, "output")
    print("wrote %s (%dx%d, %d bytes, sha256 %s)" % (dst, w, h, len(out), sha))


if __name__ == "__main__":
    run()
