"""Command-line interface for the reference implementation."""
from __future__ import annotations

import argparse
import csv
from pathlib import Path

from . import __version__
from .experiment import apply_selection, paired_trials, run_trial
from .rng import MsvcRand, MsvcSource
from .stats import summarize, theoretical_mean, theoretical_sd

CSV_HEADER = [
    "trial",
    "seed",
    "target_c",
    "target_d",
    "arm",
    "iterations",
    "final_x",
    "final_y",
]


def _write_csv(path: Path, rows: list[tuple]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.writer(handle)
        writer.writerow(CSV_HEADER)
        writer.writerows(rows)


def _print_summary(label: str, stats: dict, mean_theory: float, sd_theory: float) -> None:
    print(f"{label}:")
    print(f"  n={stats['n']}")
    print(f"  mean={stats['mean']:.1f}")
    print(f"  sd={stats['sd']:.1f}")
    print(f"  min={stats['min']} max={stats['max']}")
    print(f"  theoretical_mean={mean_theory:.1f}")
    print(f"  theoretical_sd={sd_theory:.1f}")


def cmd_paired(args: argparse.Namespace) -> int:
    target = (args.target[0], args.target[1])
    rows: list[tuple] = []
    control_values: list[int] = []
    select_values: list[int] = []
    mismatches = 0

    for trial, seed, control, selection in paired_trials(
        args.seed, target, args.trials, args.lo, args.hi
    ):
        control_values.append(control.iterations)
        select_values.append(selection.iterations)
        if control.iterations != selection.iterations:
            mismatches += 1
        rows.append(
            (
                trial,
                seed,
                target[0],
                target[1],
                "control",
                control.iterations,
                control.final_x,
                control.final_y,
            )
        )
        rows.append(
            (
                trial,
                seed,
                target[0],
                target[1],
                "select",
                selection.iterations,
                selection.final_x,
                selection.final_y,
            )
        )

    if args.out:
        _write_csv(args.out, rows)

    print(
        f"mode=paired target={target} trials={args.trials} "
        f"lo={args.lo} hi={args.hi} seed0={args.seed}"
    )
    print(f"mismatches={mismatches}")
    mean_theory = theoretical_mean(target, args.lo, args.hi, args.source)
    sd_theory = theoretical_sd(target, args.lo, args.hi, args.source)
    _print_summary("control", summarize(control_values), mean_theory, sd_theory)
    _print_summary("select", summarize(select_values), mean_theory, sd_theory)
    return 0


def cmd_run(args: argparse.Namespace) -> int:
    target = (args.target[0], args.target[1])
    values: list[int] = []
    rows: list[tuple] = []

    for trial in range(args.trials):
        seed = (args.seed + trial) & 0xFFFFFFFF
        result = run_trial(MsvcSource(seed, args.lo, args.hi), target, args.arm)
        values.append(result.iterations)
        rows.append(
            (
                trial,
                seed,
                target[0],
                target[1],
                result.arm,
                result.iterations,
                result.final_x,
                result.final_y,
            )
        )

    if args.out:
        _write_csv(args.out, rows)

    print(
        f"mode=run arm={args.arm} target={target} trials={args.trials} "
        f"lo={args.lo} hi={args.hi} seed0={args.seed}"
    )
    _print_summary(
        args.arm,
        summarize(values),
        theoretical_mean(target, args.lo, args.hi, args.source),
        theoretical_sd(target, args.lo, args.hi, args.source),
    )
    return 0


def cmd_selftest(args: argparse.Namespace) -> int:
    if MsvcRand(1).next() != 41:
        raise SystemExit("self-test failed: MSVC rand(1) != 41")

    cases = [
        ((-5, -5, 3, 4, 10, 12), (3, 4)),
        ((-5, 5, 3, 4, 10, 12), (3, 4)),
        ((3, 4, -5, 5, 10, 12), (3, 4)),
        ((3, 4, 5, 6, 10, 12), (5, 6)),
        ((5, 6, 3, 4, 10, 12), (5, 6)),
        ((5, 5, -3, -4, -10, -12), (-3, -4)),
        ((-3, -4, -5, -6, -10, -12), (-5, -6)),
        ((0, 5, -3, 4, 10, 12), (-3, 4)),
    ]
    for (x, y, a, b, c, d), expected in cases:
        got = apply_selection(x, y, a, b, c, d)
        if got != expected:
            raise SystemExit(
                f"self-test failed: apply_selection({x}, {y}, {a}, {b}, {c}, {d}) "
                f"= {got}, expected {expected}"
            )

    target = (3, 4)
    for seed in range(200):
        control = run_trial(MsvcSource(seed, -5, 5), target, "control")
        selection = run_trial(MsvcSource(seed, -5, 5), target, "select")
        if control.iterations != selection.iterations:
            raise SystemExit(
                f"self-test failed: paired mismatch at seed {seed}: "
                f"{control.iterations} != {selection.iterations}"
            )

    print("self-test OK")
    return 0


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="crlab",
        description="Controlled Randomness reference implementation",
    )
    parser.add_argument("--version", action="version", version=f"%(prog)s {__version__}")
    subparsers = parser.add_subparsers(dest="command", required=True)

    paired = subparsers.add_parser(
        "paired", help="run paired control/selection trials with identical seeds"
    )
    paired.add_argument("--target", nargs=2, type=int, metavar=("C", "D"), required=True)
    paired.add_argument("--trials", type=int, default=1000)
    paired.add_argument("--seed", type=int, default=1000003)
    paired.add_argument("--lo", type=int, default=-20)
    paired.add_argument("--hi", type=int, default=20)
    paired.add_argument("--source", choices=("msvc", "uniform"), default="msvc")
    paired.add_argument("--out", type=Path)
    paired.set_defaults(func=cmd_paired)

    run = subparsers.add_parser("run", help="run one arm")
    run.add_argument("--arm", choices=("control", "select"), required=True)
    run.add_argument("--target", nargs=2, type=int, metavar=("C", "D"), required=True)
    run.add_argument("--trials", type=int, default=1000)
    run.add_argument("--seed", type=int, default=1000003)
    run.add_argument("--lo", type=int, default=-20)
    run.add_argument("--hi", type=int, default=20)
    run.add_argument("--source", choices=("msvc", "uniform"), default="msvc")
    run.add_argument("--out", type=Path)
    run.set_defaults(func=cmd_run)

    selftest = subparsers.add_parser("selftest", help="run built-in checks")
    selftest.set_defaults(func=cmd_selftest)

    return parser


def main(argv: list[str] | None = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)

    if hasattr(args, "trials") and args.trials < 1:
        parser.error("--trials must be >= 1")
    if hasattr(args, "lo") and args.lo > args.hi:
        parser.error("--lo must be <= --hi")
    if hasattr(args, "target"):
        c, d = args.target
        if not (args.lo <= c <= args.hi and args.lo <= d <= args.hi):
            parser.error("--target values must lie inside [--lo, --hi]")

    return args.func(args)
