# Python reference implementation

The package is dependency-free (Python 3.10+) and contains:

- `crlab.rng` — MSVC-compatible PRNG, seedable source, file-backed entropy.
- `crlab.experiment` — trial runner and the original selection rule.
- `crlab.stats` — value probabilities, geometric theory, summary statistics.
- `crlab.cli` — command-line interface.

## Run without installing

```bash
cd src/python
python -m unittest discover -s tests -v
python -m crlab selftest
python -m crlab paired --target 17 19 --trials 2000
```

## Install (editable)

```bash
python -m pip install -e src/python
crlab --help
```

## Commands

```bash
crlab paired --target 17 19 --trials 10000 --out results.csv
crlab run --arm control --target 17 19 --trials 10000
crlab run --arm select --target 17 19 --trials 10000
crlab selftest
```

Use `--source uniform` for the theoretical probabilities of a uniform
source; the default `msvc` uses the exact modulo distribution of the
reference generator.

## Tests

The unit tests cover the RNG compatibility, the selection-rule cases, the
paired equality, the probability calculations, and the file-backed entropy
source. They run in CI on every push.
