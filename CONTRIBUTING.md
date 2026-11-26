# Contributing

## Before you open a pull request

- Open an issue for anything larger than a typo or a small docs fix.
- Keep the scientific claims separate from the software changes. A new
  experiment needs a preregistration, not only a code change.
- Do not add a result to the README without a reproducible script and the
  raw data.

## Reproducibility rules

- Every experiment must be runnable from a clean checkout with a documented
  command.
- Fix seeds, versions, and sample sizes.
- Commit raw data and the script that produced the summary.
- If a result changes, update the changelog and the relevant doc.

## Code

- Python: standard library only for the core; optional analysis dependencies
  go in `pyproject.toml`.
- C++: C++17, no external dependencies.
- Run the tests before submitting:

```bash
cd src/python
python -m unittest discover -s tests -v
python -m crlab selftest
```

```bash
g++ -std=c++17 -O2 -Wall -Wextra -o cr src/cpp/controlled_randomness.cpp
./cr --self-test
```

## Tone

- No hype. State what was measured, on what source, with what sample size.
- Report negative results. They are results.
- Distinguish "not tested" from "tested and rejected".
- If you cite a claim, give a source.

## Data and ethics

- Do not upload personal data.
- Human-subjects work needs ethics approval before data collection.
- Do not make medical claims.
