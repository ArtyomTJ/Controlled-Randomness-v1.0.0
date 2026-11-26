# Results — v1.0

## 1. What was run

The paired experiment in [`../experiments/run_v1.py`](../experiments/run_v1.py)
was run on the reference Python implementation:

- Source: MSVC-compatible `rand()%41-20` (the generator used by the
  original project on MSVC). The exact absolute values depend on the
  generator; the paired equality does not. If the original was built with
  GCC, the numbers shift slightly, but the conclusion is the same.
- Alphabet: $\{-20,\ldots,20\}$.
- Targets: $(17,19)$ and $(-13,-7)$.
- 10,000 paired trials per target (20,000 paired comparisons in total).
- Seeds: $1{,}000{,}003 + t$ for trial $t$.
- Both arms use the same seed for each trial.

Command:

```bash
python experiments/run_v1.py
```

The script writes the raw CSVs and `experiments/results/v1_summary.json`.

## 2. Results

| Target | Trials per arm | Mismatches | Mean $T$ | SD | Min | Max | Theory mean | Theory SD |
|---|---:|---:|---:|---:|---:|---:|---:|---:|
| $(17,19)$ | 10,000 | **0** | 1702.6 | 1720.8 | 1 | 16,535 | 1681.9 | 1681.4 |
| $(-13,-7)$ | 10,000 | **0** | 1667.4 | 1681.8 | 1 | 15,896 | 1679.8 | 1679.3 |

The mean and SD of the selection arm are identical to the control arm in
every row, because the per-trial iterations are identical. The table
therefore reports one mean and one SD for both arms.

**Mismatches:** 0 out of 20,000 paired comparisons. Not "on average zero" —
zero in every pair. For each seed, the two arms stop at exactly the same
iteration.

**Agreement with theory:** the sample means differ from the theoretical
means by 20.7 and 12.4 iterations, with a standard error of about 17. Both
are within sampling error. The SDs are also consistent with the geometric
prediction.

**Spread:** within a single target, $T$ ranges from 1 to 16,535. The
distribution is heavy-tailed; a single pair of runs can differ by a factor
of thousands with no effect present. This is why the v1.0 design uses
paired trials and thousands of replications.

## 3. Interpretation

### What this establishes

The deterministic selection rule does not change the waiting time in the
reference architecture. This is not an empirical coincidence; it follows
from the causal-isolation theorem in [`MATH.md`](MATH.md). The experiment
confirms the implementation.

H1 — "the selection rule itself biases the source" — is **falsified** for
this architecture.

### What this does not establish

It does **not** test H2 — the claim that a conscious observer can bias a
live physical source. The reference program has:

- a deterministic classical PRNG, not a live physical source;
- no human observer in the loop;
- no channel from the selection variables to the source or the stopping
  predicate.

The protocol in [`PROTOCOL.md`](PROTOCOL.md) specifies the H2 experiment.
Until that experiment is run, H2 is open.

### Why the null result is a result

A null result with a proof and a clean experiment is more informative than
a positive result without one. It tells the next experiment exactly what
must change: the source must be live, the observer must be real, and the
intention must be an input that can correlate with the source. The v1.0
program cannot provide any of these, so it cannot be used as evidence for
H2 in either direction.

## 4. Reproducibility

- Python: 3.14.8, standard library only.
- C++: C++17, no dependencies; compiled locally with Clang 22 (Zig 0.17.1)
  and self-tested; CI builds it with g++.
- Raw data: `experiments/results/v1_paired_*.csv` (two files).
- Summary: `experiments/results/v1_summary.json`.
- Runtime on the reference machine: about 39 s per target.
- The experiment is deterministic: the same seeds produce the same rows.

## 5. What would change the conclusion

For H1: a single paired mismatch would indicate a bug or a violation of
the causal-isolation assumption. None was observed.

For H2: a preregistered, powered experiment on a live source, with a
human-target arm faster than the machine-target arm beyond the sampling
error, replicated independently. That experiment has not been run.
