# Hypothesis and definitions

## 1. The question

A random source produces pairs of integers. A target pair is fixed in
advance. The process stops when the target appears. Does a selection rule —
or an observer's intention — change the waiting time?

The original project answered "yes" and tried to demonstrate it with a
program. Version 1.0 separates the question into three hypotheses that can
be tested independently.

## 2. Formal objects

- **Alphabet** $A = \{lo, \ldots, hi\}$, for example $\{-20,\ldots,20\}$.
- **Source** $S$: a process producing pairs $(a_t,b_t) \in A^2$.
- **Target** $(c,d) \in A^2$, fixed before the trial.
- **Hitting time** $T = \min\{t \ge 1 : (a_t,b_t) = (c,d)\}$.
- **Selection rule** $F$: a deterministic map
  $$(x_t,y_t) = F(x_{t-1},y_{t-1},a_t,b_t,c,d).$$
  The rule updates an auxiliary pair $(x,y)$. It does not write to the
  source.
- **Control arm**: run $S$, stop at $T$, ignore $F$.
- **Selection arm**: run $S$, update $F$ on every draw, stop at $T$. The
  stopping predicate is the same as in the control arm.

The original program is a special case: $A=\{-20,\ldots,20\}$, $S$ is a
classical PRNG, and $F$ is the sign-and-midpoint rule in
[`../legacy/original.cpp`](../legacy/original.cpp).

## 3. The three hypotheses

### H0 — classical null

The source is independent of the selection rule. Then

$$\Pr(T=k) = (1-p)^{k-1}p, \qquad p = \Pr(a=c)\Pr(b=d),$$

so $\mathbb{E}T = 1/p$ and $\operatorname{Var}T = (1-p)/p^2$. For a uniform
source on $41$ values, $p = 1/1681$ and $\mathbb{E}T \approx 1681$.

### H1 — algorithmic influence

The selection rule itself changes the distribution of future draws without
a physical feedback channel. Operationalization: on the same seed or
entropy stream, $T_{\text{sel}} < T_{\text{ctrl}}$ beyond sampling error.

### H2 — observer influence

A conscious observer's intention changes the distribution of a **live**
physical source without a known physical channel. Operationalization: a
target chosen by a human participant is hit faster than a target chosen by
a verifiable random process, using the same live source and the same
selection rule.

## 4. Why H1 and H2 are different

H1 is a claim about the program: the rule $F$ is supposed to influence the
source. In the reference implementation it cannot, because $F$ is not an
input to the source or to the stopping predicate. The proof is in
[`MATH.md`](MATH.md).

H2 is a claim about the world: the observer's intention is supposed to
correlate with a physical random source. This is not a property of the
code. It requires a live source, a human participant, and a protocol that
rules out conventional explanations. The original program has neither a
human in the loop nor a live source, so it cannot test H2.

## 5. What v1.0 establishes

| Claim | Status |
|---|---|
| The selection rule changes the waiting time in the reference implementation | **Falsified** — pathwise equality, 0/20,000 mismatches |
| The waiting time is geometric with $p \approx 1/1681$ | **Confirmed** — means and SDs match theory |
| A human observer can bias a live source | **Open** — protocol specified, no data yet |

## 6. What would count as evidence for H2

A positive result must be:

1. **Preregistered** before data collection, with a fixed primary endpoint.
2. **Powered** for a stated smallest effect of interest.
3. **Run on a live physical source** whose health is monitored.
4. **Blinded** where possible: the analyst does not know the arm labels
   until the dataset is frozen.
5. **Replicated** by an independent group using the same protocol.
6. **Reported with an effect size and a confidence interval**, not only a
   p-value.

## 7. What does not count

- A single run, however impressive.
- Choosing the target after seeing the data.
- Stopping when the result looks good.
- Comparing different ranges, sources, or selection rules post hoc.
- Anecdotes from games or daily life.
- A p-value selected from many unpublished analyses.

## 8. Falsifiability

H2 is falsifiable at a stated effect size: a sufficiently powered
experiment with no effect rules out effects above that size. It does not
rule out every conceivable effect, and the protocol says so explicitly.
