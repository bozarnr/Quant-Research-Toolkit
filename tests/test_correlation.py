import unittest

import numpy as np
import pandas as pd

from quant_toolkit.correlation import factor_correlation_matrix, find_redundant_factor_pairs


class CorrelationTests(unittest.TestCase):
    def test_redundant_factor_pair_is_flagged(self):
        rng = np.random.default_rng(11)
        rows = []
        for date in pd.date_range("2025-01-01", periods=5):
            base = rng.normal(size=30)
            for idx in range(30):
                rows.append(
                    {
                        "date": date,
                        "asset": f"A{idx}",
                        "momentum": base[idx],
                        "momentum_clone": base[idx] + rng.normal(scale=0.01),
                        "quality": rng.normal(),
                    }
                )
        panel = pd.DataFrame(rows)

        corr = factor_correlation_matrix(panel, ["momentum", "momentum_clone", "quality"])
        pairs = find_redundant_factor_pairs(corr, threshold=0.95)

        self.assertEqual(len(pairs), 1)
        self.assertEqual(pairs[0]["left"], "momentum")
        self.assertEqual(pairs[0]["right"], "momentum_clone")
        self.assertGreater(pairs[0]["correlation"], 0.95)

    def test_requires_multiple_factors(self):
        panel = pd.DataFrame({"date": ["2025-01-01"], "factor": [1.0]})
        with self.assertRaises(ValueError):
            factor_correlation_matrix(panel, ["factor"])


if __name__ == "__main__":
    unittest.main()
