import unittest

from quant_toolkit.demo import make_synthetic_panel
from quant_toolkit.metrics import evaluate_factor


class FactorMetricsTest(unittest.TestCase):
    def test_cost_reduces_net_return(self) -> None:
        panel = make_synthetic_panel(days=25, assets=12)
        no_cost = evaluate_factor(panel, "momentum_5d", transaction_cost_bps=0)
        with_cost = evaluate_factor(panel, "momentum_5d", transaction_cost_bps=30)
        self.assertLess(with_cost.top_quantile_net_return, no_cost.top_quantile_net_return)

    def test_rank_ic_is_finite_on_demo_panel(self) -> None:
        panel = make_synthetic_panel(days=25, assets=12)
        diagnostics = evaluate_factor(panel, "momentum_5d")
        self.assertEqual(diagnostics.dates, 25)
        self.assertGreater(diagnostics.observations, 0)
        self.assertEqual(diagnostics.coverage, 1.0)


if __name__ == "__main__":
    unittest.main()
