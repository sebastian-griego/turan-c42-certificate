# Improved two-block upper bound for Turan's pure power sum constant

## 1. Statement of the bound

This note records a proposed two-block certificate for the upper bound

$$
\limsup_{n\to\infty} R_n \le 0.6906538 < 0.69368.
$$

The number `0.69368` is the current public upper bound being improved.

## 2. Parameters

Let

$$
\tau=\frac{36988243}{10^8}=0.36988243,
$$

$$
\alpha=\frac{61927309+57623741i}{10^8},
$$

and

$$
\eta=\frac{59839764-34485185i}{10^8}.
$$

Set

$$
s=1-\alpha=\frac{38072691-57623741i}{10^8},
$$

$$
w=\eta-s=\frac{21767073+23138556i}{10^8},
$$

and

$$
C=\frac{3453269}{5000000}=0.6906538.
$$

Also put

$$
L=1-2\tau,
\qquad
B=1-\tau.
$$

## 3. Elementary exact checks

The two radius checks are exact:

$$
C^2-|1-\alpha|^2
=
\frac{693863919}{5000000000000000}
>0,
$$

and

$$
C^2-|\eta|^2
=
\frac{1374484479}{10000000000000000}
>0.
$$

Therefore

$$
|1-\alpha|<C,
\qquad
|\eta|<C.
$$

Also

$$
C=\frac{3453269}{5000000}<0.69368.
$$

## 4. Integral certificate

For $\operatorname{Re} A>0$ and $0<x<1$, define

$$
I_A(x)=\int_0^x \frac{u^{A-1}}{1-u}\,du.
$$

Using

$$
\frac1{1-u}=\sum_{r\ge0}u^r
$$

on $0\le u<x<1$, we have

$$
I_A(x)=\sum_{r=0}^\infty \frac{x^{A+r}}{A+r}.
$$

Define

$$
K=I_\alpha(\tau),
\qquad
D=I_{\operatorname{Re}\alpha}(\tau),
$$

$$
A_1=I_\alpha(1-\tau)-I_\alpha(\tau),
$$

and

$$
A_2=
2\int_0^{1-2\tau}
\frac{u^{\alpha-1}}{1-u}
\log\left(\frac{1-\tau-u}{\tau}\right)\,du.
$$

For $A_2$, the exact series used in the verifier is

$$
A_2=
2\sum_{m=0}^\infty
c_m\frac{L^{\alpha+m}}{\alpha+m},
$$

where

$$
c_0=\log\frac{B}{\tau},
$$

and, for $m\ge1$,

$$
c_m=
\log\frac{B}{\tau}
-
\sum_{q=1}^m\frac{1}{qB^q}.
$$

The rational interval checker certifies the following enclosures:

$$
\operatorname{Re}K\in
[0.255173870464090649926689408117142889949723769,
0.255173870464090649926689408117142889949749041],
$$

$$
\operatorname{Im}K\in
[-0.737641128754973412525026216515512688051489281,
-0.737641128754973412525026216515512688051464009],
$$

$$
D>1.03454335564960554464331381156451557904676270,
$$

$$
\operatorname{Re}A_1\in
[0.635243760435234627738324749616468423184635173,
0.635243760435234627778087458508340926525686452],
$$

$$
\operatorname{Im}A_1\in
[-0.266900766223130007775201668103068294516423969,
-0.266900766223130007735438959211195791175372689],
$$

$$
\operatorname{Re}A_2\in
[-0.0765877685048176650582192830617894175978639240,
-0.0765877685048176650582192830617706928846897567],
$$

and

$$
\operatorname{Im}A_2\in
[-0.362224889263510931184059808762355523758993944,
-0.362224889263510931184059808762336799045819777].
$$

Now set

$$
Y=1-wA_1+\frac{w^2}{2}A_2+sK.
$$

The verifier certifies

$$
\operatorname{Re}Y\in
[0.490543800494073940325352038219744140253636975,
0.490543800494073940343207732755079418503591593],
$$

and

$$
\operatorname{Im}Y\in
[-0.519512292824219544542933624750386589139572330,
-0.519512292824219544525077930215051310889617712].
$$

For a rectangle in the complex plane, the function $x^2+y^2$ is a convex
quadratic in $x$ for fixed $y$, and a convex quadratic in $y$ for fixed $x$.
Hence its maximum over the rectangle is attained at a corner. Checking the
four corners of the certified rectangle for $Y$ gives

$$
|Y|^2
<
0.510526242598647450670698846558829323291175577.
$$

The lower bound for $D$ gives

$$
C^2D^2
>
0.510526397604979025520969801453222348904263483.
$$

Thus

$$
|Y|<CD.
$$

## 5. Construction

For $l\ge0$, define

$$
\beta_l=\frac{(\alpha)_l}{l!}.
$$

Equivalently,

$$
\beta_0=1,
$$

and

$$
l\beta_l=\alpha(\beta_0+\cdots+\beta_{l-1})
\qquad(l\ge1).
$$

Fix a large positive integer $n$, and put

$$
A_n=\lfloor \tau n\rfloor.
$$

Define three index ranges:

$$
B_n=\{1,\dots,A_n\},
$$

$$
M_n=\{A_n+1,\dots,n-A_n-1\},
$$

and

$$
F_n=\{n-A_n,\dots,n\}.
$$

For $k\in B_n$, set

$$
S_k=s=1-\alpha.
$$

For $k\in M_n$, set

$$
S_k=\eta.
$$

For $m\in F_n$, define

$$
P_m=\frac{n}{m}\beta_{n-m}.
$$

Define

$$
Y_n=
n\beta_n
-nw\sum_{m\in M_n}\frac{\beta_{n-m}}{m}
+
\frac{nw^2}{2}
\sum_{\substack{m_1,m_2\in M_n\\m_1+m_2\le n}}
\frac{\beta_{n-m_1-m_2}}{m_1m_2}
+
s\sum_{m\in F_n}P_m.
$$

The asymptotic argument below proves that, for all sufficiently large $n$,

$$
|Y_n|
\le
C\sum_{m\in F_n}|P_m|.
$$

Choose the remaining values $S_m$, for $m\in F_n$, so that

$$
|S_m|\le C
$$

and

$$
\sum_{m\in F_n}S_mP_m=Y_n.
$$

One explicit choice is this. If $Y_n=0$, set all final $S_m=0$. Otherwise put

$$
u_n=\frac{Y_n}{|Y_n|},
$$

$$
\rho_n=
\frac{|Y_n|}
{C\sum_{r\in F_n}|P_r|},
$$

and define

$$
S_m=
\rho_n C u_n\frac{\overline{P_m}}{|P_m|}
\qquad(m\in F_n).
$$

Then $0\le\rho_n\le1$, so $|S_m|\le C$, and the desired linear identity holds.

## 6. Recursive coefficients

Define $b_0=1$ and, for $1\le l\le n$,

$$
S_l+b_1S_{l-1}+\cdots+b_{l-1}S_1
=
1+b_1+\cdots+b_{l-1}-lb_l.
$$

Define

$$
p_n(Z)=Z^{n-1}+b_1Z^{n-2}+\cdots+b_{n-1}.
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

Since $y_1=1$, we have $M_n\ge1$, and therefore

$$
\max_j |z_j^{(n)}|=1.
$$

## 7. Proof that $b_n=0$

The recursion for $b_l$ is equivalent, through degree $n$, to

$$
B(z)
=
(1-z)^{-\alpha}
\exp\left(
-\sum_{m>A_n}\frac{(S_m-s)z^m}{m}
\right),
$$

where

$$
B(z)=\sum_{l\ge0}b_lz^l.
$$

Because $\tau>1/3$, three correction indices are already too large to
contribute to the coefficient of $z^n$, since $3(A_n+1)>n$ for all
sufficiently large $n$.

Also, every final index $m\in F_n$ satisfies $m\ge n-A_n$, so a final index
plus any correction index exceeds $n$. Thus final corrections enter $b_n$
only linearly.

Therefore

$$
b_n=
\beta_n
-w\sum_{m\in M_n}\frac{\beta_{n-m}}{m}
+
\frac{w^2}{2}
\sum_{\substack{m_1,m_2\in M_n\\m_1+m_2\le n}}
\frac{\beta_{n-m_1-m_2}}{m_1m_2}
-
\sum_{m\in F_n}
\frac{(S_m-s)\beta_{n-m}}{m}.
$$

Multiplying by $n$, and using the definition of $P_m$, the condition

$$
\sum_{m\in F_n}S_mP_m=Y_n
$$

is exactly the condition $b_n=0$.

## 8. Proof of the asymptotic condition

The only remaining point is the eventual inequality

$$
|Y_n|
\le
C\sum_{m\in F_n}|P_m|.
$$

Using

$$
\beta_l=
\frac{\Gamma(l+\alpha)}{\Gamma(\alpha)\Gamma(l+1)}
=
\frac{l^{\alpha-1}}{\Gamma(\alpha)}(1+o(1)),
$$

one obtains the limits

$$
\Gamma(\alpha)n^{1-\alpha}\beta_n\to1,
$$

$$
\Gamma(\alpha)n^{1-\alpha}
\sum_{m\in M_n}\frac{\beta_{n-m}}{m}
\to A_1,
$$

$$
\Gamma(\alpha)n^{1-\alpha}
\sum_{\substack{m_1,m_2\in M_n\\m_1+m_2\le n}}
\frac{\beta_{n-m_1-m_2}}{m_1m_2}
\to A_2,
$$

$$
\Gamma(\alpha)n^{1-\alpha}
\sum_{m\in F_n}\frac{\beta_{n-m}}{m}
\to K,
$$

and

$$
|\Gamma(\alpha)|n^{1-\operatorname{Re}\alpha}
\sum_{m\in F_n}\frac{|\beta_{n-m}|}{m}
\to D.
$$

Consequently,

$$
\frac{|Y_n|}{\sum_{m\in F_n}|P_m|}
\to
\frac{|Y|}{D}.
$$

The certified inequality $|Y|<CD$ therefore implies that, for all sufficiently
large $n$,

$$
|Y_n|
\le
C\sum_{m\in F_n}|P_m|.
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
\sum_{j=1}^n (z_j^{(n)})^k
=
M_n^{-k}S_k.
$$

Since $M_n\ge1$ and $|S_k|\le C$,

$$
\left|
\sum_{j=1}^n (z_j^{(n)})^k
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
0.6906538.
$$

## 10. Reproducibility

The displayed numerical inequalities are certified by exact rational interval
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
