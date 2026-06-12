from __future__ import annotations

import hashlib
import sys
import tempfile
import unittest
from fractions import Fraction
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))

import export_42a_certificate
import verify_42a_certificate


class CertificateSmokeTests(unittest.TestCase):
    def test_exact_verifier_returns_expected_claim_summary(self) -> None:
        result = verify_42a_certificate.run_verification(verbose=False)

        self.assertEqual(result["bound"], "3453269/5000000")
        self.assertEqual(result["previous_public_bound"], "69368/100000")
        self.assertEqual(
            result["verified_claims"]["final_bound"],
            "3453269/5000000 < 69368/100000",
        )
        self.assertGreater(Fraction(result["verified_claims"]["main_gap"]), 0)
        self.assertIsNone(result["limitations"]["finite_threshold_N"])
        self.assertFalse(result["limitations"]["formalized_asymptotic_proof"])

    def test_sha256_file_hashes_file_contents(self) -> None:
        with tempfile.TemporaryDirectory() as tmpdir:
            path = Path(tmpdir) / "sample.txt"
            payload = b"certificate smoke test\n"
            path.write_bytes(payload)

            self.assertEqual(
                export_42a_certificate.sha256_file(path),
                hashlib.sha256(payload).hexdigest(),
            )


if __name__ == "__main__":
    unittest.main()
