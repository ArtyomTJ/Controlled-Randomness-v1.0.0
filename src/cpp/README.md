# C++ reference implementation

`controlled_randomness.cpp` is a C++17, dependency-free port of the
original algorithm with a control arm.

## Build

```bash
g++ -std=c++17 -O2 -Wall -Wextra -o cr controlled_randomness.cpp
```

## Run

```bash
./cr --self-test
./cr --arm both --target 17 19 --trials 10000
./cr --arm control --target 17 19 --trials 10000
./cr --arm select --target 17 19 --trials 10000
./cr --arm both --target 17 19 --trials 10000 --out results.csv
```

Options:

| Option | Meaning |
|---|---|
| `--arm both` | Paired control/selection runs with identical seeds (default) |
| `--arm control` | Control arm only |
| `--arm select` | Selection arm only |
| `--target C D` | Target pair |
| `--trials N` | Number of trials |
| `--seed S` | First seed; trial `t` uses `S + t` |
| `--lo L`, `--hi H` | Alphabet bounds |
| `--out FILE` | Write per-trial CSV |
| `--self-test` | Run built-in checks and exit |

The built-in self-test checks the MSVC `rand()` compatibility, the
selection-rule cases, and the paired equality on a small alphabet. It is run
in CI.

## Expected result

For any seed, the paired arms stop at the same iteration. The summary line
`mismatches=` should be 0. The mean and SD should be close to the geometric
prediction for the chosen target and alphabet.
