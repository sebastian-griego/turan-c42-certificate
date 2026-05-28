# Certificate artifacts

This directory contains exported artifacts for the proposed asymptotic
certificate

```text
C_42 <= 0.6906538.
```

The certificate package consists of:

- the proof note: `../notes/turan_42a_improved_upper_bound.md`,
- the exact verifier: `../scripts/verify_42a_certificate.py`,
- the exported JSON certificate: `turan42_certificate.json`,
- the verifier transcript: `verify_42a_certificate.output.txt`,
- the SHA256 metadata: `turan42_certificate.sha256`.

The exact verifier checks the limiting numerical certificate using exact
integer arithmetic and outward-rounded rational interval arithmetic. The
asymptotic reduction is in the proof note.

No explicit finite threshold `N` is provided.

AI assistance was used to help format the writeup and prepare verification
scripts. The mathematical claim, references, constants, and computations should
be independently reviewed before any public submission.
