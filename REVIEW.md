# Review map

## Claim

This package proposes the asymptotic upper bound

$$
C_{42}\le 0.6906538.
$$

The proof is asymptotic and does not supply an explicit finite threshold.

## Machine-checked limiting certificate

The exact verifier checks

$$
|1-\alpha|<C,
\qquad
|\eta|<C,
\qquad
|Y|<CD,
\qquad
C<0.69368.
$$

The main inequality is checked as

$$
|Y|^2<C^2D^2
$$

using exact rational interval arithmetic.

## Prose mathematical reduction

The following steps are proved in the note rather than formalized by the
verifier:

1. coefficient asymptotic for $\beta_l=(\alpha)_l/l!$,
2. Riemann-sum limits for $K$, $D$, $A_1$, and $A_2$,
3. endpoint truncation near $l=0$,
4. harmlessness of $A_n=\lfloor\tau n\rfloor$,
5. generating-function derivation of $b_n=0$,
6. Newton identity step producing prescribed power sums,
7. final-block convex combination argument.

## Suggested reviewer checks

- Check the sign convention in the generating function.
- Check the factor $2$ in the double-sum limit defining $A_2$.
- Check the endpoint and floor-error estimates.
- Run the exact verifier.
- Regenerate the certificate and check that there is no diff.
- Optionally run the Sage exported-certificate consistency checker.

## Known limitations

- No explicit finite $N$ is supplied.
- The proof is asymptotic.
- The exact verifier checks the limiting numerical certificate, not a
  proof-assistant formalization of the asymptotic reduction.
