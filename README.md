# An improved asymptotic certificate for Turan's pure power sum constant C_42

This repository contains a proposed asymptotic certificate for

```text
C_42 <= 0.6906538.
```

The previously listed upper bound is `0.69368`.

The proof is asymptotic. No explicit finite threshold `N` is provided. The
exact verifier checks the limiting numerical certificate; the asymptotic
reduction is proved in the note, not formalized by the verifier.

## Artifacts

- `notes/turan_42a_improved_upper_bound.md`: proof/writeup
- `scripts/verify_42a_certificate.py`: exact rational interval verifier
- `scripts/export_42a_certificate.py`: deterministic certificate export
- `certificate/`: exported certificate data, transcript, and metadata
- `scripts/numeric_sanity_check.py`: high-precision numerical sanity check
- `scripts/verify_42a_certificate_sage.sage`: optional exported-certificate consistency checker
- `REVIEW.md`: reviewer-facing claim map

## What The Exact Verifier Checks

`scripts/verify_42a_certificate.py` checks:

- the rational input constants,
- the radius inequalities `|1-alpha| < C` and `|eta| < C`,
- interval enclosures for `K`, `D`, `A1`, and `A2`,
- the limiting inequality `|Y| < C D`, checked as `|Y|^2 < C^2 D^2`,
- the comparison `0.6906538 < 0.69368`.

It uses exact integer arithmetic and outward-rounded rational interval
arithmetic for all pass/fail comparisons. Decimal arithmetic is used only for
display.

The verifier does not formalize the coefficient asymptotics, Riemann-sum
limits, endpoint truncation, floor-error estimates, generating-function
derivation, Newton identity step, or final-block convex combination argument.
Those steps are proved in the writeup.

## Run

Run the exact verifier:

```bash
python3 scripts/verify_42a_certificate.py
```

Regenerate the exported certificate files:

```bash
python3 scripts/export_42a_certificate.py
```

Run the numerical sanity check:

```bash
python3 scripts/numeric_sanity_check.py
```

The numerical sanity check requires `mpmath` and is not the certificate.

Optionally, with Sage installed:

```bash
sage scripts/verify_42a_certificate_sage.sage
```

This optional Sage script checks the exported certificate and hashes for
internal consistency. It does not independently recompute all interval
enclosures.

## Reproducibility

CI runs:

- the exact verifier,
- the exact verifier with optimized Python (`python3 -O`),
- the numerical sanity check,
- deterministic regeneration of `certificate/`,
- a `git diff --exit-code certificate` reproducibility check.

The exact verifier has no third-party dependencies.

## Disclosure

AI assistance was used for formatting, exposition, and preparation of
verification scripts. The mathematical claim, constants, references, and
computations are provided for independent review.

## References

- Constant page: https://teorth.github.io/optimizationproblems/constants/42a.html
- This repository: version/tag placeholder `v1.0.0`
