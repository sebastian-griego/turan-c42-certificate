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

## Verification Status

This package separates the claim into two parts.

1. The limiting numerical certificate is checked by
   `scripts/verify_42a_certificate.py` using exact integer arithmetic and
   outward-rounded rational interval arithmetic. This script verifies the
   radius checks, the interval enclosures for `K`, `D`, `A1`, and `A2`, and
   the strict inequality `|Y| < C D`.

2. The passage from the finite construction to the limiting certificate is
   proved in `notes/turan_42a_improved_upper_bound.md` using standard
   coefficient asymptotics and Riemann-sum limits.

The package does not provide an explicit finite threshold `N`. The result is
an asymptotic `limsup` upper bound.

The package is intended as a reviewable certificate, not as a peer-reviewed
publication.

## What The Verifier Does Not Prove By Itself

The exact verifier does not formalize the asymptotic argument. In particular,
the following steps are proved in the writeup rather than checked by the
script:

- the uniform asymptotic estimate for the coefficients `beta_l`,
- the Riemann-sum limits for the one-block and two-block sums,
- the harmlessness of the floor in `A_n = floor(tau n)`,
- the Newton identity step converting the prescribed power sums into roots,
- the final-block convex combination argument.

## Files

- `notes/turan_42a_improved_upper_bound.md`: self-contained writeup.
- `REVIEW.md`: claim map and suggested reviewer checklist.
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

The CI workflow also runs the exact verifier with optimized Python:

```bash
python3 -O scripts/verify_42a_certificate.py
```

Run the numerical sanity check:

```bash
python3 scripts/numeric_sanity_check.py
```

The mpmath script is only a sanity check and is not the certificate.

The CI workflow runs both scripts on Python 3.11 and 3.12. The exact verifier
runs without dependencies; the sanity check installs `mpmath`.

## Slack Summary

| Quantity | Certified or numerical value |
| --- | --- |
| Claimed bound `C` | `0.6906538` |
| Numerical `|Y|/D` | approximately `0.690653695151631` |
| Numerical slack `C - |Y|/D` | approximately `1.05e-7` |
| Certified comparison | `|Y|^2 < C^2 D^2` |
| Explicit finite threshold `N` | not provided |
