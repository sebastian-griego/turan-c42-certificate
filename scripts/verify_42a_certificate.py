#!/usr/bin/env python3
"""Exact verifier for the proposed two-block C_42 certificate.

All pass/fail comparisons are made with integer or rational interval
arithmetic. Decimal arithmetic is used only for human-readable output.
"""

from __future__ import annotations

from dataclasses import dataclass
from decimal import Decimal, getcontext
from fractions import Fraction
from functools import lru_cache


DEN = 10**8
TAU = Fraction(36988243, DEN)
L = 1 - 2 * TAU
ONE_MINUS_TAU = 1 - TAU
TAU_TEXT = "36988243/100000000"

ALPHA_RE = Fraction(61927309, DEN)
ALPHA_IM = Fraction(57623741, DEN)
A = ALPHA_RE
B = ALPHA_IM
ALPHA_RE_TEXT = "61927309/100000000"
ALPHA_IM_TEXT = "57623741/100000000"

S_RE = 1 - ALPHA_RE
S_IM = -ALPHA_IM
ETA_RE = Fraction(59839764, DEN)
ETA_IM = Fraction(-34485185, DEN)
W_RE = ETA_RE - S_RE
W_IM = ETA_IM - S_IM
S_RE_TEXT = "38072691/100000000"
S_IM_TEXT = "-57623741/100000000"
ETA_RE_TEXT = "59839764/100000000"
ETA_IM_TEXT = "-34485185/100000000"
W_RE_TEXT = "21767073/100000000"
W_IM_TEXT = "23138556/100000000"

C = Fraction(3453269, 5000000)
PUBLIC_BOUND = Fraction(69368, 100000)
C_TEXT = "3453269/5000000"
PUBLIC_BOUND_TEXT = "69368/100000"

# Number of terms retained from I_A(x) = sum x^{A+r}/(A+r).
I_SERIES_TERMS = 90

# Number of terms retained from the A_2 coefficient series.
A2_SERIES_TERMS = 80

# Number of terms in the atanh series used to enclose logarithms.
LOG_SERIES_TERMS = 45

# Number of alternating Taylor terms used for exp(-x), sin(x), and cos(x).
TAYLOR_SERIES_TERMS = 35

# Every interval operation is rounded outward to this denominator.
ROUND_DEN = 10**60


class CertificateError(RuntimeError):
    pass


def check(condition: bool, message: str) -> None:
    if not condition:
        raise CertificateError(message)


def check_equal(actual: object, expected: object, label: str) -> None:
    if actual != expected:
        raise CertificateError(f"{label}: expected {expected}, got {actual}")


def round_down(q: Fraction) -> Fraction:
    return Fraction((q.numerator * ROUND_DEN) // q.denominator, ROUND_DEN)


def round_up(q: Fraction) -> Fraction:
    return Fraction(-((-q.numerator * ROUND_DEN) // q.denominator), ROUND_DEN)


def enclose(lo: Fraction, hi: Fraction) -> "Interval":
    return Interval(round_down(lo), round_up(hi))


@dataclass(frozen=True)
class Interval:
    lo: Fraction
    hi: Fraction

    def __post_init__(self) -> None:
        if self.lo > self.hi:
            raise ValueError((self.lo, self.hi))

    @staticmethod
    def point(x: Fraction | int) -> "Interval":
        q = Fraction(x)
        return Interval(q, q)

    def __add__(self, other: "Interval") -> "Interval":
        return enclose(self.lo + other.lo, self.hi + other.hi)

    def __sub__(self, other: "Interval") -> "Interval":
        return enclose(self.lo - other.hi, self.hi - other.lo)

    def __mul__(self, other: "Interval") -> "Interval":
        vals = (
            self.lo * other.lo,
            self.lo * other.hi,
            self.hi * other.lo,
            self.hi * other.hi,
        )
        return enclose(min(vals), max(vals))

    def scale(self, q: Fraction | int) -> "Interval":
        q = Fraction(q)
        if q >= 0:
            return enclose(q * self.lo, q * self.hi)
        return enclose(q * self.hi, q * self.lo)

    def widen(self, eps: Fraction) -> "Interval":
        return enclose(self.lo - eps, self.hi + eps)


@dataclass(frozen=True)
class ComplexInterval:
    re: Interval
    im: Interval

    @staticmethod
    def point(re: Fraction | int, im: Fraction | int = 0) -> "ComplexInterval":
        return ComplexInterval(Interval.point(re), Interval.point(im))

    def __add__(self, other: "ComplexInterval") -> "ComplexInterval":
        return ComplexInterval(self.re + other.re, self.im + other.im)

    def __sub__(self, other: "ComplexInterval") -> "ComplexInterval":
        return ComplexInterval(self.re - other.re, self.im - other.im)

    def scale(self, q: Fraction | int) -> "ComplexInterval":
        return ComplexInterval(self.re.scale(q), self.im.scale(q))

    def scale_interval(self, q: Interval) -> "ComplexInterval":
        return ComplexInterval(self.re * q, self.im * q)

    def mul_exact(self, re: Fraction, im: Fraction) -> "ComplexInterval":
        real = self.re.scale(re) - self.im.scale(im)
        imag = self.re.scale(im) + self.im.scale(re)
        return ComplexInterval(real, imag)

    def widen(self, eps: Fraction) -> "ComplexInterval":
        return ComplexInterval(self.re.widen(eps), self.im.widen(eps))


def dec(q: Fraction, prec: int = 70) -> str:
    getcontext().prec = prec
    return str(Decimal(q.numerator) / Decimal(q.denominator))


def interval_dec(x: Interval, prec: int = 45) -> str:
    return f"[{dec(x.lo, prec)}, {dec(x.hi, prec)}]"


def sci(q: Fraction, places: int = 16) -> str:
    getcontext().prec = places + 5
    value = Decimal(q.numerator) / Decimal(q.denominator)
    return f"{value:.{places}E}"


def fraction_str(q: Fraction) -> str:
    return str(q)


def interval_json(x: Interval) -> list[str]:
    return [fraction_str(x.lo), fraction_str(x.hi)]


def complex_interval_json(z: ComplexInterval) -> dict[str, list[str]]:
    return {"re": interval_json(z.re), "im": interval_json(z.im)}


def emit(verbose: bool, message: str) -> None:
    if verbose:
        print(message)


def log_near_one_interval(x: Fraction, terms: int = LOG_SERIES_TERMS) -> Interval:
    """Enclose log(x) using 2 atanh((x-1)/(x+1))."""
    check(x > 0, f"log_near_one_interval expected x > 0, got {x}")
    y = (x - 1) / (x + 1)
    check(abs(y) < 1, f"atanh log transform expected |y| < 1, got {y}")
    partial = Fraction(0)
    y_power = y
    y2 = y * y
    for k in range(terms + 1):
        partial += 2 * y_power / (2 * k + 1)
        y_power *= y2
    rem = 2 * abs(y_power) / ((2 * terms + 3) * (1 - y2))
    return enclose(partial - rem, partial + rem)


@lru_cache(maxsize=None)
def log2_interval() -> Interval:
    return log_near_one_interval(Fraction(2), LOG_SERIES_TERMS)


@lru_cache(maxsize=None)
def log_interval(x: Fraction) -> Interval:
    """Enclose log(x), reducing by powers of two before using atanh."""
    check(x > 0, f"log_interval expected x > 0, got {x}")
    z = x
    shift = 0
    while z < Fraction(2, 3):
        z *= 2
        shift += 1
    while z > Fraction(4, 3):
        z /= 2
        shift -= 1

    near = log_near_one_interval(z, LOG_SERIES_TERMS)
    if shift == 0:
        return near
    return near - log2_interval().scale(shift)


@lru_cache(maxsize=None)
def exp_neg_point_interval(x: Fraction, terms: int = TAYLOR_SERIES_TERMS) -> Interval:
    # e^{-x} = 1 - x + x^2/2! - ... . Here 0 < x < 1.
    check(0 <= x < 1, f"exp_neg_point_interval expected 0 <= x < 1, got {x}")
    term = Fraction(1)
    partial = Fraction(1)
    lower = None
    upper = partial
    for n in range(1, 2 * terms + 2):
        term *= x
        term /= n
        if n % 2:
            partial -= term
            lower = partial
        else:
            partial += term
            upper = partial
    check(lower is not None, "exp_neg_point_interval did not produce a lower bound")
    return enclose(lower, upper)


def exp_neg_interval(x: Interval) -> Interval:
    # These calls come from x^{-a} with 0 < x < 1 and 0 < a < 1, so
    # 0 <= -a log(x) < 1. On this interval e^{-x} is decreasing.
    check(0 <= x.lo <= x.hi < 1, f"exp_neg_interval expected 0 <= lo <= hi < 1, got {x}")
    lower = exp_neg_point_interval(x.hi).lo
    upper = exp_neg_point_interval(x.lo).hi
    return enclose(lower, upper)


@lru_cache(maxsize=None)
def cos_point_interval(x: Fraction, terms: int = TAYLOR_SERIES_TERMS) -> Interval:
    # cos(x) = 1 - x^2/2! + x^4/4! - ... . Here 0 <= x < 1.
    check(0 <= x < 1, f"cos_point_interval expected 0 <= x < 1, got {x}")
    x2 = x * x
    term = Fraction(1)
    partial = Fraction(1)
    lower = None
    upper = partial
    for k in range(1, 2 * terms + 2):
        term *= x2
        term /= (2 * k - 1) * (2 * k)
        if k % 2:
            partial -= term
            lower = partial
        else:
            partial += term
            upper = partial
    check(lower is not None, "cos_point_interval did not produce a lower bound")
    return enclose(lower, upper)


@lru_cache(maxsize=None)
def sin_point_interval(x: Fraction, terms: int = TAYLOR_SERIES_TERMS) -> Interval:
    # sin(x) = x - x^3/3! + x^5/5! - ... . Here 0 <= x < 1.
    check(0 <= x < 1, f"sin_point_interval expected 0 <= x < 1, got {x}")
    x2 = x * x
    term = x
    partial = x
    lower = None
    upper = partial
    for k in range(1, 2 * terms + 2):
        term *= x2
        term /= (2 * k) * (2 * k + 1)
        if k % 2:
            partial -= term
            lower = partial
        else:
            partial += term
            upper = partial
    check(lower is not None, "sin_point_interval did not produce a lower bound")
    return enclose(lower, upper)


def cos_interval(theta: Interval) -> Interval:
    # These calls come from b log(x) with 0 < x < 1 and 0 < b < 1.
    # In this certificate they all lie in (-1, 0), so use evenness and
    # monotonicity of cos on (0, 1).
    check(-1 < theta.lo <= theta.hi <= 0, f"cos_interval expected -1 < lo <= hi <= 0, got {theta}")
    abs_lo = -theta.hi
    abs_hi = -theta.lo
    lower = cos_point_interval(abs_hi).lo
    upper = cos_point_interval(abs_lo).hi
    return enclose(lower, upper)


def sin_interval(theta: Interval) -> Interval:
    # These calls come from b log(x) with 0 < x < 1 and 0 < b < 1.
    # In this certificate they all lie in (-1, 0), where sin is increasing.
    check(-1 < theta.lo <= theta.hi <= 0, f"sin_interval expected -1 < lo <= hi <= 0, got {theta}")
    abs_lo = -theta.hi
    abs_hi = -theta.lo
    lower = -sin_point_interval(abs_hi).hi
    upper = -sin_point_interval(abs_lo).lo
    return enclose(lower, upper)


@lru_cache(maxsize=None)
def x_to_alpha_interval(x: Fraction) -> ComplexInterval:
    logx = log_interval(x)
    exp_part = exp_neg_interval(logx.scale(-A))
    theta = logx.scale(B)
    return ComplexInterval(exp_part * cos_interval(theta), exp_part * sin_interval(theta))


@lru_cache(maxsize=None)
def x_to_a_interval(x: Fraction) -> Interval:
    return exp_neg_interval(log_interval(x).scale(-A))


def reciprocal_alpha_plus(r: int) -> tuple[Fraction, Fraction]:
    re = A + r
    im = B
    den = re * re + im * im
    return re / den, -im / den


def finite_i_alpha_sum(x: Fraction, terms: int = I_SERIES_TERMS) -> tuple[Fraction, Fraction]:
    total_re = Fraction(0)
    total_im = Fraction(0)
    x_power = Fraction(1)
    for r in range(terms):
        inv_re, inv_im = reciprocal_alpha_plus(r)
        total_re += x_power * inv_re
        total_im += x_power * inv_im
        x_power *= x
    return total_re, total_im


def finite_i_a_sum(x: Fraction, terms: int = I_SERIES_TERMS) -> Fraction:
    total = Fraction(0)
    x_power = Fraction(1)
    for r in range(terms):
        total += x_power / (A + r)
        x_power *= x
    return total


def i_alpha_tail_bound(x: Fraction, terms: int = I_SERIES_TERMS) -> Fraction:
    xa_upper = x_to_a_interval(x).hi
    return xa_upper * x**terms / ((A + terms) * (1 - x))


def i_alpha_interval(x: Fraction, terms: int = I_SERIES_TERMS) -> ComplexInterval:
    power = x_to_alpha_interval(x)
    sum_re, sum_im = finite_i_alpha_sum(x, terms)
    value = power.mul_exact(sum_re, sum_im)
    return value.widen(i_alpha_tail_bound(x, terms))


def i_a_lower(x: Fraction, terms: int = I_SERIES_TERMS) -> Fraction:
    return round_down(x_to_a_interval(x).lo * finite_i_a_sum(x, terms))


def a2_tail_bound(log_ratio_upper: Fraction, l_to_a_upper: Fraction) -> Fraction:
    # This implements
    # 2 L^a/(a+N) * (log(B/tau) L^N/(1-L)
    #     + (L/B)^N / ((1-B)(1-L/B))).
    m = A2_SERIES_TERMS
    first = log_ratio_upper * L**m / (1 - L)
    ratio = L / ONE_MINUS_TAU
    second = ratio**m / ((1 - ONE_MINUS_TAU) * (1 - ratio))
    return 2 * l_to_a_upper * (first + second) / (A + m)


def a2_interval() -> ComplexInterval:
    log_ratio = log_interval(ONE_MINUS_TAU / TAU)
    l_alpha = x_to_alpha_interval(L)
    total = ComplexInterval.point(0)
    harmonic = Fraction(0)
    l_power = Fraction(1)

    for m in range(A2_SERIES_TERMS):
        if m > 0:
            harmonic += Fraction(1, m) / (ONE_MINUS_TAU**m)
        coeff = log_ratio - Interval.point(harmonic)
        inv_re, inv_im = reciprocal_alpha_plus(m)
        term = l_alpha.scale(l_power).mul_exact(inv_re, inv_im).scale_interval(coeff).scale(2)
        total = total + term
        l_power *= L

    tail = a2_tail_bound(log_ratio.hi, x_to_a_interval(L).hi)
    return total.widen(tail)


def norm_square_upper(z: ComplexInterval) -> Fraction:
    vals = [
        re * re + im * im
        for re in (z.re.lo, z.re.hi)
        for im in (z.im.lo, z.im.hi)
    ]
    return max(vals)


def verify_radius(verbose: bool = True) -> tuple[Fraction, Fraction]:
    s_margin = C * C - (S_RE * S_RE + S_IM * S_IM)
    eta_margin = C * C - (ETA_RE * ETA_RE + ETA_IM * ETA_IM)
    check_equal(
        s_margin,
        Fraction(693863919, 5000000000000000),
        "exact margin for |1-alpha| < C",
    )
    check_equal(
        eta_margin,
        Fraction(1374484479, 10000000000000000),
        "exact margin for |eta| < C",
    )
    check(s_margin > 0, "radius check failed for |1-alpha| < C")
    check(eta_margin > 0, "radius check failed for |eta| < C")
    emit(verbose, f"PASS |1-alpha| < C: exact margin = {s_margin}")
    emit(verbose, f"PASS |eta| < C: exact margin = {eta_margin}")
    return s_margin, eta_margin


def verify_integrals(verbose: bool = True) -> tuple[ComplexInterval, Fraction, ComplexInterval, ComplexInterval]:
    k_interval = i_alpha_interval(TAU)
    i_alpha_b = i_alpha_interval(ONE_MINUS_TAU)
    a1_interval = i_alpha_b - k_interval
    d_lower = i_a_lower(TAU)
    a2 = a2_interval()

    emit(verbose, f"PASS K enclosure: Re {interval_dec(k_interval.re)}, Im {interval_dec(k_interval.im)}")
    emit(verbose, f"PASS D lower bound: D > {dec(d_lower, 45)}")
    emit(verbose, f"PASS A1 enclosure: Re {interval_dec(a1_interval.re)}, Im {interval_dec(a1_interval.im)}")
    emit(verbose, f"PASS A2 enclosure: Re {interval_dec(a2.re)}, Im {interval_dec(a2.im)}")
    return k_interval, d_lower, a1_interval, a2


def verify_main_inequality(
    k_interval: ComplexInterval,
    d_lower: Fraction,
    a1_interval: ComplexInterval,
    a2: ComplexInterval,
    verbose: bool = True,
) -> tuple[ComplexInterval, Fraction, Fraction, Fraction]:
    w2_re = W_RE * W_RE - W_IM * W_IM
    w2_im = 2 * W_RE * W_IM

    y = (
        ComplexInterval.point(1)
        - a1_interval.mul_exact(W_RE, W_IM)
        + a2.mul_exact(w2_re / 2, w2_im / 2)
        + k_interval.mul_exact(S_RE, S_IM)
    )

    y2_upper = norm_square_upper(y)
    lower = C * C * d_lower * d_lower
    check(
        y2_upper < lower,
        f"main inequality failed: |Y|^2 upper bound {y2_upper} "
        f"is not below C^2 D^2 lower bound {lower}",
    )
    gap = lower - y2_upper
    emit(verbose, f"PASS Y enclosure: Re {interval_dec(y.re)}, Im {interval_dec(y.im)}")
    emit(verbose, f"PASS |Y|^2 upper bound: {dec(y2_upper, 45)}")
    emit(verbose, f"PASS C^2 D^2 lower bound: {dec(lower, 45)}")
    emit(verbose, f"PASS comparison gap: {sci(gap)}; exact rational = {gap}")
    return y, y2_upper, lower, gap


def verify_final_bound(verbose: bool = True) -> None:
    check(C < PUBLIC_BOUND, "final comparison C < public bound failed")
    emit(verbose, "PASS final certified bound C = 0.6906538 < 0.69368")


def run_verification(verbose: bool = True) -> dict[str, object]:
    s_margin, eta_margin = verify_radius(verbose=verbose)
    k_interval, d_lower, a1_interval, a2 = verify_integrals(verbose=verbose)
    y, y2_upper, lower, gap = verify_main_inequality(
        k_interval,
        d_lower,
        a1_interval,
        a2,
        verbose=verbose,
    )
    verify_final_bound(verbose=verbose)

    return {
        "description": "Certificate for the asymptotic upper bound C_42 <= 0.6906538",
        "bound": C_TEXT,
        "previous_public_bound": PUBLIC_BOUND_TEXT,
        "tau": TAU_TEXT,
        "alpha": {"re": ALPHA_RE_TEXT, "im": ALPHA_IM_TEXT},
        "eta": {"re": ETA_RE_TEXT, "im": ETA_IM_TEXT},
        "s": {"re": S_RE_TEXT, "im": S_IM_TEXT},
        "w": {"re": W_RE_TEXT, "im": W_IM_TEXT},
        "series_terms": {
            "I_A": I_SERIES_TERMS,
            "A2": A2_SERIES_TERMS,
            "log": LOG_SERIES_TERMS,
            "taylor": TAYLOR_SERIES_TERMS,
        },
        "rounding_denominator": fraction_str(Fraction(ROUND_DEN, 1)),
        "verified_claims": {
            "radius_s_margin": fraction_str(s_margin),
            "radius_eta_margin": fraction_str(eta_margin),
            "main_gap": fraction_str(gap),
            "final_bound": f"{C_TEXT} < {PUBLIC_BOUND_TEXT}",
        },
        "enclosures": {
            "K": complex_interval_json(k_interval),
            "D_lower": fraction_str(d_lower),
            "A1": complex_interval_json(a1_interval),
            "A2": complex_interval_json(a2),
            "Y": complex_interval_json(y),
        },
        "bounds": {
            "Y_norm_square_upper": fraction_str(y2_upper),
            "C2D2_lower_bound": fraction_str(lower),
            "comparison_gap": fraction_str(gap),
        },
        "limitations": {
            "finite_threshold_N": None,
            "formalized_asymptotic_proof": False,
        },
    }


def main() -> None:
    run_verification(verbose=True)


if __name__ == "__main__":
    main()
