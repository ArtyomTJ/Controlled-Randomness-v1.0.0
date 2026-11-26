# Mathematical note: causal isolation and power

## 1. Setup

Let a source produce a fixed sequence of pairs
$z_t=(a_t,b_t)$ for a given seed or entropy stream. Let
$T=\min\{t\ge 1:z_t=(c,d)\}$.

The control arm computes nothing except $T$. The selection arm maintains an
auxiliary pair $(x_t,y_t)$:

$$(x_t,y_t)=F(x_{t-1},y_{t-1},z_t,c,d).$$

The stopping rule in both arms is $z_t=(c,d)$.

## 2. Theorem (causal isolation)

**Theorem.** For every fixed source trajectory $(z_t)_{t\ge 1}$ and every
target $(c,d)$,

$$T_{\text{sel}} = T_{\text{ctrl}}.$$

**Proof.** By induction on $t$, the sequence $z_t$ is the same in both arms:
the source is not modified by $F$, and $F$ reads $z_t$ but does not write to
it. The stopping predicate depends only on $z_t$. Therefore the first index
at which the predicate is true is the same in both arms. $\square$

**Corollary.** Every statistic of $T$ — mean, median, variance, quantiles,
hitting-time distribution — is identical in the two arms. No test can
distinguish them except through numerical error or a bug.

The auxiliary pair $(x,y)$ may follow different trajectories in the two
arms. That is irrelevant: $(x,y)$ is not read by the stopping predicate and
is not an input to the source.

**Consequence for the original hypothesis.** H1 ("the deterministic
selection rule biases the source") is false for any implementation with
this architecture, not just for this particular code. Changing the rule
$F$, fixing input validation, or using a better PRNG cannot change the
conclusion.

## 3. Distribution under H0

If the source is iid with value probabilities $\pi(v)=\Pr(a=v)$, then

$$p=\Pr(z=(c,d))=\pi(c)\pi(d),$$

and

$$\Pr(T=k)=(1-p)^{k-1}p, \qquad \mathbb{E}T=\frac{1}{p}, \qquad
\operatorname{Var}T=\frac{1-p}{p^2}.$$

For a uniform alphabet of size $m=hi-lo+1$:

$$p=\frac{1}{m^2}, \qquad \mathbb{E}T=m^2, \qquad
\sigma_T=\sqrt{m^2(m^2-1)}\approx m^2.$$

For $m=41$: $p=1/1681$, $\mathbb{E}T\approx1681$,
$\sigma_T\approx1681$.

For the MSVC modulo generator, $32768=41\cdot799+9$, so the values
$-20,\ldots,-12$ have probability $800/32768$ and the rest
$799/32768$. The exact $p$ values used in the experiment are:

| Target | $p$ | $\mathbb{E}T$ | $\sigma_T$ |
|---|---:|---:|---:|
| $(17,19)$ | $(799/32768)^2$ | 1681.92 | 1681.42 |
| $(-13,-7)$ | $(800\cdot799)/32768^2$ | 1679.82 | 1679.32 |

## 4. Why single runs are useless

The standard deviation is approximately equal to the mean. Two single runs
can differ by a factor of two or more without any effect. In the v1.0
dataset, $T$ ranges from $1$ to $16{,}535$ within one target. A comparison
of two one-off runs is a comparison of two draws from a distribution with
$\sigma\approx\mu$; it has almost no evidential value.

## 5. Power for a shift in the mean

For a two-sample comparison of means with a normal approximation, the
number of trials per arm is

$$N \approx \frac{2(z_{1-\alpha/2}+z_{1-\beta})^2\sigma^2}{\Delta^2}.$$

With $\alpha=0.05$, power $0.8$, and $\sigma\approx1681$:

| Relative effect $\Delta/\mu$ | $\Delta$ (trials) | $N$ per arm |
|---|---:|---:|
| 10% | 168 | $\approx1{,}570$ |
| 5% | 84 | $\approx6{,}280$ |
| 2% | 34 | $\approx39{,}200$ |
| 1% | 17 | $\approx157{,}000$ |
| 0.5% | 8.4 | $\approx628{,}000$ |

The hitting-time endpoint is expensive because the distribution is
heavy-tailed. A bit-level test on a quantum source is more efficient: to
detect a bias $\varepsilon$ in a fair bit sequence with the same power,

$$N \approx \frac{(z_{1-\alpha/2}+z_{1-\beta})^2}{4\varepsilon^2}
\text{ bits}.$$

For $\varepsilon=10^{-3}$ this is about $2\times10^6$ bits; for
$\varepsilon=10^{-4}$ about $2\times10^8$ bits. A QRNG produces these
counts quickly, but the human-in-the-loop design must be planned around
the slower component.

## 6. Paired sign test

If the primary endpoint is "the human-target trial is faster than its
matched machine-target trial", let

$$q=\Pr(T_{\text{human}}<T_{\text{machine}}).$$

Under H0, $q=0.5$. The sign test requires approximately

$$N \approx \frac{(z_{1-\alpha/2}+z_{1-\beta})^2 q(1-q)}{(q-0.5)^2}$$

pairs. For $q=0.52$: $N\approx4{,}900$; for $q=0.51$:
$N\approx19{,}600$. This is the basis for the protocol's sample size.

## 7. Multiplicity and sequential monitoring

- Fix one primary endpoint before data collection.
- Use Holm-Bonferroni for secondary endpoints.
- If interim analyses are used, use a group-sequential boundary
  (O'Brien-Fleming) with a prespecified alpha-spending function. Do not
  stop at a nominal p-value without adjusting for the looks.
- Report all deviations and all exclusions.

## 8. What the mathematics does not decide

The theorem is about the reference architecture. It does not say that
consciousness cannot affect a physical source; it says that **this
program** has no channel through which such an effect could enter. H2 needs
a different experiment, not a different line of code.
