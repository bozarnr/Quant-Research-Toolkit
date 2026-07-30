from __future__ import annotations

import numpy as np
import pandas as pd

from .contracts import MarketPanelContract
from .metrics import evaluate_factor
from .registry import FactorRegistry, FactorSpec


def make_synthetic_panel(days: int = 40, assets: int = 30, seed: int = 7) -> pd.DataFrame:
    rng = np.random.default_rng(seed)
    dates = pd.date_range("2026-01-01", periods=days, freq="B")
    asset_ids = [f"A{i:03d}" for i in range(assets)]
    rows = []
    latent_quality = rng.normal(0, 1, size=assets)
    for day_idx, date in enumerate(dates):
        market_noise = rng.normal(0, 0.01)
        for asset_idx, asset in enumerate(asset_ids):
            seasonal = np.sin(day_idx / 6.0 + asset_idx / 5.0)
            momentum_5d = 0.55 * latent_quality[asset_idx] + 0.25 * seasonal + rng.normal(0, 0.45)
            label = 0.0007 * latent_quality[asset_idx] + 0.0003 * seasonal + market_noise + rng.normal(0, 0.012)
            rows.append(
                {
                    "date": date,
                    "asset": asset,
                    "close": 10 + asset_idx + rng.normal(0, 0.5),
                    "amount": 1_000_000 + rng.integers(0, 200_000),
                    "momentum_5d": momentum_5d,
                    "label_ret_1d": label,
                }
            )
    return pd.DataFrame(rows).sort_values(["date", "asset"]).reset_index(drop=True)


def main() -> None:
    panel = make_synthetic_panel()
    contract = MarketPanelContract(feature_cols=["momentum_5d"])
    contract.validate(panel)

    registry = FactorRegistry()
    registry.register(
        FactorSpec(
            factor_id="momentum_5d_demo",
            family="price_volume",
            description="Synthetic five-day momentum proxy for public smoke testing.",
            input_fields=("close", "amount"),
            point_in_time_rule="formed after t close; label starts from t+1",
            status="diagnosed",
        )
    )

    diagnostics = evaluate_factor(panel, "momentum_5d", transaction_cost_bps=30)
    print(diagnostics.to_frame().round(6).to_string(index=False))
    print(f"verdict={diagnostics.verdict()}")
    print(f"registered={registry.as_rows()[0]['factor_id']}")


if __name__ == "__main__":
    main()
