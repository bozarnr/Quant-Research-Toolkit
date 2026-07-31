from __future__ import annotations

import unittest

import pandas as pd

from quant_toolkit.demo import make_synthetic_panel
from quant_toolkit.splits import apply_split, build_walk_forward_splits


class WalkForwardSplitTest(unittest.TestCase):
    def test_builds_ordered_non_overlapping_test_windows(self) -> None:
        panel = make_synthetic_panel(days=18, assets=3)
        splits = build_walk_forward_splits(panel["date"], train_window=8, test_window=3)

        self.assertEqual(len(splits), 3)
        self.assertLess(splits[0].train_end, splits[0].test_start)
        self.assertLess(splits[0].test_end, splits[1].test_start)

    def test_apply_split_returns_train_and_test_panels(self) -> None:
        panel = make_synthetic_panel(days=12, assets=2)
        split = build_walk_forward_splits(panel["date"], train_window=6, test_window=2)[0]

        train, test = apply_split(panel, split)

        self.assertEqual(train["date"].nunique(), 6)
        self.assertEqual(test["date"].nunique(), 2)
        self.assertLess(pd.to_datetime(train["date"]).max(), pd.to_datetime(test["date"]).min())

    def test_rejects_bad_windows(self) -> None:
        with self.assertRaises(ValueError):
            build_walk_forward_splits(["2026-01-01"], train_window=0, test_window=1)


if __name__ == "__main__":
    unittest.main()
