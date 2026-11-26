#!/usr/bin/env python3
"""Run the v1.0 paired null experiment and write the result artefacts.

Usage:
    python experiments/run_v1.py

The script uses only the Python standard library. It writes:
    experiments/results/v1_paired_<c>_<d>.csv
    experiments/results/v1_summary.json
"""
from __future__ import annotations

import csv
import json
import sys
import time
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src" / "python"))

from crlab.experiment import paired_trials  # noqa: E402
from crlab.stats import summarize, theoretical_mean, theoretical_sd  # noqa: E402

TARGETS = [(17, 19), (-13, -7)]
TRIALS = 10_000
SEED0 = 1_000_003
LO, HI = -20, 20


def main() -> int:
    out_dir = ROOT / "experiments" / "results"
    out_dir.mkdir(parents=True, exist_ok=True)

    summary = {
        "version": "1.0.0",
        "lo": LO,
        "hi": HI,
        "trials_per_target": TRIALS,
        "seed0": SEED0,
        "targets": [],
    }

    for c, d in TARGETS:
        target = (c, d)
        rows: list[tuple] = []
        control_values: list[int] = []
        select_values: list[int] = []
        mismatches = 0
        started = time.time()

        for trial, seed, control, selection in paired_trials(
            SEED0, target, TRIALS, LO, HI
        ):
            control_values.append(control.iterations)
            select_values.append(selection.iterations)
            if control.iterations != selection.iterations:
                mismatches += 1
            rows.append(
                (
                    trial,
                    seed,
                    c,
                    d,
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
                    c,
                    d,
                    "select",
                    selection.iterations,
                    selection.final_x,
                    selection.final_y,
                )
            )

        elapsed = time.time() - started
        csv_path = out_dir / f"v1_paired_{c}_{d}.csv"
        with csv_path.open("w", newline="", encoding="utf-8") as handle:
            writer = csv.writer(handle)
            writer.writerow(
                [
                    "trial",
                    "seed",
                    "target_c",
                    "target_d",
                    "arm",
                    "iterations",
                    "final_x",
                    "final_y",
                ]
            )
            writer.writerows(rows)

        entry = {
            "target": [c, d],
            "trials_per_arm": TRIALS,
            "mismatches": mismatches,
            "control": summarize(control_values),
            "select": summarize(select_values),
            "theory": {
                "mean": theoretical_mean(target, LO, HI, "msvc"),
                "sd": theoretical_sd(target, LO, HI, "msvc"),
            },
            "elapsed_seconds": round(elapsed, 2),
            "csv": str(csv_path.relative_to(ROOT)),
        }
        summary["targets"].append(entry)

        print(
            f"target={target} trials={TRIALS} mismatches={mismatches} "
            f"mean={entry['control']['mean']:.1f} sd={entry['control']['sd']:.1f} "
            f"min={entry['control']['min']} max={entry['control']['max']} "
            f"theory_mean={entry['theory']['mean']:.1f} elapsed={elapsed:.1f}s"
        )

    summary_path = out_dir / "v1_summary.json"
    summary_path.write_text(json.dumps(summary, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    print(f"wrote {summary_path.relative_to(ROOT)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
