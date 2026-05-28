# Review map

## Claim

The package claims the asymptotic upper bound

$$
C_{42}\le 0.6906538.
$$

The proof is asymptotic and does not provide an explicit finite threshold.

## Constants

The construction uses

$$
\tau=\frac{36988243}{10^8},
\qquad
\alpha=\frac{61927309+57623741i}{10^8},
\qquad
\eta=\frac{59839764-34485185i}{10^8},
$$

$$
s=1-\alpha=\frac{38072691-57623741i}{10^8},
\qquad
w=\eta-s=\frac{21767073+23138556i}{10^8},
$$

and

$$
C=\frac{3453269}{5000000}=0.6906538.
$$

## Computational certificate

The exact verifier proves

$$
|1-\alpha|<C,\qquad |\eta|<C,\qquad |Y|<CD,\qquad C<0.69368.
$$

It does this using exact integer arithmetic and outward-rounded rational
interval arithmetic. The exact verifier is

```text
scripts/verify_42a_certificate.py
```

and a transcript is recorded in

```text
certificate/verify_42a_certificate.output.txt
```

## Mathematical reduction

The writeup proves that the finite construction has prescribed power sums
$S_k$, that $b_n=0$, and that the limiting inequality $|Y|<CD$ implies

$$
|Y_n|\le C\sum_{m\in F_n}|P_m|
$$

for all sufficiently large $n$.

## Known limitations

No explicit threshold $N$ is provided. The proof is asymptotic. The exact
verifier checks the limiting numerical certificate, not the full asymptotic
proof in a formal proof assistant.

An independent ball-arithmetic verifier is not included yet. A useful future
check would recompute $K$, $D$, $A_1$, and $A_2$ using independent interval or
ball arithmetic, preferably without sharing the custom rational interval code.

## Suggested reviewer checks

1. Verify the generating-function derivation of $b_n$.
2. Check the sign and factor $2$ in the double-sum limit.
3. Check the endpoint and floor-error arguments.
4. Run the exact verifier.
5. Optionally add or run an independent ball-arithmetic verifier.
