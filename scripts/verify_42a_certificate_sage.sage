# Optional exported-certificate consistency checker.
#
# This is not the primary certificate and does not independently recompute the
# interval enclosures. It is intended for reviewers who use Sage and want a
# separate check that the exported JSON certificate and SHA256 file are
# internally consistent and imply the final strict inequality.

from __future__ import annotations

import hashlib
import json
from fractions import Fraction
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
CERTIFICATE_DIR = ROOT / "certificate"
JSON_PATH = CERTIFICATE_DIR / "turan42_certificate.json"
SHA256_PATH = CERTIFICATE_DIR / "turan42_certificate.sha256"


def check(condition, message):
    if not condition:
        raise RuntimeError(message)


def sha256_file(path):
    h = hashlib.sha256()
    with path.open("rb") as f:
        for chunk in iter(lambda: f.read(1024 * 1024), b""):
            h.update(chunk)
    return h.hexdigest()


def q(s):
    return Fraction(s)


def main():
    expected_hashes = {}
    for line in SHA256_PATH.read_text(encoding="utf-8").splitlines():
        digest, name = line.split("  ", 1)
        expected_hashes[name] = digest

    for name, digest in expected_hashes.items():
        check(
            sha256_file(CERTIFICATE_DIR / name) == digest,
            "SHA256 mismatch for {}".format(name),
        )

    data = json.loads(JSON_PATH.read_text(encoding="utf-8"))

    c = q(data["bound"])
    previous = q(data["previous_public_bound"])
    s_margin = q(data["verified_claims"]["radius_s_margin"])
    eta_margin = q(data["verified_claims"]["radius_eta_margin"])
    gap = q(data["verified_claims"]["main_gap"])
    y2_upper = q(data["bounds"]["Y_norm_square_upper"])
    c2d2_lower = q(data["bounds"]["C2D2_lower_bound"])

    check(s_margin > 0, "radius margin for |1-alpha| is not positive")
    check(eta_margin > 0, "radius margin for |eta| is not positive")
    check(gap == c2d2_lower - y2_upper, "main gap does not match exported bounds")
    check(gap > 0, "main gap is not positive")
    check(c < previous, "claimed bound is not below previous listed bound")
    check(data["limitations"]["finite_threshold_N"] is None, "finite threshold should be null")
    check(
        data["limitations"]["formalized_asymptotic_proof"] is False,
        "formalized_asymptotic_proof should be false",
    )

    y = data["enclosures"]["Y"]
    y2_from_corners = max(
        re * re + im * im
        for re in [q(y["re"][0]), q(y["re"][1])]
        for im in [q(y["im"][0]), q(y["im"][1])]
    )
    check(y2_from_corners == y2_upper, "Y norm-square upper bound is not the corner maximum")

    print("PASS optional Sage exported-certificate consistency check")


if __name__ == "__main__":
    main()
