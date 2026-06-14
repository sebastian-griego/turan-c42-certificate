#!/usr/bin/env python3
"""Audit the exported C_42 certificate package.

This script intentionally audits the committed package artifacts rather than
importing the verifier. It checks that the exported JSON, transcript, and hash
metadata are internally consistent and that the exact rational inequalities
advertised by the package are positive.
"""

from __future__ import annotations

import argparse
import csv
import hashlib
import json
from fractions import Fraction
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
CERTIFICATE_DIR = ROOT / "certificate"
JSON_NAME = "turan42_certificate.json"
TRANSCRIPT_NAME = "verify_42a_certificate.output.txt"
SHA256_NAME = "turan42_certificate.sha256"
AUDIT_JSON_NAME = "turan42_certificate.audit.json"
AUDIT_MD_NAME = "turan42_certificate.audit.md"

REQUIRED_TOP_LEVEL_KEYS = {
    "alpha",
    "bound",
    "bounds",
    "description",
    "enclosures",
    "eta",
    "limitations",
    "previous_public_bound",
    "rounding_denominator",
    "s",
    "series_terms",
    "tau",
    "verified_claims",
    "w",
}


def sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as f:
        for chunk in iter(lambda: f.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def parse_fraction(value: Any, label: str) -> Fraction:
    if not isinstance(value, str):
        raise ValueError(f"{label} is not a fraction string")
    try:
        return Fraction(value)
    except ValueError as exc:
        raise ValueError(f"{label} is not a valid fraction: {value!r}") from exc


def parse_interval(value: Any, label: str) -> tuple[Fraction, Fraction]:
    if not isinstance(value, list) or len(value) != 2:
        raise ValueError(f"{label} must be a two-item fraction interval")
    lo = parse_fraction(value[0], f"{label}[0]")
    hi = parse_fraction(value[1], f"{label}[1]")
    if lo > hi:
        raise ValueError(f"{label} has lo > hi")
    return lo, hi


def parse_complex_interval(value: Any, label: str) -> dict[str, tuple[Fraction, Fraction]]:
    if not isinstance(value, dict) or "re" not in value or "im" not in value:
        raise ValueError(f"{label} must contain re and im intervals")
    return {
        "re": parse_interval(value["re"], f"{label}.re"),
        "im": parse_interval(value["im"], f"{label}.im"),
    }


def compact_json(value: object) -> str:
    return json.dumps(value, sort_keys=True)


def check_row(
    check_id: str,
    area: str,
    evidence: str,
    problems: list[str],
    required_action: str,
) -> dict[str, str]:
    return {
        "check_id": check_id,
        "area": area,
        "status": "fail" if problems else "pass",
        "evidence": evidence,
        "problems": compact_json(problems[:12]),
        "required_action": required_action,
    }


def read_sha256_manifest(path: Path) -> dict[str, str]:
    hashes: dict[str, str] = {}
    for line_no, line in enumerate(path.read_text(encoding="utf-8").splitlines(), start=1):
        if not line.strip():
            continue
        parts = line.split()
        if len(parts) != 2:
            raise ValueError(f"{path.name}:{line_no}: expected '<sha256>  <filename>'")
        digest, name = parts
        if len(digest) != 64 or any(ch not in "0123456789abcdef" for ch in digest):
            raise ValueError(f"{path.name}:{line_no}: invalid sha256 digest")
        hashes[name] = digest
    return hashes


def norm_square_upper(z: dict[str, tuple[Fraction, Fraction]]) -> Fraction:
    re_lo, re_hi = z["re"]
    im_lo, im_hi = z["im"]
    return max(re * re + im * im for re in (re_lo, re_hi) for im in (im_lo, im_hi))


def decimal_string(value: Fraction, places: int = 18) -> str:
    scaled = value.numerator * (10**places) // value.denominator
    whole, frac = divmod(scaled, 10**places)
    return f"{whole}.{frac:0{places}d}"


def audit_schema(data: dict[str, Any]) -> tuple[dict[str, Any], list[str]]:
    problems: list[str] = []
    missing = sorted(REQUIRED_TOP_LEVEL_KEYS - set(data))
    extra = sorted(set(data) - REQUIRED_TOP_LEVEL_KEYS)
    if missing:
        problems.append(f"missing top-level keys: {missing}")
    if extra:
        problems.append(f"unexpected top-level keys: {extra}")

    derived: dict[str, Any] = {}
    try:
        derived["bound"] = parse_fraction(data.get("bound"), "bound")
        derived["previous_public_bound"] = parse_fraction(data.get("previous_public_bound"), "previous_public_bound")
        derived["rounding_denominator"] = parse_fraction(data.get("rounding_denominator"), "rounding_denominator")
        claims = data.get("verified_claims", {})
        bounds = data.get("bounds", {})
        enclosures = data.get("enclosures", {})
        derived["radius_s_margin"] = parse_fraction(claims.get("radius_s_margin"), "verified_claims.radius_s_margin")
        derived["radius_eta_margin"] = parse_fraction(claims.get("radius_eta_margin"), "verified_claims.radius_eta_margin")
        derived["main_gap"] = parse_fraction(claims.get("main_gap"), "verified_claims.main_gap")
        derived["comparison_gap"] = parse_fraction(bounds.get("comparison_gap"), "bounds.comparison_gap")
        derived["y_norm_square_upper"] = parse_fraction(bounds.get("Y_norm_square_upper"), "bounds.Y_norm_square_upper")
        derived["c2d2_lower_bound"] = parse_fraction(bounds.get("C2D2_lower_bound"), "bounds.C2D2_lower_bound")
        derived["d_lower"] = parse_fraction(enclosures.get("D_lower"), "enclosures.D_lower")
        derived["y_interval"] = parse_complex_interval(enclosures.get("Y"), "enclosures.Y")
    except (TypeError, ValueError) as exc:
        problems.append(str(exc))
    return derived, problems


def audit_hash_manifest(certificate_dir: Path) -> list[str]:
    sha_path = certificate_dir / SHA256_NAME
    problems: list[str] = []
    try:
        manifest = read_sha256_manifest(sha_path)
    except (OSError, ValueError) as exc:
        return [str(exc)]

    expected_names = {JSON_NAME, TRANSCRIPT_NAME}
    missing = sorted(expected_names - set(manifest))
    extra = sorted(set(manifest) - expected_names)
    if missing:
        problems.append(f"sha256 manifest missing entries: {missing}")
    if extra:
        problems.append(f"sha256 manifest has unexpected entries: {extra}")
    for name in sorted(expected_names & set(manifest)):
        actual = sha256_file(certificate_dir / name)
        if manifest[name] != actual:
            problems.append(f"{name} hash mismatch: manifest={manifest[name]} actual={actual}")
    return problems


def audit_exact_claims(data: dict[str, Any], derived: dict[str, Any]) -> tuple[dict[str, str], list[str]]:
    problems: list[str] = []
    metrics: dict[str, str] = {}
    try:
        bound = derived["bound"]
        previous = derived["previous_public_bound"]
        radius_s = derived["radius_s_margin"]
        radius_eta = derived["radius_eta_margin"]
        main_gap = derived["main_gap"]
        comparison_gap = derived["comparison_gap"]
        y2_upper = derived["y_norm_square_upper"]
        lower = derived["c2d2_lower_bound"]
        d_lower = derived["d_lower"]
        y_interval = derived["y_interval"]
    except KeyError:
        return metrics, ["schema parsing failed; exact claims were not audited"]

    if not bound < previous:
        problems.append("bound is not below previous public bound")
    if data.get("verified_claims", {}).get("final_bound") != f"{data.get('bound')} < {data.get('previous_public_bound')}":
        problems.append("verified_claims.final_bound does not match bound strings")
    if radius_s <= 0:
        problems.append("radius_s_margin is not positive")
    if radius_eta <= 0:
        problems.append("radius_eta_margin is not positive")
    if main_gap <= 0:
        problems.append("main_gap is not positive")
    if comparison_gap != main_gap:
        problems.append("bounds.comparison_gap does not equal verified_claims.main_gap")
    if lower - y2_upper != main_gap:
        problems.append("C2D2_lower_bound - Y_norm_square_upper does not equal main_gap")
    if lower != bound * bound * d_lower * d_lower:
        problems.append("C2D2_lower_bound is not bound^2 * D_lower^2")
    y_corner_upper = norm_square_upper(y_interval)
    if y2_upper != y_corner_upper:
        problems.append("Y_norm_square_upper does not match the Y interval corner maximum")

    metrics = {
        "bound": str(data.get("bound")),
        "previous_public_bound": str(data.get("previous_public_bound")),
        "public_bound_delta": str(previous - bound),
        "radius_s_margin": str(radius_s),
        "radius_eta_margin": str(radius_eta),
        "main_gap": str(main_gap),
        "main_gap_decimal_floor": decimal_string(main_gap, 18),
    }
    return metrics, problems


def audit_limitations(data: dict[str, Any]) -> list[str]:
    limitations = data.get("limitations", {})
    if not isinstance(limitations, dict):
        return ["limitations must be an object"]
    problems: list[str] = []
    if limitations.get("finite_threshold_N") is not None:
        problems.append("finite_threshold_N must remain null unless an explicit finite threshold is proved")
    if limitations.get("formalized_asymptotic_proof") is not False:
        problems.append("formalized_asymptotic_proof must remain false unless the asymptotic proof is formalized")
    return problems


def audit_transcript(certificate_dir: Path, data: dict[str, Any]) -> list[str]:
    try:
        transcript = (certificate_dir / TRANSCRIPT_NAME).read_text(encoding="utf-8")
    except OSError as exc:
        return [str(exc)]
    claims = data.get("verified_claims", {})
    required_snippets = [
        f"PASS |1-alpha| < C: exact margin = {claims.get('radius_s_margin')}",
        f"PASS |eta| < C: exact margin = {claims.get('radius_eta_margin')}",
        f"exact rational = {claims.get('main_gap')}",
        "PASS final certified bound C = 0.6906538 < 0.69368",
    ]
    return [f"transcript missing snippet: {snippet}" for snippet in required_snippets if snippet not in transcript]


def build_audit(certificate_dir: Path = CERTIFICATE_DIR) -> dict[str, Any]:
    json_path = certificate_dir / JSON_NAME
    data = json.loads(json_path.read_text(encoding="utf-8"))
    derived, schema_problems = audit_schema(data)
    metrics, exact_problems = audit_exact_claims(data, derived)
    rows = [
        check_row(
            "schema_and_required_fields",
            "json_certificate",
            f"top_level_keys={len(data)}; required_keys={len(REQUIRED_TOP_LEVEL_KEYS)}",
            schema_problems,
            "Regenerate the certificate JSON and keep the exported schema stable for reviewers.",
        ),
        check_row(
            "sha256_manifest",
            "package_integrity",
            f"manifest={SHA256_NAME}; expected_entries={JSON_NAME},{TRANSCRIPT_NAME}",
            audit_hash_manifest(certificate_dir),
            "Regenerate certificate hashes with scripts/export_42a_certificate.py after certificate changes.",
        ),
        check_row(
            "exact_inequality_margins",
            "rational_arithmetic",
            (
                f"bound_delta={metrics.get('public_bound_delta', 'unavailable')}; "
                f"main_gap_decimal_floor={metrics.get('main_gap_decimal_floor', 'unavailable')}"
            ),
            exact_problems,
            "Do not advertise the certificate unless all exact rational margins are positive and internally consistent.",
        ),
        check_row(
            "limitation_disclosure",
            "claim_boundary",
            compact_json(data.get("limitations", {})),
            audit_limitations(data),
            "Keep the asymptotic and no-finite-threshold limitations explicit until stronger proof artifacts exist.",
        ),
        check_row(
            "transcript_consistency",
            "review_transcript",
            f"transcript={TRANSCRIPT_NAME}",
            audit_transcript(certificate_dir, data),
            "Regenerate the transcript when the verifier output or certified margins change.",
        ),
    ]
    failures = sum(1 for row in rows if row["status"] == "fail")
    return {
        "schema_version": 1,
        "certificate": JSON_NAME,
        "checks": rows,
        "summary": {
            "check_count": len(rows),
            "failures": failures,
            "status": "fail" if failures else "pass",
        },
        "metrics": metrics,
    }


def write_json(path: Path, data: dict[str, Any]) -> None:
    path.write_text(json.dumps(data, indent=2, sort_keys=True) + "\n", encoding="utf-8", newline="\n")


def escape_table(value: str) -> str:
    return value.replace("|", "/").replace("\n", " ")


def write_markdown(path: Path, audit: dict[str, Any]) -> None:
    rows = audit["checks"]
    metrics = audit.get("metrics", {})
    lines = [
        "# C_42 Certificate Package Audit",
        "",
        "This generated audit checks the exported certificate package without importing the verifier. It validates hash metadata, exact rational claim arithmetic, transcript consistency, and explicit claim-boundary limitations.",
        "",
        "## Summary",
        "",
        f"- status: `{audit['summary']['status']}`",
        f"- checks: `{audit['summary']['check_count']}`",
        f"- failures: `{audit['summary']['failures']}`",
        f"- bound: `{metrics.get('bound', 'unavailable')}`",
        f"- previous public bound: `{metrics.get('previous_public_bound', 'unavailable')}`",
        f"- public bound delta: `{metrics.get('public_bound_delta', 'unavailable')}`",
        f"- main comparison gap: `{metrics.get('main_gap', 'unavailable')}`",
        "",
        "## Checks",
        "",
        "| check | area | status | evidence | problems | required action |",
        "| --- | --- | --- | --- | --- | --- |",
    ]
    for row in rows:
        lines.append(
            f"| `{row['check_id']}` | {row['area']} | {row['status']} | "
            f"{escape_table(row['evidence'])} | `{escape_table(row['problems'])}` | "
            f"{escape_table(row['required_action'])} |"
        )
    lines.extend([
        "",
        "## Scope",
        "",
        "This audit proves package consistency for the exported limiting certificate. It does not formalize the asymptotic reduction, supply an explicit finite threshold `N`, or replace independent mathematical review of the note.",
        "",
    ])
    path.write_text("\n".join(lines), encoding="utf-8", newline="\n")


def write_csv(path: Path, audit: dict[str, Any]) -> None:
    fields = ["check_id", "area", "status", "evidence", "problems", "required_action"]
    with path.open("w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=fields)
        writer.writeheader()
        writer.writerows(audit["checks"])


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--certificate-dir", type=Path, default=CERTIFICATE_DIR)
    parser.add_argument("--json-out", type=Path, default=CERTIFICATE_DIR / AUDIT_JSON_NAME)
    parser.add_argument("--markdown-out", type=Path, default=CERTIFICATE_DIR / AUDIT_MD_NAME)
    parser.add_argument("--csv-out", type=Path, default=None)
    args = parser.parse_args()

    audit = build_audit(args.certificate_dir)
    write_json(args.json_out, audit)
    write_markdown(args.markdown_out, audit)
    if args.csv_out is not None:
        write_csv(args.csv_out, audit)
    failures = audit["summary"]["failures"]
    print(
        f"wrote {args.json_out.relative_to(ROOT)} and {args.markdown_out.relative_to(ROOT)}; "
        f"failures={failures}"
    )
    return 1 if failures else 0


if __name__ == "__main__":
    raise SystemExit(main())
