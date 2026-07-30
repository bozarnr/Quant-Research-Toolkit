import unittest

import pandas as pd

from quant_toolkit.contracts import MarketPanelContract


class MarketPanelContractTest(unittest.TestCase):
    def setUp(self) -> None:
        self.panel = pd.DataFrame(
            [
                {"date": pd.Timestamp("2026-01-01"), "asset": "A", "close": 1.0, "amount": 10.0, "alpha": 0.1, "label_ret_1d": 0.01},
                {"date": pd.Timestamp("2026-01-01"), "asset": "B", "close": 2.0, "amount": 20.0, "alpha": 0.2, "label_ret_1d": 0.02},
                {"date": pd.Timestamp("2026-01-02"), "asset": "A", "close": 1.1, "amount": 11.0, "alpha": 0.3, "label_ret_1d": 0.03},
            ]
        )

    def test_accepts_sorted_panel(self) -> None:
        MarketPanelContract(feature_cols=["alpha"]).validate(self.panel)

    def test_rejects_unsorted_panel(self) -> None:
        unsorted = self.panel.iloc[[1, 0, 2]].reset_index(drop=True)
        with self.assertRaisesRegex(ValueError, "sorted"):
            MarketPanelContract(feature_cols=["alpha"]).validate(unsorted)

    def test_rejects_label_as_feature(self) -> None:
        with self.assertRaisesRegex(ValueError, "future/label"):
            MarketPanelContract(feature_cols=["label_ret_1d"]).validate(self.panel)


if __name__ == "__main__":
    unittest.main()
