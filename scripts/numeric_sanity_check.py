#!/usr/bin/env python3
"""High-precision numerical sanity check for the C_42 certificate.

This script is not the certificate.  It uses mpmath to confirm the numerical
shape of the exact rational-interval verification.
"""

from __future__ import annotations

import mpmath as mp


def main() -> None:
    mp.mp.dps = 90

    alpha = mp.mpc(mp.mpf(567376361) / 10**9, mp.mpf(542239436) / 10**9)
    a = mp.mpf(567376361) / 10**9
    s = 1 - alpha
    c = mp.mpf(6936763075) / 10**10

    def i_of(A: mp.mpc | mp.mpf) -> mp.mpc:
        total = mp.mpc(0)
        r = 0
        while True:
            term = mp.power(2, -A - r) / (A + r)
            total += term
            if abs(term) < mp.mpf("1e-95"):
                break
            r += 1
        return total

    i_alpha = i_of(alpha)
    i_a = mp.re(i_of(a))
    ratio = abs(1 + s * i_alpha) / i_a

    print("I_alpha =")
    print(mp.nstr(mp.re(i_alpha), 80))
    print("-")
    print(mp.nstr(-mp.im(i_alpha), 80), "i")
    print()
    print("I_a =")
    print(mp.nstr(i_a, 80))
    print()
    print("ratio =")
    print(mp.nstr(ratio, 80))
    print()
    print("C - ratio =")
    print(mp.nstr(c - ratio, 30))


if __name__ == "__main__":
    main()
