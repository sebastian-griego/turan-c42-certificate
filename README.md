# C42 Turan verification package

This repository contains a verification package for a proposed improved
asymptotic upper bound for Turan's pure power sum constant `C_42`.

The claimed bound is

$$
C_{42}=\limsup_{n\to\infty} R_n \le 0.6906538.
$$

The currently listed upper bound on the optimization problems repository is
`0.69368`.

The proof is asymptotic. It does not claim an explicit finite threshold `N`
such that the displayed block construction works for every `n >= N`.

This is a standalone package; it does not modify `teorth/optimizationproblems`.

## Files

- `notes/turan_42a_improved_upper_bound.md`: self-contained writeup.
- `scripts/verify_42a_certificate.py`: exact rational-interval verifier.
- `scripts/numeric_sanity_check.py`: high-precision numerical sanity check.
- `certificate/verify_42a_certificate.output.txt`: verification transcript.
- `certificate/README.md`: certificate note.

## Verification

Run the exact certificate:

```bash
python3 scripts/verify_42a_certificate.py
```

This script uses exact integer arithmetic and outward-rounded rational interval
arithmetic for all pass/fail comparisons. Decimal arithmetic is used only for
display.

No third-party dependencies are required for `scripts/verify_42a_certificate.py`.

Expected output consists of `PASS` lines for:

- the radius checks `|1-alpha| < C` and `|eta| < C`,
- certified enclosures for `K`, `D`, `A1`, and `A2`,
- the main inequality `|Y| < C D`,
- the final comparison `0.6906538 < 0.69368`.

Run the numerical sanity check:

```bash
python3 scripts/numeric_sanity_check.py
```

The mpmath script is only a sanity check and is not the certificate.

The CI workflow runs both scripts on Python 3.12. The exact verifier runs
without dependencies; the sanity check installs `mpmath`.
