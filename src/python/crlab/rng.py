"""Random sources for the Controlled Randomness experiments."""
from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path


class MsvcRand:
    """A bit-compatible reimplementation of MSVC's ``rand()``/``srand()``.

    ``RAND_MAX`` is 32767. The original project was built with
    MSVC-compatible semantics, so this class is used for the reference
    experiment. It is a deterministic PRNG and is **not** suitable for
    cryptography.
    """

    __slots__ = ("_state",)

    def __init__(self, seed: int) -> None:
        self._state = seed & 0xFFFFFFFF

    def next(self) -> int:
        self._state = (self._state * 214013 + 2531011) & 0xFFFFFFFF
        return (self._state >> 16) & 0x7FFF

    def pair(self, lo: int = -20, hi: int = 20) -> tuple[int, int]:
        span = hi - lo + 1
        if span < 1:
            raise ValueError("hi must be >= lo")
        return self.next() % span + lo, self.next() % span + lo


@dataclass
class MsvcSource:
    """A seedable pair source backed by :class:`MsvcRand`."""

    seed: int
    lo: int = -20
    hi: int = 20

    def __post_init__(self) -> None:
        if self.hi < self.lo:
            raise ValueError("hi must be >= lo")
        self._rng = MsvcRand(self.seed)

    def pair(self) -> tuple[int, int]:
        return self._rng.pair(self.lo, self.hi)


class EntropyExhausted(RuntimeError):
    """Raised when a file-backed entropy stream runs out of values."""


@dataclass
class FileEntropy:
    """A pair source backed by a text file with one integer per line.

    Lines starting with ``#`` and blank lines are ignored. Values must lie
    in ``[lo, hi]``. The stream is consumed sequentially and never wrapped:
    reusing entropy would silently correlate trials.
    """

    path: Path | str
    lo: int = -20
    hi: int = 20

    def __post_init__(self) -> None:
        if self.hi < self.lo:
            raise ValueError("hi must be >= lo")
        self._values: list[int] = []
        with Path(self.path).open("r", encoding="utf-8") as handle:
            for lineno, raw in enumerate(handle, start=1):
                line = raw.strip()
                if not line or line.startswith("#"):
                    continue
                try:
                    value = int(line)
                except ValueError as exc:
                    raise ValueError(f"{self.path}:{lineno}: not an integer") from exc
                if not self.lo <= value <= self.hi:
                    raise ValueError(
                        f"{self.path}:{lineno}: {value} outside [{self.lo}, {self.hi}]"
                    )
                self._values.append(value)
        self._index = 0

    def pair(self) -> tuple[int, int]:
        if self._index + 1 >= len(self._values):
            raise EntropyExhausted(
                f"entropy stream exhausted after {self._index} values"
            )
        a = self._values[self._index]
        b = self._values[self._index + 1]
        self._index += 2
        return a, b
