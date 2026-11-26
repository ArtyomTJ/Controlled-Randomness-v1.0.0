# Experiments

## v1.0 — paired null experiment

```bash
python experiments/run_v1.py
```

- Targets: $(17,19)$ and $(-13,-7)$.
- Alphabet: $\{-20,\ldots,20\}$.
- 10,000 paired trials per target.
- Seeds: $1{,}000{,}003 + t$.
- Runtime: about 39 s per target on the reference machine.

Outputs:

```
experiments/results/v1_paired_17_19.csv
experiments/results/v1_paired_-13_-7.csv
experiments/results/v1_summary.json
```

The result is reported in [`../docs/RESULTS-v1.md`](../docs/RESULTS-v1.md):
0 mismatches in 20,000 paired comparisons.

## What these experiments can and cannot test

The included source is a deterministic classical PRNG. The experiments test
the algorithmic claim (H1) and the implementation, not the observer claim
(H2). H2 needs a live physical source and a human participant; see
[`../docs/PROTOCOL.md`](../docs/PROTOCOL.md).

## File-backed entropy

`crlab.rng.FileEntropy` reads one integer per line, ignores blank lines and
`#` comments, and refuses to wrap the stream. It is useful for replaying a
recorded source, but it is **not** suitable for the confirmatory H2 test: a
prerecorded stream cannot react to an observer.

## Data policy

- Commit raw data and the script that produced the summary.
- Do not edit a result file by hand; rerun the script.
- Record the software version, the seed, and the source metadata.
