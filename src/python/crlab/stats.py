"""Small dependency-free statistics helpers for v1.0."""
from __future__ import annotations

import math
from statistics import mean, stdev


def value_prob_msvc(v: int, lo: int, hi: int) -> float:
    """Probability of one value from ``rand() % span + lo``.

    ``rand()`` returns 0..32767. When the span does not divide 32768, the
    low residues occur ``base + 1`` times and the rest ``base`` times.
    """
    span = hi - lo + 1
    if span < 1:
        raise ValueError("hi must be >= lo")
    residue = v - lo
    if not 0 <= residue < span:
        raise ValueError(f"{v} outside [{lo}, {hi}]")
    base, rem = divmod(32768, span)
    return (base + (1 if residue < rem else 0)) / 32768.0


def target_prob(
    target: tuple[int, int], lo: int = -20, hi: int = 20, source: str = "msvc"
) -> float:
    """Probability that one draw equals ``target``."""
    if source == "uniform":
        span = hi - lo + 1
        return 1.0 / (span * span)
    if source == "msvc":
        return value_prob_msvc(target[0], lo, hi) * value_prob_msvc(target[1], lo, hi)
    raise ValueError("source must be 'msvc' or 'uniform'")


def theoretical_mean(
    target: tuple[int, int], lo: int = -20, hi: int = 20, source: str = "msvc"
) -> float:
    return 1.0 / target_prob(target, lo, hi, source)


def theoretical_sd(
    target: tuple[int, int], lo: int = -20, hi: int = 20, source: str = "msvc"
) -> float:
    p = target_prob(target, lo, hi, source)
    return math.sqrt((1.0 - p) / (p * p))


def summarize(values: list[int]) -> dict[str, float | int]:
    """Return count, mean, sample SD, min and max."""
    n = len(values)
    if n == 0:
        raise ValueError("cannot summarize an empty sequence")
    return {
        "n": n,
        "mean": mean(values),
        "sd": stdev(values) if n > 1 else 0.0,
        "min": min(values),
        "max": max(values),
    }
