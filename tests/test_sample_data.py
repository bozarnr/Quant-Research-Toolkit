import unittest

import pandas as pd

from quant_toolkit.contracts import MarketPanelContract


class SampleDataTests(unittest.TestCase):
    def test_market_panel_sample_matches_contract(self):
        panel = pd.read_csv("sample_data/market_panel_sample.csv", parse_dates=["date"])
        contract = MarketPanelContract(feature_cols=["momentum_5d", "reversal_5d", "quality", "size", "volatility"])

        contract.validate(panel)

        self.assertEqual(len(panel), 9)
        self.assertIn("label_ret_1d", panel.columns)


if __name__ == "__main__":
    unittest.main()
