import unittest

import numpy as np
import pandas as pd

from quant_toolkit.neutralization import diagnose_neutralization, neutralize_cross_section


class NeutralizationTests(unittest.TestCase):
    def test_neutralization_reduces_exposure_correlation(self):
        rng = np.random.default_rng(7)
        rows = []
        for date in pd.date_range("2025-01-01", periods=8):
            size = rng.normal(size=40)
            value = 2.5 * size + rng.normal(scale=0.2, size=40)
            for idx in range(40):
                rows.append({"date": date, "asset": f"A{idx}", "factor": value[idx], "size": size[idx]})
        panel = pd.DataFrame(rows)

        panel["factor_neutralized"] = neutralize_cross_section(panel, "factor", ["size"])
        diagnostics = diagnose_neutralization(panel, "factor", ["size"], neutralized_col="factor_neutralized")

        self.assertEqual(diagnostics.observations_before, 320)
        self.assertEqual(diagnostics.observations_after, 320)
        self.assertTrue(diagnostics.improved())
        self.assertLess(diagnostics.mean_abs_exposure_corr_after, 0.05)

    def test_missing_exposure_column_raises(self):
        panel = pd.DataFrame({"date": ["2025-01-01"], "factor": [1.0]})
        with self.assertRaises(ValueError):
            neutralize_cross_section(panel, "factor", ["missing"])


if __name__ == "__main__":
    unittest.main()
