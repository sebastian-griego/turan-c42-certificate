# C42 Turan verification package

This is a local verification and writeup package for a proposed improved upper
bound for Turan's pure power sum constant `C_42`.

No pull request has been made from this package, and no changes have been made
to `teorth/optimizationproblems`.

## Claim

The proposed bound is

```text
limsup_{n -> infinity} R_n <= 0.6936763075 < 0.69368.
```

The current public bound being improved is `0.69368`.

## Files

- `notes/turan_42a_improved_upper_bound.md`: self-contained writeup.
- `scripts/verify_42a_certificate.py`: exact rational-interval verifier.
- `scripts/numeric_sanity_check.py`: high-precision numerical sanity check.
- `certificate/README.md`: certificate/disclosure note.

## Verification

Run the exact certificate:

```bash
python3 scripts/verify_42a_certificate.py
```

This script uses exact integer and rational arithmetic for all pass/fail
comparisons. Decimal arithmetic is used only for display.

Run the numerical sanity check:

```bash
python3 scripts/numeric_sanity_check.py
```

The mpmath script is only a sanity check and is not the certificate.
