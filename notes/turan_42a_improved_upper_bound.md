# Improved two-block upper bound for Turan's pure power sum constant

## 1. Statement of the bound

This note records a proposed asymptotic two-block certificate for the upper
bound

$$ \limsup_{n\to\infty} R_n \le 0.6906538 < 0.69368. $$

For $n\ge1$, let

$$ R_n= \min_{\max_i |z_i|=1} \max_{1\le k\le n} \left|\sum_{i=1}^n z_i^k\right|, $$

where the minimum is over $z_1,\dots,z_n\in\mathbb C$. The constant considered
here is

$$ C_{42}=\limsup_{n\to\infty} R_n. $$

The number `0.69368` is the current public upper bound being improved. The
proof is asymptotic; it does not provide an explicit finite threshold $N$.

## 2. Parameters

Let

$$ \tau=\frac{36988243}{10^8}=0.36988243, $$

$$ \alpha=\frac{61927309+57623741i}{10^8}, $$

and

$$ \eta=\frac{59839764-34485185i}{10^8}. $$

Set

$$ s=1-\alpha=\frac{38072691-57623741i}{10^8}, $$

$$ w=\eta-s=\frac{21767073+23138556i}{10^8}, $$

and

$$ C=\frac{3453269}{5000000}=0.6906538. $$

Also put

$$ L=1-2\tau, \qquad B=1-\tau. $$

## 3. Elementary exact checks

The two radius checks are exact:

$$ C^2-|1-\alpha|^2 = \frac{693863919}{5000000000000000} >0, $$

and

$$ C^2-|\eta|^2 = \frac{1374484479}{10000000000000000} >0. $$

Therefore

$$ |1-\alpha|<C, \qquad |\eta|<C. $$

Also

$$ C=\frac{3453269}{5000000}<0.69368. $$

## 4. Integral certificate

For $\mathrm{Re} A>0$ and $0<x<1$, define

$$ I_A(x)=\int_0^x \frac{u^{A-1}}{1-u}\,du. $$

Using

$$ \frac1{1-u}=\sum_{r\ge0}u^r $$

on $0\le u<x<1$, we have

$$ I_A(x)=\sum_{r=0}^\infty \frac{x^{A+r}}{A+r}. $$

Define

$$ K=I_\alpha(\tau), \qquad D=I_{\mathrm{Re}\alpha}(\tau), $$

$$ A_1=I_\alpha(1-\tau)-I_\alpha(\tau), $$

and

$$ A_2= 2\int_0^{1-2\tau} \frac{u^{\alpha-1}}{1-u} \log\left(\frac{1-\tau-u}{\tau}\right)\,du. $$

For $A_2$, the exact series used in the verifier is

$$ A_2= 2\sum_{m=0}^\infty c_m\frac{L^{\alpha+m}}{\alpha+m}, $$

where

$$ c_0=\log\frac{B}{\tau}, $$

and, for $m\ge1$,

$$ c_m= \log\frac{B}{\tau} - \sum_{q=1}^m\frac{1}{qB^q}. $$

To obtain the series, note that $0\le u\le L=1-2\tau<B=1-\tau$. Hence

$$ \log\left(\frac{B-u}{\tau}\right) = \log\left(\frac B\tau\right) + \log\left(1-\frac uB\right) = \log\left(\frac B\tau\right) - \sum_{q\ge1}\frac{u^q}{qB^q}. $$

Also

$$ \frac1{1-u}=\sum_{r\ge0}u^r. $$

Thus

$$ \frac1{1-u} \log\left(\frac{B-u}{\tau}\right) = \sum_{m\ge0}c_m u^m, $$

with the coefficients above. Termwise integration gives the displayed series
for $A_2$.

For $m\ge N$,

$$ |c_m| \le \log\frac B\tau+\sum_{q=1}^m B^{-q} \le \log\frac B\tau+\frac{B^{-m}}{1-B}. $$

Therefore

$$ \left| 2\sum_{m\ge N}c_m\frac{L^{\alpha+m}}{\alpha+m} \right| \le \frac{2L^a}{a+N} \left( \log\frac B\tau\frac{L^N}{1-L} + \frac{(L/B)^N}{(1-B)(1-L/B)} \right), $$

where $a=\mathrm{Re}\alpha$. This is the tail bound implemented in the
exact verifier.

The rational interval checker certifies the following enclosures:

$$ \mathrm{Re}K\in [0.255173870464090649926689408117142889949723769, 0.255173870464090649926689408117142889949749041], $$

$$ \mathrm{Im}K\in [-0.737641128754973412525026216515512688051489281, -0.737641128754973412525026216515512688051464009], $$

$$ D>1.03454335564960554464331381156451557904676270, $$

$$ \mathrm{Re}A_1\in [0.635243760435234627738324749616468423184635173, 0.635243760435234627778087458508340926525686452], $$

$$ \mathrm{Im}A_1\in [-0.266900766223130007775201668103068294516423969, -0.266900766223130007735438959211195791175372689], $$

$$ \mathrm{Re}A_2\in [-0.0765877685048176650582192830617894175978639240, -0.0765877685048176650582192830617706928846897567], $$

and

$$ \mathrm{Im}A_2\in [-0.362224889263510931184059808762355523758993944, -0.362224889263510931184059808762336799045819777]. $$

Now set

$$ Y=1-wA_1+\frac{w^2}{2}A_2+sK. $$

The verifier certifies

$$ \mathrm{Re}Y\in [0.490543800494073940325352038219744140253636975, 0.490543800494073940343207732755079418503591593], $$

and

$$ \mathrm{Im}Y\in [-0.519512292824219544542933624750386589139572330, -0.519512292824219544525077930215051310889617712]. $$

For a rectangle in the complex plane, the function $x^2+y^2$ is a convex
quadratic in $x$ for fixed $y$, and a convex quadratic in $y$ for fixed $x$.
Hence its maximum over the rectangle is attained at a corner. Checking the
four corners of the certified rectangle for $Y$ gives

$$ |Y|^2 < 0.510526242598647450670698846558829323291175577. $$

The lower bound for $D$ gives

$$ C^2D^2 > 0.510526397604979025520969801453222348904263483. $$

Thus

$$ |Y|<CD. $$

The limiting slack is small but strict. Numerically,

$$ \frac{|Y|}{D}\approx0.690653695151631, $$

so

$$ C-\frac{|Y|}{D}\approx1.05\cdot10^{-7}. $$

The proof does not rely on this decimal approximation. The strict comparison
is certified by the rational interval verifier through $|Y|^2<C^2D^2$.

## Slack summary

| Quantity | Certified or numerical value |
| --- | --- |
| Claimed bound $C$ | $0.6906538$ |
| Numerical abs(Y)/D | approximately $0.690653695151631$ |
| Numerical slack C - abs(Y)/D | approximately $1.05\cdot10^{-7}$ |
| Certified comparison | $\lvert Y\rvert^2<C^2D^2$ |
| Explicit finite threshold $N$ | not provided |

## 5. Construction

For $l\ge0$, define

$$ \beta_l=\frac{(\alpha)_l}{l!}. $$

Equivalently,

$$ \beta_0=1, $$

and

$$ l\beta_l=\alpha(\beta_0+\cdots+\beta_{l-1}) \qquad(l\ge1). $$

Fix a large positive integer $n$, and put

$$ A_n=\lfloor \tau n\rfloor. $$

Define three index ranges:

$$ B_n=\{1,\dots,A_n\}, $$

$$ J_n=\{A_n+1,\dots,n-A_n-1\}, $$

and

$$ F_n=\{n-A_n,\dots,n\}. $$

For $k\in B_n$, set

$$ S_k=s=1-\alpha. $$

For $k\in J_n$, set

$$ S_k=\eta. $$

For $m\in F_n$, define

$$ P_m=\frac{n}{m}\beta_{n-m}. $$

Since $\alpha$ is not a nonpositive integer, $(\alpha)_l\ne0$ for every
$l\ge0$. Hence $P_m\ne0$ for all $m\in F_n$, so the expression
$\overline{P_m}/|P_m|$ below is well-defined.

Define

$$ Y_n= n\beta_n -nw\sum_{m\in J_n}\frac{\beta_{n-m}}{m} + \frac{nw^2}{2} \sum_{m_1,m_2\in J_n,\;m_1+m_2\le n} \frac{\beta_{n-m_1-m_2}}{m_1m_2} + s\sum_{m\in F_n}P_m. $$

The asymptotic argument below proves that, for all sufficiently large $n$,

$$ |Y_n| \le C\sum_{m\in F_n}|P_m|. $$

Choose the remaining values $S_m$, for $m\in F_n$, so that

$$ |S_m|\le C $$

and

$$ \sum_{m\in F_n}S_mP_m=Y_n. $$

One explicit choice is this. If $Y_n=0$, set all final $S_m=0$. Otherwise put

$$ u_n=\frac{Y_n}{|Y_n|}, $$

$$ \rho_n= \frac{|Y_n|} {C\sum_{r\in F_n}|P_r|}, $$

and define

$$ S_m= \rho_n C u_n\frac{\overline{P_m}}{|P_m|} \qquad(m\in F_n). $$

Then $0\le\rho_n\le1$, so $|S_m|\le C$, and the desired linear identity holds.

## 6. Recursive coefficients

Define $b_0=1$ and, for $1\le l\le n$,

$$ S_l+b_1S_{l-1}+\cdots+b_{l-1}S_1 = 1+b_1+\cdots+b_{l-1}-lb_l. $$

Define

$$ p_n(Z)=Z^{n-1}+b_1Z^{n-2}+\cdots+b_{n-1}. $$

Let $y_2,\dots,y_n$ be the roots of $p_n$, counted with multiplicity, and put
$y_1=1$. Let

$$ \Lambda_n=\max_{1\le j\le n}|y_j|, $$

and

$$ z_j^{(n)}=\frac{y_j}{\Lambda_n}. $$

Since $y_1=1$, we have $\Lambda_n\ge1$, and therefore

$$ \max_j |z_j^{(n)}|=1. $$

## 7. Proof that $b_n=0$

Let

$$ S(z)=\sum_{l\ge1}S_lz^l, \qquad B(z)=\sum_{l\ge0}b_lz^l. $$

The recursion gives, for $l\ge1$,

$$ [z^l]B(z)S(z) = [z^l]\frac{z}{1-z}B(z)-[z^l]zB'(z). $$

Hence

$$ B(z)S(z)=\frac{z}{1-z}B(z)-zB'(z), $$

so

$$ \frac{B'(z)}{B(z)}=\frac{1}{1-z}-\frac{S(z)}{z}. $$

Integrating and using $B(0)=1$ gives

$$ B(z)=(1-z)^{-1} \exp\left(-\sum_{m\ge1}\frac{S_mz^m}{m}\right). $$

Since $S_m=s=1-\alpha$ for $m\le A_n$, this becomes, through degree $n$,

$$ B(z) = (1-z)^{-\alpha} \exp\left( -\sum_{m>A_n}\frac{(S_m-s)z^m}{m} \right). $$

Because $\tau>1/3$, three correction indices are already too large to
contribute to the coefficient of $z^n$, since $3(A_n+1)>n$ for all
sufficiently large $n$.

Also, every final index $m\in F_n$ satisfies $m\ge n-A_n$, so a final index
plus any correction index exceeds $n$. Thus final corrections enter $b_n$
only linearly.

Therefore

$$ b_n= \beta_n -w\sum_{m\in J_n}\frac{\beta_{n-m}}{m} + \frac{w^2}{2} \sum_{m_1,m_2\in J_n,\;m_1+m_2\le n} \frac{\beta_{n-m_1-m_2}}{m_1m_2} - \sum_{m\in F_n} \frac{(S_m-s)\beta_{n-m}}{m}. $$

Multiplying by $n$, and using the definition of $P_m$, the condition

$$ \sum_{m\in F_n}S_mP_m=Y_n $$

is exactly the condition $b_n=0$.

## 8. Proof of the asymptotic condition

Let

$$ a=\mathrm{Re}\alpha>0, \qquad A_n=\lfloor \tau n\rfloor, $$

and write

$$ J_n=\{A_n+1,\dots,n-A_n-1\}, \qquad F_n=\{n-A_n,\dots,n\}. $$

We use the standard estimate

$$ \beta_l= \frac{\Gamma(l+\alpha)}{\Gamma(\alpha)\Gamma(l+1)} = \frac{l^{\alpha-1}}{\Gamma(\alpha)}\left(1+O(l^{-1})\right) $$

as $l\to\infty$. The estimate is uniform on ranges $l\ge\varepsilon n$,
where $\varepsilon>0$ is fixed. On ranges touching $l=0$, the endpoint is
handled by first truncating to $l\ge L_0$, applying the uniform estimate, and
then letting $L_0\to\infty$. This is valid because $a>0$, so $u^{a-1}$ is
integrable at $u=0$.

The following limits hold:

$$ \Gamma(\alpha)n^{1-\alpha}\beta_n\to1, $$

$$ \Gamma(\alpha)n^{1-\alpha} \sum_{m\in J_n}\frac{\beta_{n-m}}{m} \to \int_\tau^{1-\tau}\frac{u^{\alpha-1}}{1-u}\,du =A_1, $$

$$ \Gamma(\alpha)n^{1-\alpha} \sum_{m\in F_n}\frac{\beta_{n-m}}{m} \to \int_0^\tau\frac{u^{\alpha-1}}{1-u}\,du =K, $$

and

$$ |\Gamma(\alpha)|n^{1-a} \sum_{m\in F_n}\frac{|\beta_{n-m}|}{m} \to \int_0^\tau\frac{u^{a-1}}{1-u}\,du =D. $$

For the double sum, group terms by

$$ l=n-m_1-m_2. $$

Then $0\le l\le n-2A_n-2$, and

$$ \sum_{m_1,m_2\in J_n,\;m_1+m_2=n-l} \frac{1}{m_1m_2} = \sum_{m=A_n+1}^{n-l-A_n-1} \frac{1}{m(n-l-m)}. $$

By partial fractions,

$$ \sum_{m=A_n+1}^{n-l-A_n-1} \frac{1}{m(n-l-m)} = \frac{2}{n-l} \sum_{m=A_n+1}^{n-l-A_n-1} \frac{1}{m}. $$

If $l/n\to u$, with $0\le u\le1-2\tau$, then

$$ n \sum_{m=A_n+1}^{n-l-A_n-1} \frac{1}{m(n-l-m)} \to \frac{2}{1-u} \log\left(\frac{1-\tau-u}{\tau}\right). $$

Therefore

$$ \Gamma(\alpha)n^{1-\alpha} \sum_{m_1,m_2\in J_n,\;m_1+m_2\le n} \frac{\beta_{n-m_1-m_2}}{m_1m_2} \to 2\int_0^{1-2\tau} \frac{u^{\alpha-1}}{1-u} \log\left(\frac{1-\tau-u}{\tau}\right)\,du =A_2. $$

Lemma. Replacing $\tau n$ by $A_n=\lfloor\tau n\rfloor$ does not change any
of the normalized limits above.

Proof. The symmetric difference between the summation ranges defined by
$A_n$ and by $\tau n$ contains $O(1)$ indices in each one-dimensional
boundary. Each one-dimensional boundary term has size $O(n^{a-2})$ before
normalization, since $\beta_{n-m}=O(n^{a-1})$ away from the endpoint and
$m\asymp n$. After multiplication by $n^{1-a}$, the total contribution is
$O(n^{-1})$.

For the double sum, changing one boundary changes $O(n)$ summands. Away from
the endpoint, each summand has size $O(n^{a-3})$ before normalization:
$\beta_{n-m_1-m_2}=O(n^{a-1})$ and $m_1m_2\asymp n^2$. After multiplication
by $n^{1-a}$, these boundary contributions are again $O(n^{-1})$. Endpoint
ranges with $l=n-m_1-m_2$ bounded are handled by first truncating to
$l\ge L_0$, applying the uniform estimate away from zero, and then letting
$L_0\to\infty$, using $a>0$.

It follows that

$$ \Gamma(\alpha)n^{-\alpha}Y_n \to 1-wA_1+\frac{w^2}{2}A_2+sK =Y, $$

and

$$ |\Gamma(\alpha)|n^{-a} \sum_{m\in F_n}|P_m| \to D. $$

Consequently

$$ \frac{|Y_n|}{\sum_{m\in F_n}|P_m|} \to \frac{|Y|}{D}. $$

Since the certified computation proves $|Y|<CD$, there exists $N$ such that
for all $n\ge N$,

$$ |Y_n| \le C\sum_{m\in F_n}|P_m|. $$

## 9. Power sum bound

Let

$$ Q_k=\sum_{j=1}^n y_j^k. $$

Newton's identities for the roots $y_2,\dots,y_n$ of $p_n$, together with
$y_1=1$, give

$$ Q_k+b_1Q_{k-1}+\cdots+b_{k-1}Q_1 = 1+b_1+\cdots+b_{k-1}-kb_k $$

for $1\le k\le n$, with $b_n=0$ used when $k=n$.

For $1\le k\le n-1$, this is the usual Newton identity for the $n-1$ roots
of $p_n$, after adding the extra root $y_1=1$. For $k=n$, Newton's identity
for a monic polynomial of degree $n-1$ has no $nb_n$ coefficient term. Thus
the same displayed formula remains valid exactly when $b_n=0$, which is why
the construction enforces $b_n=0$.

The $S_k$ satisfy the same triangular system, so

$$ Q_k=S_k $$

for $1\le k\le n$. Therefore

$$ \sum_{j=1}^n (z_j^{(n)})^k = \Lambda_n^{-k}S_k. $$

Since $\Lambda_n\ge1$ and $|S_k|\le C$,

$$ \left| \sum_{j=1}^n (z_j^{(n)})^k \right| \le C $$

for $1\le k\le n$.

Thus $R_n\le C$ for all sufficiently large $n$, and

$$ \limsup_{n\to\infty} R_n \le C = 0.6906538. $$

## 10. Reproducibility

The displayed numerical inequalities are certified by exact rational interval
arithmetic in

```text
scripts/verify_42a_certificate.py
```

A transcript is included at

```text
certificate/verify_42a_certificate.output.txt
```

The high-precision mpmath script

```text
scripts/numeric_sanity_check.py
```

is only a numerical sanity check. It is not the certificate.

## 11. Eventual disclosure note

See `certificate/README.md` for the disclosure note to preserve before any
public submission.
