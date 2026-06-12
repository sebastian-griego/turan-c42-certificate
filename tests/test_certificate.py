from __future__ import annotations

import hashlib
import json
import sys
import tempfile
import unittest
from fractions import Fraction
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))

import export_42a_certificate
import audit_42a_certificate_package
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

    def test_package_audit_passes_for_committed_certificate(self) -> None:
        audit = audit_42a_certificate_package.build_audit(ROOT / "certificate")

        self.assertEqual(audit["summary"]["status"], "pass")
        self.assertEqual(audit["summary"]["failures"], 0)
        self.assertEqual(audit["metrics"]["bound"], "3453269/5000000")
        self.assertGreater(Fraction(audit["metrics"]["main_gap"]), 0)

    def test_package_audit_detects_tampered_hash_manifest(self) -> None:
        with tempfile.TemporaryDirectory() as tmpdir:
            certificate_dir = Path(tmpdir) / "certificate"
            certificate_dir.mkdir()
            for name in [
                "turan42_certificate.json",
                "verify_42a_certificate.output.txt",
                "turan42_certificate.sha256",
            ]:
                (certificate_dir / name).write_bytes((ROOT / "certificate" / name).read_bytes())
            sha_path = certificate_dir / "turan42_certificate.sha256"
            sha_path.write_text(
                sha_path.read_text(encoding="utf-8").replace("a", "b", 1),
                encoding="utf-8",
            )

            audit = audit_42a_certificate_package.build_audit(certificate_dir)

            hash_check = next(row for row in audit["checks"] if row["check_id"] == "sha256_manifest")
            self.assertEqual(hash_check["status"], "fail")

    def test_package_audit_detects_inconsistent_main_gap(self) -> None:
        with tempfile.TemporaryDirectory() as tmpdir:
            certificate_dir = Path(tmpdir) / "certificate"
            certificate_dir.mkdir()
            for name in [
                "turan42_certificate.json",
                "verify_42a_certificate.output.txt",
                "turan42_certificate.sha256",
            ]:
                (certificate_dir / name).write_bytes((ROOT / "certificate" / name).read_bytes())
            json_path = certificate_dir / "turan42_certificate.json"
            data = json.loads(json_path.read_text(encoding="utf-8"))
            data["bounds"]["comparison_gap"] = "0"
            json_path.write_text(json.dumps(data, indent=2, sort_keys=True) + "\n", encoding="utf-8")

            audit = audit_42a_certificate_package.build_audit(certificate_dir)

            exact_check = next(row for row in audit["checks"] if row["check_id"] == "exact_inequality_margins")
            self.assertEqual(exact_check["status"], "fail")


if __name__ == "__main__":
    unittest.main()
