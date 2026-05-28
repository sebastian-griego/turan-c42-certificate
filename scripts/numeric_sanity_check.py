#!/usr/bin/env python3
"""High-precision numerical sanity check for the two-block C_42 certificate.

This script is not the certificate. It uses mpmath to confirm the numerical
shape of the exact rational-interval verification.
"""

from __future__ import annotations

import mpmath as mp


def main() -> None:
    mp.mp.dps = 90

    tau = mp.mpf(36988243) / 10**8
    alpha = mp.mpc(mp.mpf(61927309) / 10**8, mp.mpf(57623741) / 10**8)
    eta = mp.mpc(mp.mpf(59839764) / 10**8, -mp.mpf(34485185) / 10**8)
    c = mp.mpf(3453269) / 5000000

    s = 1 - alpha
    w = eta - s
    l_end = 1 - 2 * tau
    b_end = 1 - tau

    def i_of(A: mp.mpc | mp.mpf, x: mp.mpf) -> mp.mpc:
        total = mp.mpc(0)
        r = 0
        while True:
            term = mp.power(x, A + r) / (A + r)
            total += term
            if abs(term) < mp.mpf("1e-95"):
                break
            r += 1
        return total

    def a2_series() -> mp.mpc:
        total = mp.mpc(0)
        harmonic = mp.mpf(0)
        log_ratio = mp.log(b_end / tau)
        m = 0
        while True:
            if m > 0:
                harmonic += 1 / (m * b_end**m)
            coeff = log_ratio - harmonic
            term = 2 * coeff * mp.power(l_end, alpha + m) / (alpha + m)
            total += term
            if abs(term) < mp.mpf("1e-95"):
                break
            m += 1
        return total

    k = i_of(alpha, tau)
    d = mp.re(i_of(mp.re(alpha), tau))
    a1 = i_of(alpha, b_end) - k
    a2 = a2_series()
    y = 1 - w * a1 + (w**2 / 2) * a2 + s * k
    ratio = abs(y) / d

    def print_complex(label: str, z: mp.mpc) -> None:
        sign = "-" if mp.im(z) < 0 else "+"
        print(f"{label} =")
        print(mp.nstr(mp.re(z), 80))
        print(sign)
        print(mp.nstr(abs(mp.im(z)), 80), "i")
        print()

    print_complex("K", k)
    print("D =")
    print(mp.nstr(d, 80))
    print()
    print_complex("A1", a1)
    print_complex("A2", a2)
    print_complex("Y", y)
    print("|Y|^2 =")
    print(mp.nstr(abs(y) ** 2, 80))
    print()
    print("C^2 D^2 =")
    print(mp.nstr(c**2 * d**2, 80))
    print()
    print("ratio =")
    print(mp.nstr(ratio, 80))
    print()
    print("C - ratio =")
    print(mp.nstr(c - ratio, 30))

    if not ratio < c:
        raise RuntimeError(
            "sanity check failed: "
            f"ratio = {mp.nstr(ratio, 50)} >= C = {mp.nstr(c, 50)}"
        )

    if not abs(y) ** 2 < c**2 * d**2:
        raise RuntimeError("sanity check failed: |Y|^2 >= C^2 D^2")

    print("PASS numerical sanity check: ratio < C")


if __name__ == "__main__":
    main()
