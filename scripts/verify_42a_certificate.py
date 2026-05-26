#!/usr/bin/env python3
"""Exact verifier for the proposed C_42 upper-bound certificate.

All pass/fail comparisons are made with integer or rational arithmetic.
Decimal arithmetic is used only for human-readable output.
"""

from __future__ import annotations

from dataclasses import dataclass
from decimal import Decimal, getcontext
from fractions import Fraction


DEN = 10**9
ALPHA_RE = Fraction(567376361, DEN)
ALPHA_IM = Fraction(542239436, DEN)
A = ALPHA_RE
B = ALPHA_IM
S_RE = Fraction(432623639, DEN)
S_IM_ABS = Fraction(542239436, DEN)  # s = S_RE - i S_IM_ABS
C = Fraction(6936763075, 10**10)
N = 140
TAIL = Fraction(7, 10**45)


@dataclass(frozen=True)
class Interval:
    lo: Fraction
    hi: Fraction

    def __post_init__(self) -> None:
        if self.lo > self.hi:
            raise ValueError((self.lo, self.hi))

    def __add__(self, other: Interval) -> Interval:
        return Interval(self.lo + other.lo, self.hi + other.hi)

    def __sub__(self, other: Interval) -> Interval:
        return Interval(self.lo - other.hi, self.hi - other.lo)

    def __mul__(self, other: Interval) -> Interval:
        vals = (
            self.lo * other.lo,
            self.lo * other.hi,
            self.hi * other.lo,
            self.hi * other.hi,
        )
        return Interval(min(vals), max(vals))

    def scale(self, q: Fraction) -> Interval:
        if q >= 0:
            return Interval(q * self.lo, q * self.hi)
        return Interval(q * self.hi, q * self.lo)

    def widen(self, eps: Fraction) -> Interval:
        return Interval(self.lo - eps, self.hi + eps)


def dec(q: Fraction, prec: int = 70) -> str:
    getcontext().prec = prec
    return str(Decimal(q.numerator) / Decimal(q.denominator))


def interval_dec(x: Interval, prec: int = 45) -> str:
    return f"[{dec(x.lo, prec)}, {dec(x.hi, prec)}]"


def log2_interval(k_terms: int = 80) -> Interval:
    partial = sum(
        Fraction(2, (2 * k + 1) * 3 ** (2 * k + 1))
        for k in range(k_terms + 1)
    )
    remainder = Fraction(
        2,
        (2 * k_terms + 3) * 3 ** (2 * k_terms + 3),
    ) / (1 - Fraction(1, 9))
    return Interval(partial, partial + remainder)


def exp_neg_point_interval(x: Fraction, terms: int = 60) -> Interval:
    # e^{-x} = 1 - x + x^2/2! - ... .  For 0 < x < 1 the terms decrease.
    term = Fraction(1)
    partial = Fraction(1)
    upper = partial
    lower = None
    for n in range(1, 2 * terms + 2):
        term *= x
        term /= n
        if n % 2:
            partial -= term
            lower = partial
        else:
            partial += term
            upper = partial
    assert lower is not None
    return Interval(lower, upper)


def cos_point_interval(x: Fraction, terms: int = 60) -> Interval:
    # cos(x) = 1 - x^2/2! + x^4/4! - ... .  For 0 < x < 1 the terms decrease.
    x2 = x * x
    term = Fraction(1)
    partial = Fraction(1)
    upper = partial
    lower = None
    for k in range(1, 2 * terms + 2):
        term *= x2
        term /= (2 * k - 1) * (2 * k)
        if k % 2:
            partial -= term
            lower = partial
        else:
            partial += term
            upper = partial
    assert lower is not None
    return Interval(lower, upper)


def sin_point_interval(x: Fraction, terms: int = 60) -> Interval:
    # sin(x) = x - x^3/3! + x^5/5! - ... .  For 0 < x < 1 the terms decrease.
    x2 = x * x
    term = x
    partial = x
    upper = partial
    lower = None
    for k in range(1, 2 * terms + 2):
        term *= x2
        term /= (2 * k) * (2 * k + 1)
        if k % 2:
            partial -= term
            lower = partial
        else:
            partial += term
            upper = partial
    assert lower is not None
    return Interval(lower, upper)


def exp_neg_interval(x: Interval) -> Interval:
    # e^{-x} is decreasing.
    lower = exp_neg_point_interval(x.hi).lo
    upper = exp_neg_point_interval(x.lo).hi
    return Interval(lower, upper)


def cos_interval_on_small_positive(x: Interval) -> Interval:
    # cos(x) is decreasing on this interval, which lies in (0, 1).
    assert 0 < x.lo < x.hi < 1
    lower = cos_point_interval(x.hi).lo
    upper = cos_point_interval(x.lo).hi
    return Interval(lower, upper)


def sin_interval_on_small_positive(x: Interval) -> Interval:
    # sin(x) is increasing on this interval, which lies in (0, 1).
    assert 0 < x.lo < x.hi < 1
    lower = sin_point_interval(x.lo).lo
    upper = sin_point_interval(x.hi).hi
    return Interval(lower, upper)


def finite_sum_alpha() -> tuple[Fraction, Fraction]:
    re = Fraction(0)
    im = Fraction(0)
    for r in range(N):
        p = 567376361 + r * DEN
        q = 542239436
        den = p * p + q * q
        re += Fraction(DEN * p, den * 2**r)
        im -= Fraction(DEN * q, den * 2**r)
    return re, im


def finite_sum_a() -> Fraction:
    total = Fraction(0)
    for r in range(N):
        total += Fraction(DEN, (567376361 + r * DEN) * 2**r)
    return total


def two_minus_alpha_interval() -> tuple[Interval, Interval]:
    log2 = log2_interval()
    u = log2.scale(A)
    v = log2.scale(B)
    e = exp_neg_interval(u)
    c = cos_interval_on_small_positive(v)
    s = sin_interval_on_small_positive(v)
    real = e * c
    imag_positive = e * s
    imag = Interval(-imag_positive.hi, -imag_positive.lo)
    return real, imag


def complex_interval_times_exact(
    x: Interval,
    y: Interval,
    z_re: Fraction,
    z_im: Fraction,
) -> tuple[Interval, Interval]:
    real = x.scale(z_re) - y.scale(z_im)
    imag = x.scale(z_im) + y.scale(z_re)
    return real, imag


def verify_radius() -> None:
    margin = 6936763075**2 - 100 * (432623639**2 + 542239436**2)
    assert margin == 61163413925
    assert margin > 0
    print(f"PASS radius inequality: exact margin = {margin}")


def verify_tail() -> None:
    assert A > Fraction(14, 25)
    assert 25**25 < 2**14 * 17**25
    exact_majorant = Fraction(17, 3514 * 2**139)
    assert exact_majorant < TAIL
    margin = TAIL - exact_majorant
    print(f"PASS tail bound: 17/(3514*2^139) < 7e-45, exact margin = {margin}")


def verify_integrals() -> tuple[Interval, Interval, Fraction]:
    s_alpha_re, s_alpha_im = finite_sum_alpha()
    two_alpha_re, two_alpha_im = two_minus_alpha_interval()
    i_re, i_im = complex_interval_times_exact(
        two_alpha_re,
        two_alpha_im,
        s_alpha_re,
        s_alpha_im,
    )
    i_re = i_re.widen(TAIL)
    i_im = i_im.widen(TAIL)

    re_target = Interval(
        Fraction(60244919323019, 10**14),
        Fraction(60244919323024, 10**14),
    )
    im_target = Interval(
        Fraction(-96776228196568, 10**14),
        Fraction(-96776228196563, 10**14),
    )
    assert re_target.lo < i_re.lo and i_re.hi < re_target.hi
    assert im_target.lo < i_im.lo and i_im.hi < im_target.hi
    print(f"PASS Re I_alpha enclosure: {interval_dec(i_re)}")
    print(f"PASS Im I_alpha enclosure: {interval_dec(i_im)}")

    log2 = log2_interval()
    e_lower = exp_neg_interval(log2.scale(A)).lo
    s_a = finite_sum_a()
    i_a_lower = e_lower * s_a
    i_a_threshold = Fraction(15099327306413, 10**13)
    assert i_a_lower > i_a_threshold
    print(
        "PASS I_a lower bound: "
        f"certified lower bound = {dec(i_a_lower, 45)}"
    )
    return i_re, i_im, i_a_lower


def corner_value(x: Fraction, y: Fraction) -> Fraction:
    u = S_RE
    v = S_IM_ABS
    return (1 + u * x + v * y) ** 2 + (u * y - v * x) ** 2


def verify_corners() -> Fraction:
    xs = [
        Fraction(60244919323019, 10**14),
        Fraction(60244919323024, 10**14),
    ]
    ys = [
        Fraction(-96776228196568, 10**14),
        Fraction(-96776228196563, 10**14),
    ]
    values = [corner_value(x, y) for x in xs for y in ys]
    max_corner = max(values)
    upper = Fraction(1097056313558, 10**12)
    assert all(value < upper for value in values)
    print(
        "PASS four-corner upper bound: "
        f"max corner = {dec(max_corner, 45)}"
    )
    return max_corner


def verify_lower_comparison() -> Fraction:
    i_a_floor = Fraction(15099327306413, 10**13)
    lower = C * C * i_a_floor * i_a_floor
    target = Fraction(1097056314748, 10**12)
    assert lower > target
    print(
        "PASS C^2 I_a^2 lower bound: "
        f"C^2*(1.5099327306413)^2 = {dec(lower, 45)}"
    )
    return lower


def verify_final(max_corner: Fraction, lower: Fraction) -> None:
    upper_corner = Fraction(1097056313558, 10**12)
    lower_target = Fraction(1097056314748, 10**12)
    assert max_corner < upper_corner < lower_target < lower
    print(
        "PASS comparison gap: "
        f"1.097056314748 - 1.097056313558 = "
        f"{dec(lower_target - upper_corner, 30)}"
    )
    assert C < Fraction(69368, 100000)
    print("PASS final certified bound C = 0.6936763075 < 0.69368")


def main() -> None:
    verify_radius()
    verify_tail()
    verify_integrals()
    max_corner = verify_corners()
    lower = verify_lower_comparison()
    verify_final(max_corner, lower)


if __name__ == "__main__":
    main()
