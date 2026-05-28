#!/usr/bin/env python3
"""Deterministically export the C_42 certificate artifacts."""

from __future__ import annotations

import contextlib
import hashlib
import io
import json
from pathlib import Path

import verify_42a_certificate


ROOT = Path(__file__).resolve().parents[1]
CERTIFICATE_DIR = ROOT / "certificate"
TRANSCRIPT_PATH = CERTIFICATE_DIR / "verify_42a_certificate.output.txt"
JSON_PATH = CERTIFICATE_DIR / "turan42_certificate.json"
SHA256_PATH = CERTIFICATE_DIR / "turan42_certificate.sha256"


def sha256_file(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as f:
        for chunk in iter(lambda: f.read(1024 * 1024), b""):
            h.update(chunk)
    return h.hexdigest()


def write_text(path: Path, text: str) -> None:
    path.write_text(text, encoding="utf-8", newline="\n")


def main() -> None:
    CERTIFICATE_DIR.mkdir(parents=True, exist_ok=True)

    transcript_buffer = io.StringIO()
    with contextlib.redirect_stdout(transcript_buffer):
        result = verify_42a_certificate.run_verification(verbose=True)

    transcript = transcript_buffer.getvalue()
    if not transcript.endswith("\n"):
        transcript += "\n"

    write_text(TRANSCRIPT_PATH, transcript)
    write_text(JSON_PATH, json.dumps(result, indent=2, sort_keys=True) + "\n")

    hashes = {
        TRANSCRIPT_PATH.name: sha256_file(TRANSCRIPT_PATH),
        JSON_PATH.name: sha256_file(JSON_PATH),
    }
    sha_lines = [f"{digest}  {name}" for name, digest in sorted(hashes.items())]
    write_text(SHA256_PATH, "\n".join(sha_lines) + "\n")

    for name, digest in sorted(hashes.items()):
        print(f"{digest}  certificate/{name}")
    print(f"{sha256_file(SHA256_PATH)}  certificate/{SHA256_PATH.name}")


if __name__ == "__main__":
    main()
