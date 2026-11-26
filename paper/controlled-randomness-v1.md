# Controlled Randomness

## A Preregistered Test of Selection and Observer Effects on Random Sources

**Artem Larin** · Version 1.0.0 · 2026-11-26

### Abstract

Can a random process be biased by selection or observation? The original
project proposed a selection rule that keeps pairs closer to a target and
reported that the target seemed to appear faster. We show that the rule is
causally isolated from the random source and from the stopping predicate:
for a fixed seed, the selection and control arms are the same experiment. A
paired experiment confirms this with 20,000 comparisons and zero mismatches.
This rules out the algorithmic version of the hypothesis. The observer
version — that a conscious participant can bias a live physical source —
remains open. We specify a preregistered protocol to test it, with a live
quantum RNG, human-chosen versus machine-chosen targets, 5,000 matched
pairs, blinding, and a sequential analysis plan. The contribution is a clear
separation of the two claims and a credible instrument for the stronger one.

## 1. Introduction

The idea is simple and old: if you select outcomes that resemble the one you
want, the desired outcome may arrive sooner. In games with random rewards
this feeling is common; in the original project it became an experiment. A
program drew pairs of integers, kept the pair "closest" to a target, and
stopped when the target appeared. The reported impression was that the
target arrived faster with the selection rule than without it.

The claim has two very different forms.

**H1 — algorithmic influence.** The selection rule itself changes the
distribution of future draws, without a physical feedback channel. This is
a claim about the program's causal structure. It can be settled by
inspection and by a paired experiment.

**H2 — observer influence.** A conscious observer's intention changes the
distribution of a live physical source. This is a claim about the world. It
requires a live source, a human participant, and a protocol that rules out
noise, bias, and selective reporting.

The original project conflated the two. This note separates them. Section 2
proves that H1 is false for the reference architecture. Section 3 reports a
paired null experiment. Section 4 specifies the protocol for H2.

The contribution is not a positive result. It is the removal of a design
error and the construction of an experiment that can, in principle, produce
a credible positive result.

## 2. Model and the causal-isolation result

Let the alphabet be $A=\{lo,\ldots,hi\}$, the target $(c,d)\in A^2$, and the
source produce $z_t=(a_t,b_t)$. The hitting time is
$T=\min\{t\ge1:z_t=(c,d)\}$.

The control arm observes $T$. The selection arm maintains an auxiliary pair

$$(x_t,y_t)=F(x_{t-1},y_{t-1},z_t,c,d),$$

where $F$ is the original sign-and-midpoint rule. The stopping predicate in
both arms is $z_t=(c,d)$.

**Theorem.** For every fixed source trajectory and every target,
$T_{\text{sel}}=T_{\text{ctrl}}$.

**Proof.** By induction on $t$, the sequence $z_t$ is identical in both arms:
$F$ reads $z_t$ but does not write to the source, and the source does not
read $(x,y)$. The stopping predicate depends only on $z_t$. Therefore the
first index at which it holds is the same in both arms. $\square$

**Corollary.** Every statistic of $T$ is identical in the two arms. The
auxiliary pair $(x,y)$ may differ, but it is not read by the stopping rule
and is not an input to the source.

If the source is iid with value probabilities $\pi(v)$, then
$p=\pi(c)\pi(d)$ and

$$\Pr(T=k)=(1-p)^{k-1}p,\qquad \mathbb{E}T=\frac1p,\qquad
\operatorname{Var}T=\frac{1-p}{p^2}.$$

For a uniform alphabet of size $m$, $p=1/m^2$ and $\mathbb{E}T=m^2$. For
$m=41$, $\mathbb{E}T\approx1681$ and $\sigma_T\approx1681$.

The theorem is not a property of the particular rule $F$. Any rule that
only updates auxiliary state has the same consequence. Changing the rule,
fixing the input validation, or using a better PRNG cannot change the
conclusion.

## 3. The v1.0 experiment

The paired experiment uses the MSVC-compatible generator of the original
project, the alphabet $\{-20,\ldots,20\}$, and two targets: $(17,19)$ and
$(-13,-7)$. Each trial runs the control and selection arms with the same
seed. The sample is 10,000 paired trials per target.

| Target | Trials per arm | Mismatches | Mean $T$ | SD | Min | Max | Theory mean |
|---|---:|---:|---:|---:|---:|---:|---:|
| $(17,19)$ | 10,000 | 0 | 1702.6 | 1720.8 | 1 | 16,535 | 1681.9 |
| $(-13,-7)$ | 10,000 | 0 | 1667.4 | 1681.8 | 1 | 15,896 | 1679.8 |

The selection arm matches the control arm in every pair. The sample means
are within sampling error of the theoretical mean (standard error about 17).
The standard deviations are consistent with the geometric prediction.

The spread is the practical lesson: within one target, $T$ ranges from 1 to
16,535. A single comparison of two runs has almost no evidential value. The
feeling that a ritual "works" can be produced by this variance alone.

## 4. The observer hypothesis

H2 cannot be tested with a deterministic PRNG and no observer. The protocol
in [`../docs/PROTOCOL.md`](../docs/PROTOCOL.md) specifies the missing
ingredients:

- a **live** physical source (a certified QRNG or an auditable public
  quantum randomness service), with health checks;
- a **human participant** who chooses the target before the trial;
- a **machine arm** with a target drawn from a committed, verifiable
  randomness beacon independent of the experimental source;
- **blinding** of the analyst until the dataset and analysis script are
  frozen;
- a **primary endpoint** fixed in advance: the probability $q$ that the
  human-target trial is faster than its matched machine-target trial;
- a **sample size** of 5,000 pairs, powered for $q=0.52$ at 80% power;
- **group-sequential monitoring** with O'Brien-Fleming boundaries;
- a **replication** requirement before any strong claim.

Under H0, $q=0.5$. Under H2, $q>0.5$. The protocol also includes an
exploratory per-draw human-selection arm on a smaller alphabet, because the
original intuition is about the act of selecting, not only about the target.

The protocol is deliberately conservative. A positive result from a single
laboratory, a single source, or a single participant would not settle the
question. It would justify a replication.

## 5. Discussion

### Relation to the literature

The experimental literature on intention and random number generators is
small and contested. The Princeton Engineering Anomalies Research program
reported small correlations between operator intention and random binary
sequences over many years (Jahn et al., 1997). A meta-analysis of
psychokinesis experiments with random number generators reported a small
overall effect (Bösch, Steinkamp, & Boller, 2006), but the result has been
debated and has not led to a consensus or to a widely accepted physical
mechanism. The present project does not assume that literature is correct;
it builds a protocol that would make a positive result credible.

Quantum randomness is well understood as a physical resource (Acín &
Masanes, 2016). The "observer effect" in quantum mechanics is a consequence
of measurement and decoherence (Zurek, 2003), not evidence that conscious
intention can steer a random source. A claim of the latter kind needs its
own experiment.

### What the null result does and does not mean

The v1.0 null result is a statement about the reference architecture. It
does not say that consciousness cannot affect matter. It says that this
program has no channel through which such an effect could enter. That is a
useful negative result: it tells the next experiment what must change.

### Limitations

- The v1.0 experiment uses a classical PRNG; it cannot test H2.
- The protocol is a template; it has not been executed.
- A single laboratory and a single source cannot establish a general
  effect.
- The choice of target, alphabet, and selection rule fixes one
  operationalization of "intention"; others need their own protocols.

### Open science

The code, the raw data, the analysis script, and the protocol are public.
The null result is reported with the same care that a positive result would
receive. This is the minimum for a claim that, if true, would change
everything.

## 6. Conclusion

The original program could not have detected the effect it was looking for:
the selection rule is causally isolated from the source. The paired
experiment confirms the isolation with zero mismatches in 20,000
comparisons. What remains is the stronger hypothesis, and it now has a
protocol that can test it. The next step is data, not code.

## References

- Acín, A., & Masanes, L. (2016). Certified randomness in quantum physics.
  *Nature*, 540, 213–219.
- Benjamin, D. J., Berger, J. O., Johnson, V. E., et al. (2018). Redefine
  statistical significance. *Nature Human Behaviour*, 2, 6–10.
- Benjamini, Y., & Hochberg, Y. (1995). Controlling the false discovery
  rate: A practical and powerful approach to multiple testing. *Journal of
  the Royal Statistical Society: Series B*, 57(1), 289–300.
- Bösch, H., Steinkamp, F., & Boller, E. (2006). Examining psychokinesis:
  The interaction of human intention with random number generators — A
  meta-analysis. *Psychological Bulletin*, 132(4), 497–523.
- Jahn, R. G., Dunne, B. J., Nelson, R. D., Dobyns, Y. H., & Bradish, G. J.
  (1997). Correlations of random binary sequences with pre-stated operator
  intention: A review of a 12-year program. *Journal of Scientific
  Exploration*, 11(3), 345–367.
- Nosek, B. A., Ebersole, C. R., DeHaven, A. C., & Mellor, D. T. (2018).
  The preregistration revolution. *Proceedings of the National Academy of
  Sciences*, 115(11), 2600–2606.
- Rouder, J. N., Speckman, P. L., Sun, D., Morey, R. D., & Iverson, G.
  (2009). Bayesian t tests for accepting and rejecting the null hypothesis.
  *Psychonomic Bulletin & Review*, 16(2), 225–237.
- Wald, A. (1945). Sequential tests of statistical hypotheses. *Annals of
  Mathematical Statistics*, 16(2), 117–186.
- Zurek, W. H. (2003). Decoherence, einselection, and the quantum origins of
  the classical. *Reviews of Modern Physics*, 75(3), 715–775.
