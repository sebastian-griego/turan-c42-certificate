# Improved one-block upper bound for Turan's pure power sum constant

## 1. Statement of the bound

This note records a proposed one-block certificate for the upper bound

$$
\limsup_{n\to\infty} R_n \le 0.6936763075 < 0.69368.
$$

The number `0.69368` is the current public upper bound being improved.

## 2. Parameters

Let

$$
\alpha=\frac{567376361+542239436i}{10^9},
$$

and write

$$
a=\operatorname{Re}\alpha=\frac{567376361}{10^9}.
$$

Set

$$
s=1-\alpha=\frac{432623639-542239436i}{10^9}
$$

and

$$
C=\frac{6936763075}{10^{10}}=0.6936763075.
$$

The finite truncation parameter used for the integral certificate is

$$
N=140.
$$

## 3. Elementary exact checks

The radius check is exact:

$$
6936763075^2
-
100(432623639^2+542239436^2)
=
61163413925>0.
$$

Since

$$
C^2-|s|^2
=
\frac{
6936763075^2
-
100(432623639^2+542239436^2)
}{10^{20}},
$$

this proves

$$
|s|<C.
$$

Also

$$
C=\frac{6936763075}{10^{10}}<0.69368.
$$

## 4. Integral certificate

For $\operatorname{Re}A>0$, define

$$
I_A=\int_0^{1/2}\frac{x^{A-1}}{1-x}\,dx.
$$

Using

$$
\frac1{1-x}=\sum_{r\ge0}x^r
$$

on $0\le x\le1/2$, we have

$$
I_A=\sum_{r=0}^{\infty}\frac{2^{-A-r}}{A+r}.
$$

For $A=\alpha$ or $A=a$, the tail from $r=140$ satisfies

$$
\sum_{r=140}^{\infty}
\left|\frac{2^{-A-r}}{A+r}\right|
\le
\frac{2^{1-a-140}}{140+a}
<7\cdot10^{-45}.
$$

The last strict inequality is checked using only rational arithmetic. Namely,

$$
a>\frac{14}{25},
$$

and

$$
2^{-a}<2^{-14/25}<\frac{17}{25},
$$

where the final inequality follows from

$$
\left(\frac{25}{17}\right)^{25}<2^{14}.
$$

Thus

$$
\frac{2^{1-a-140}}{140+a}
<
2^{-139}\frac{17}{25}\frac1{140+14/25}
=
\frac{17}{3514\cdot2^{139}}
<7\cdot10^{-45}.
$$

A certified rational interval computation gives

$$
0.60244919323019
<
\operatorname{Re}I_\alpha
<
0.60244919323024,
$$

$$
-0.96776228196568
<
\operatorname{Im}I_\alpha
<
-0.96776228196563,
$$

and

$$
I_a>1.5099327306413.
$$

Let

$$
x\in
\left[
\frac{60244919323019}{10^{14}},
\frac{60244919323024}{10^{14}}
\right],
$$

and

$$
y\in
\left[
-\frac{96776228196568}{10^{14}},
-\frac{96776228196563}{10^{14}}
\right].
$$

For $s=u-iv$ with

$$
u=\frac{432623639}{10^9},
\qquad
v=\frac{542239436}{10^9},
$$

we have

$$
|1+s(x+iy)|^2
=
(1+ux+vy)^2+(uy-vx)^2.
$$

For fixed $y$, this expression is a convex quadratic in $x$, so the maximum
over $x$ occurs at an endpoint. For each endpoint $x$, it is a convex quadratic
in $y$, so the maximum over $y$ occurs at an endpoint. Hence it is enough to
check the four corners.

The exact four-corner check gives

$$
|1+(1-\alpha)I_\alpha|^2<1.097056313558.
$$

The exact lower comparison gives

$$
C^2(1.5099327306413)^2>1.097056314748.
$$

Therefore

$$
|1+(1-\alpha)I_\alpha|<C I_a.
$$

## 5. Construction

Define

$$
\beta_l=\frac{(\alpha)_l}{l!}.
$$

Equivalently, $\beta_0=1$ and

$$
l\beta_l=\alpha(\beta_0+\cdots+\beta_{l-1}).
$$

For a positive integer $n$, set

$$
T=\lfloor n/2\rfloor.
$$

For $T<m\le n$, define

$$
P_m=\frac{n\beta_{n-m}}{m}.
$$

Define

$$
Y_n
=
n\beta_n
+
(1-\alpha)\sum_{m=T+1}^n P_m.
$$

The asymptotic argument proves that, for all sufficiently large $n$,

$$
|Y_n|
\le
C\sum_{m=T+1}^n |P_m|.
$$

Set target power sums $S_m$ as follows. For $1\le m\le T$,

$$
S_m=1-\alpha.
$$

For $T<m\le n$, if $Y_n=0$, set $S_m=0$. If $Y_n\ne0$, put

$$
u_n=\frac{Y_n}{|Y_n|},
$$

$$
\rho_n=
\frac{|Y_n|}{C\sum_{r=T+1}^n |P_r|},
$$

and define

$$
S_m=
\rho_n C u_n\frac{\overline{P_m}}{|P_m|}.
$$

Then $|S_m|\le C$ for every $m$, and

$$
\sum_{m=T+1}^n S_mP_m=Y_n.
$$

## 6. Recursive coefficients

Define $b_0=1$ and, for $1\le l\le n$,

$$
S_l+b_1S_{l-1}+\cdots+b_{l-1}S_1
=
1+b_1+\cdots+b_{l-1}-lb_l.
$$

Define

$$
p_n(Z)=
Z^{n-1}+b_1Z^{n-2}+\cdots+b_{n-1}.
$$

Let $y_2,\dots,y_n$ be the roots of $p_n$, counted with multiplicity, and put
$y_1=1$. Let

$$
M_n=\max_{1\le j\le n}|y_j|,
$$

and

$$
z_j^{(n)}=\frac{y_j}{M_n}.
$$

Since $y_1=1$, $M_n\ge1$, so

$$
\max_j |z_j^{(n)}|=1.
$$

## 7. Proof of the asymptotic condition

The condition

$$
\left|
\beta_n+(1-\alpha)
\sum_{h=0}^{n-T-1}\frac{\beta_h}{n-h}
\right|
\le
C
\sum_{h=0}^{n-T-1}\frac{|\beta_h|}{n-h}
$$

follows for all sufficiently large $n$ from

$$
\beta_h
=
\frac{h^{\alpha-1}}{\Gamma(\alpha)}(1+o(1)),
$$

$$
|\beta_h|
=
\frac{h^{a-1}}{|\Gamma(\alpha)|}(1+o(1)),
$$

and the Riemann sum limits

$$
\Gamma(\alpha)n^{1-\alpha}
\sum_{h=0}^{n-T-1}\frac{\beta_h}{n-h}
\to
I_\alpha,
$$

$$
|\Gamma(\alpha)|n^{1-a}
\sum_{h=0}^{n-T-1}\frac{|\beta_h|}{n-h}
\to
I_a,
$$

$$
\Gamma(\alpha)n^{1-\alpha}\beta_n\to1.
$$

The limiting strict inequality is

$$
|1+(1-\alpha)I_\alpha|<CI_a,
$$

which was certified above.

## 8. Proof that $b_n=0$

For $l\le T$, the recursion gives

$$
b_l=\beta_l.
$$

Set

$$
d_l=b_l-\beta_l,
\qquad
w_l=S_l-(1-\alpha).
$$

Then

$$
d_l=w_l=0
\qquad
(1\le l\le T).
$$

Subtract the $\beta$ identity from the $b$ identity. For $l\le n$, the
potential quadratic term $d_rw_{l-r}$ vanishes because it would require
$r>T$ and $l-r>T$, hence $l\ge2T+2>n$, impossible.

This gives, for $T<l\le n$,

$$
\sum_{m=T+1}^{l}\beta_{l-m}w_m
=
\alpha\sum_{r=T+1}^{l-1}d_r-ld_l.
$$

Set

$$
\Delta_l=-ld_l.
$$

Then

$$
\Delta_l
=
\sum_{m=T+1}^{l}\beta_{l-m}w_m
+
\alpha\sum_{r=T+1}^{l-1}\frac{\Delta_r}{r}.
$$

We prove by induction that

$$
\Delta_l
=
\sum_{m=T+1}^{l}\frac{l}{m}\beta_{l-m}w_m.
$$

The coefficient calculation uses

$$
(l-m)\beta_{l-m}
=
\alpha\sum_{q=0}^{l-m-1}\beta_q.
$$

At $l=n$,

$$
\Delta_n
=
\sum_{m=T+1}^{n}P_m(S_m-(1-\alpha))
=
Y_n-(1-\alpha)\sum_{m=T+1}^{n}P_m
=
n\beta_n.
$$

Since

$$
\Delta_n=-n(b_n-\beta_n),
$$

this gives

$$
b_n=0.
$$

## 9. Power sum bound

Let

$$
Q_k=\sum_{j=1}^n y_j^k.
$$

Newton's identities for the roots $y_2,\dots,y_n$ of $p_n$, together with
$y_1=1$, give

$$
Q_k+b_1Q_{k-1}+\cdots+b_{k-1}Q_1
=
1+b_1+\cdots+b_{k-1}-kb_k
$$

for $1\le k\le n$, with $b_n=0$ used when $k=n$.

The $S_k$ satisfy the same triangular system, so

$$
Q_k=S_k
$$

for $1\le k\le n$. Therefore

$$
\sum_{j=1}^{n}(z_j^{(n)})^k
=
M_n^{-k}S_k.
$$

Since $M_n\ge1$ and $|S_k|\le C$,

$$
\left|
\sum_{j=1}^{n}(z_j^{(n)})^k
\right|
\le C
$$

for $1\le k\le n$.

Thus $R_n\le C$ for all sufficiently large $n$, and

$$
\limsup_{n\to\infty} R_n
\le
C
=
0.6936763075.
$$

## 10. Reproducibility

The displayed numerical inequalities are certified by rational interval
arithmetic in

```text
scripts/verify_42a_certificate.py
```

The high-precision mpmath script

```text
scripts/numeric_sanity_check.py
```

is only a numerical sanity check. It is not the certificate.

## 11. Eventual disclosure note

See `certificate/README.md` for the disclosure note to preserve before any
public submission.
