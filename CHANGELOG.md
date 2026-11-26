# Changelog

All notable changes to this project are documented here. The format follows
[Keep a Changelog](https://keepachangelog.com/en/1.1.0/) and the project uses
[Semantic Versioning](https://semver.org/).

## [1.0.0] — 2026-11-26

### Added

- Formal model of selection and waiting time.
- Causal-isolation theorem: for a fixed seed, the selection and control arms
  stop at the same iteration.
- Reference implementation in Python 3 (standard library only) and C++17
  (no dependencies), with a built-in self-test.
- Paired v1.0 experiment: 10,000 trials per target, two targets, identical
  seeds in both arms.
- Raw result files (`experiments/results/`) and a summary JSON.
- Preregistered protocol for the observer hypothesis (H2), including sample
  size, blinding, sequential monitoring, and data management.
- Documentation: hypothesis, mathematics, protocol, results, legacy, FAQ.
- CI workflow: Python unit tests and C++ build/self-test.

### Results

- 20,000 paired comparisons; 0 mismatches.
- Mean waiting time and SD consistent with the geometric distribution
  ($p \approx 1/1681$).
- H1 falsified for the reference architecture. H2 remains open.
