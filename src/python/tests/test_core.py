"""Unit tests for the reference implementation."""
from __future__ import annotations

import tempfile
import unittest
from pathlib import Path

from crlab.experiment import apply_selection, run_trial
from crlab.rng import EntropyExhausted, FileEntropy, MsvcRand, MsvcSource
from crlab.stats import summarize, target_prob, value_prob_msvc


class TestMsvcRand(unittest.TestCase):
    def test_first_value_matches_msvc(self) -> None:
        self.assertEqual(MsvcRand(1).next(), 41)

    def test_output_is_15_bit(self) -> None:
        rng = MsvcRand(12345)
        for _ in range(1000):
            value = rng.next()
            self.assertGreaterEqual(value, 0)
            self.assertLessEqual(value, 32767)

    def test_pair_is_in_range(self) -> None:
        rng = MsvcRand(7)
        for _ in range(1000):
            a, b = rng.pair(-20, 20)
            self.assertTrue(-20 <= a <= 20)
            self.assertTrue(-20 <= b <= 20)


class TestSelectionRule(unittest.TestCase):
    def check(self, args, expected) -> None:
        self.assertEqual(apply_selection(*args), expected)

    def test_rule_1_new_positive_replaces_negative(self) -> None:
        self.check((-5, -5, 3, 4, 10, 12), (3, 4))

    def test_rule_2_new_mixed_replaces_negative(self) -> None:
        self.check((-5, -5, -3, 4, 10, 12), (-3, 4))

    def test_rule_3_new_positive_replaces_mixed(self) -> None:
        self.check((-5, 5, 3, 4, 10, 12), (3, 4))

    def test_rule_4_new_mixed_replaces_mixed(self) -> None:
        self.check((3, -4, -5, 6, 10, 12), (-5, 6))

    def test_rule_6_closer_positive_is_taken(self) -> None:
        self.check((3, 4, 5, 6, 10, 12), (5, 6))

    def test_rule_6_farther_positive_is_rejected(self) -> None:
        self.check((5, 6, 3, 4, 10, 12), (5, 6))

    def test_negative_target_rule_1(self) -> None:
        self.check((5, 5, -3, -4, -10, -12), (-3, -4))

    def test_negative_target_rule_6(self) -> None:
        self.check((-3, -4, -5, -6, -10, -12), (-5, -6))

    def test_zero_current_is_replaced(self) -> None:
        self.check((0, 5, -3, 4, 10, 12), (-3, 4))


class _ListSource:
    def __init__(self, pairs: list[tuple[int, int]]):
        self._pairs = iter(pairs)

    def pair(self) -> tuple[int, int]:
        return next(self._pairs)


class TestTrial(unittest.TestCase):
    def test_control_ignores_selection(self) -> None:
        source = _ListSource([(1, 1), (1, 2)])
        result = run_trial(source, (1, 2), "control")
        self.assertEqual(result.iterations, 2)
        self.assertEqual((result.final_x, result.final_y), (1, 1))

    def test_selection_updates_auxiliary_pair(self) -> None:
        source = _ListSource([(1, 1), (1, 2)])
        result = run_trial(source, (1, 2), "select")
        self.assertEqual(result.iterations, 2)
        self.assertEqual((result.final_x, result.final_y), (1, 2))

    def test_same_seed_same_iterations(self) -> None:
        target = (3, 4)
        for seed in range(200):
            control = run_trial(MsvcSource(seed, -5, 5), target, "control")
            selection = run_trial(MsvcSource(seed, -5, 5), target, "select")
            self.assertEqual(control.iterations, selection.iterations)


class TestStats(unittest.TestCase):
    def test_msvc_value_probabilities_sum_to_one(self) -> None:
        total = sum(value_prob_msvc(v, -20, 20) for v in range(-20, 21))
        self.assertAlmostEqual(total, 1.0, places=12)

    def test_target_prob_matches_theory(self) -> None:
        p = target_prob((17, 19), -20, 20, "msvc")
        self.assertAlmostEqual(p, (799 / 32768) ** 2, places=12)

    def test_summarize(self) -> None:
        stats = summarize([1, 2, 3, 4])
        self.assertEqual(stats["n"], 4)
        self.assertAlmostEqual(stats["mean"], 2.5)
        self.assertEqual(stats["min"], 1)
        self.assertEqual(stats["max"], 4)


class TestFileEntropy(unittest.TestCase):
    def test_reads_pairs_and_exhausts(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / "entropy.txt"
            path.write_text("# test stream\n1\n2\n-3\n4\n", encoding="utf-8")
            source = FileEntropy(path, -20, 20)
            self.assertEqual(source.pair(), (1, 2))
            self.assertEqual(source.pair(), (-3, 4))
            with self.assertRaises(EntropyExhausted):
                source.pair()

    def test_rejects_out_of_range(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / "bad.txt"
            path.write_text("1\n99\n", encoding="utf-8")
            with self.assertRaises(ValueError):
                FileEntropy(path, -20, 20)


if __name__ == "__main__":
    unittest.main()
