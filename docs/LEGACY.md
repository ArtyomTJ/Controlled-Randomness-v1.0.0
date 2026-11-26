# The original program, preserved

[`../legacy/original.cpp`](../legacy/original.cpp) is the original
implementation of the idea. It is kept verbatim for provenance and because
it contains the experiment's seed: a target, a stream of random pairs, and a
rule that keeps a pair "closer" to the target.

The v1.0 implementation keeps the rule and the experiment, but makes the
causal structure explicit.

## 1. The original rules

The program draws pairs $(a,b)$ from $\{-20,\ldots,20\}$ and stops when the
draw equals the target $(c,d)$. It maintains an auxiliary pair $(x,y)$
initialized to $(1,1)$. After each draw:

- If the target is positive-positive, and the current pair is negative-
  negative while the new pair is positive-positive or mixed, replace the
  current pair.
- If the current pair is mixed and the new pair is positive-positive or
  mixed, replace it.
- If both the current and the new pair are positive-positive, compare the
  distance between the target midpoint and the current midpoint with the
  distance between the target midpoint and the new midpoint; keep the closer
  one.
- If either current value is zero, replace the pair.
- The negative-target case mirrors this with absolute values.

The full code is preserved unchanged. The v1.0 rule is a line-by-line port
in [`../src/python/crlab/experiment.py`](../src/python/crlab/experiment.py)
and in the C++ source.

## 2. What the original program got right

- It asked a clear question: does selection change the waiting time?
- It defined a target and a repeatable selection rule.
- It made the idea executable, which is more than most "reality hacking"
  proposals do.
- It naturally suggests a control condition: the same loop without the
  selection rule.

## 3. What it cannot do

### 3.1 The selection rule is causally isolated

The rule writes only to $(x,y)$. It does not write to the generator, and
the stopping predicate is $(a,b)=(c,d)$, not $(x,y)=(c,d)$. Therefore, for
a fixed seed, the control and selection arms are the same experiment. This
is proved in [`MATH.md`](MATH.md) and confirmed in
[`RESULTS-v1.md`](RESULTS-v1.md).

This is not a small bug. No repair of the rule can fix it: the architecture
has no channel from the selection to the source.

### 3.2 There is no observer and no live source

The program has a deterministic PRNG seeded by `time(nullptr)`. The
"observer" is absent. The "system" that is supposed to receive the signal
is a local PRNG that does not read the selection variables. A test of H2
needs a live physical source and a human participant; the original program
has neither.

### 3.3 Input validation does not match the specification

The prompt says the two numbers must both be positive or both negative and
must not be 1. The validation rejects only the exact value `1`, does not
check the signs, and does not reject 0. A mixed input such as $(5,-5)$ falls
into the negative branch and is processed with `abs`, which is not the
specified behaviour.

### 3.4 The "closest pair" is not the closest pair

The rules prioritize sign classes. For example, when the current pair is
mixed and the new pair is mixed, the new pair replaces the old one even if
it is farther from the target in the midpoint metric. The midpoint metric
itself is degenerate: $(0,20)$ and $(10,10)$ have the same midpoint, so they
are indistinguishable to the rule. This does not affect the null result
(the rule is isolated either way), but it matters if the rule is ever used
as an actual selection strategy.

### 3.5 Reproducibility and bias

- `srand(time(nullptr))` has one-second resolution; two runs started in the
  same second share a seed.
- `rand() % 41` has a modulo bias: $32768 = 41\cdot799 + 9$, so
  $-20,\ldots,-12$ occur slightly more often.
- The program prints only the iteration count; the auxiliary pair is never
  observed, so there is no record of the "signal" it is supposed to send.

## 4. What survives

The idea of a target, a stream, and a selection rule survives. v1.0 keeps
it and adds:

- a control arm;
- a paired design with identical seeds;
- a proof of causal isolation;
- a live-source protocol for the observer hypothesis;
- a reproducible implementation and raw data.

The original file is not deleted or rewritten. It is the historical record
of the idea that started the project.
