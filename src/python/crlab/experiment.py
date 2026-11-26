"""Trial runner and the original selection rule."""
from __future__ import annotations

from dataclasses import dataclass
from typing import Protocol


class PairSource(Protocol):
    def pair(self) -> tuple[int, int]:
        """Return the next iid pair from the source."""


@dataclass(frozen=True)
class TrialResult:
    arm: str
    target: tuple[int, int]
    iterations: int
    final_x: int
    final_y: int


def apply_selection(
    x: int, y: int, a: int, b: int, c: int, d: int
) -> tuple[int, int]:
    """Apply the original selection rule.

    This is a line-by-line port of the rule in ``legacy/original.cpp``.
    The rule only updates the auxiliary pair ``(x, y)``. It does not touch
    the source and is not read by the stopping predicate.
    """
    if c > 0 and d > 0:
        if (
            (x < 0 and y < 0 and a > 0 and b > 0)
            or (x < 0 and y < 0 and ((a < 0 and b > 0) or (a > 0 and b < 0)))
            or (a > 0 and b > 0 and ((x < 0 and y > 0) or (x > 0 and y < 0)))
            or (
                ((x < 0 and y > 0) or (x > 0 and y < 0))
                and ((a < 0 and b > 0) or (a > 0 and b < 0))
            )
            or x == 0
            or y == 0
        ):
            x, y = a, b
        if (
            (x > 0 and y > 0 and a > 0 and b > 0)
            and (
                abs((c + d) / 2.0 - (x + y) / 2.0)
                > abs((c + d) / 2.0 - (a + b) / 2.0)
            )
        ):
            x, y = a, b
    else:
        if (
            (x > 0 and y > 0 and a < 0 and b < 0)
            or (x > 0 and y > 0 and ((a < 0 and b > 0) or (a > 0 and b < 0)))
            or (a < 0 and b < 0 and ((x < 0 and y > 0) or (x > 0 and y < 0)))
            or (
                ((x < 0 and y > 0) or (x > 0 and y < 0))
                and ((a < 0 and b > 0) or (a > 0 and b < 0))
            )
            or x == 0
            or y == 0
        ):
            x, y = a, b
        if (
            (x < 0 and y < 0 and a < 0 and b < 0)
            and (
                abs((abs(c) + abs(d)) / 2.0 - (abs(x) + abs(y)) / 2.0)
                > abs((abs(c) + abs(d)) / 2.0 - (abs(a) + abs(b)) / 2.0)
            )
        ):
            x, y = a, b
    return x, y


def run_trial(source: PairSource, target: tuple[int, int], arm: str) -> TrialResult:
    """Run one trial until the raw draw equals ``target``.

    ``arm`` is ``"control"`` (no selection) or ``"select"`` (update the
    auxiliary pair on every draw). The stopping predicate is identical in
    both arms: ``(a, b) == target``.
    """
    if arm not in ("control", "select"):
        raise ValueError("arm must be 'control' or 'select'")

    c, d = target
    a = b = x = y = 1
    iterations = 0

    while (a, b) != (c, d):
        a, b = source.pair()
        iterations += 1
        if arm == "select":
            x, y = apply_selection(x, y, a, b, c, d)

    return TrialResult(arm=arm, target=target, iterations=iterations, final_x=x, final_y=y)


def paired_trials(
    seed0: int,
    target: tuple[int, int],
    trials: int,
    lo: int = -20,
    hi: int = 20,
):
    """Yield paired control/selection trials with identical seeds."""
    from .rng import MsvcSource

    for t in range(trials):
        seed = (seed0 + t) & 0xFFFFFFFF
        control = run_trial(MsvcSource(seed, lo, hi), target, "control")
        select = run_trial(MsvcSource(seed, lo, hi), target, "select")
        yield t, seed, control, select
