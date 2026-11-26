# Controlled Randomness

**Can selection — or observation — bias a random process?**

Version **1.0.0** · reference implementation · formal model · paired null experiment · preregistered protocol

---

> If the effect is real, it must survive a protocol that rules out noise,
> bias, and selective reporting. This repository is that protocol.

## The question

A random source produces pairs of integers. A target pair is fixed in
advance. The process stops when the target appears. Two strategies:

- **Control:** accept every draw.
- **Selection:** keep the pair that is "closer" to the target according to a
  fixed rule.

Does the selection strategy change the waiting time?

**Scope.** This is not a classroom exercise. It is a research program built
to produce a result that would survive adversarial review. The first release
deliberately spends its effort on the hardest part: making the claim
falsifiable.

In a classical RNG the answer is **no**, and v1.0 proves it: the selection
rule updates only auxiliary variables and never touches the generator or the
stopping condition. The proof is in [`docs/MATH.md`](docs/MATH.md); the
experiment is in [`docs/RESULTS-v1.md`](docs/RESULTS-v1.md).

The original hypothesis has a stronger form: a **conscious observer** can
bias a physical random source without a known channel. That claim is not
tested by the original program — it cannot be, because the observer has no
causal path. v1.0 specifies the experiment that can test it.

## Three hypotheses

| ID | Hypothesis | Status in v1.0 |
|---|---|---|
| **H0** | The source is classical and independent of the selection rule. The waiting time is geometric. | Baseline; confirmed for the reference implementation |
| **H1** | A deterministic selection rule biases the source without feedback. | **Falsified** for the reference implementation: $T_{\text{sel}} \equiv T_{\text{ctrl}}$ pathwise |
| **H2** | A conscious observer's intention biases a live physical source. | **Open**; protocol specified, not yet run |

## Key result

For every seed, the selection arm and the control arm execute the **same**
sequence of draws and stop at the **same** iteration:

$$T_{\text{sel}}(s) = T_{\text{ctrl}}(s).$$

In **20,000 paired comparisons** (10,000 per target, two targets) the number
of mismatches was **0**. The waiting time is geometric with
$p \approx 1/1681$, $\mathbb{E}T \approx 1681$, $\sigma_T \approx 1681$.

This is not a failed experiment. It is a successful falsification of H1 —
and the reason H2 needs a different design.

**Verification:** Python unit tests 20/20 pass; the C++ self-test passes
(Clang 22); the paired experiment reports 0 mismatches in 20,000
comparisons.

## Quick start

### Python (standard library only)

```bash
cd src/python
python -m unittest discover -s tests -v
python -m crlab selftest
python -m crlab paired --target 17 19 --trials 2000
```

### C++17 (no dependencies)

```bash
g++ -std=c++17 -O2 -Wall -Wextra -o cr src/cpp/controlled_randomness.cpp
./cr --self-test
./cr --arm both --target 17 19 --trials 2000
```

### Reproduce the v1.0 result

```bash
python experiments/run_v1.py
```

This writes `experiments/results/v1_paired_*.csv` and
`experiments/results/v1_summary.json`.

## Repository map

```
docs/           hypothesis, math, protocol, results, legacy, FAQ
src/python/     reference implementation + unit tests
src/cpp/        C++17 port with a built-in self-test
legacy/         the original program, preserved
experiments/    v1.0 run script and raw results
paper/          research note draft
.github/        CI: Python tests and C++ build
```

## The protocol in one page

H2 is tested with a **live** entropy source, not a prerecorded file. In each
trial:

1. A target is chosen either by the participant (human arm) or by a
   verifiable random process (machine arm).
2. The machine draws pairs from the live source and applies the same
   selection rule.
3. The waiting time $T$ is recorded.
4. The primary test compares the human-target and machine-target
   distributions.

Under H0 both arms have the same distribution. Under H2 the human-target arm
is faster. The full protocol, including sample size and stopping rules, is
in [`docs/PROTOCOL.md`](docs/PROTOCOL.md).

## What would count as evidence

Not a single lucky run. A positive result must be:

- preregistered;
- adequately powered for a stated effect size;
- run on a live physical source;
- blinded where possible;
- replicated by an independent group;
- reported with an effect size and a confidence interval, not only a
  p-value.

A result that survives this would be extraordinary. A result that does not
is noise.

## Why this matters

If H2 is true, it is the first reproducible anomaly linking intention to
physical randomness, and it changes the boundary between mind and matter.
If H2 is false, the project still delivers a rigorous instrument, a clean
negative result, and a cautionary tale about why random streaks feel
meaningful.

Either outcome is worth publishing.

## Status

- **v1.0.0** — this release: formal model, reference implementation, paired
  null experiment, preregistered protocol.
- **v1.1** — live QRNG adapter and human-target CLI.
- **v1.2** — first confirmatory dataset.
- **v2.0** — independent replication.

## Citation

See [`CITATION.cff`](CITATION.cff).

## License

Code: MIT. Documentation and paper: CC BY 4.0. See
[`LICENSING.md`](LICENSING.md).
