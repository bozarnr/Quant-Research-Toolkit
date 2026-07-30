from __future__ import annotations

from dataclasses import dataclass
from typing import Iterable

import pandas as pd


FORBIDDEN_FEATURE_PREFIXES = ("label_", "future_", "target_")


@dataclass(frozen=True)
class MarketPanelContract:
    """Minimal time-safe contract for a daily cross-sectional market panel."""

    date_col: str = "date"
    asset_col: str = "asset"
    label_col: str = "label_ret_1d"
    feature_cols: tuple[str, ...] = ()
    required_cols: tuple[str, ...] = ("close", "amount")

    def __init__(
        self,
        date_col: str = "date",
        asset_col: str = "asset",
        label_col: str = "label_ret_1d",
        feature_cols: Iterable[str] = (),
        required_cols: Iterable[str] = ("close", "amount"),
    ) -> None:
        object.__setattr__(self, "date_col", date_col)
        object.__setattr__(self, "asset_col", asset_col)
        object.__setattr__(self, "label_col", label_col)
        object.__setattr__(self, "feature_cols", tuple(feature_cols))
        object.__setattr__(self, "required_cols", tuple(required_cols))

    def validate(self, panel: pd.DataFrame) -> None:
        expected = {self.date_col, self.asset_col, self.label_col, *self.required_cols, *self.feature_cols}
        missing = sorted(expected.difference(panel.columns))
        if missing:
            raise ValueError(f"missing required columns: {missing}")

        leaking = [col for col in self.feature_cols if col == self.label_col or col.startswith(FORBIDDEN_FEATURE_PREFIXES)]
        if leaking:
            raise ValueError(f"feature columns include future/label fields: {leaking}")

        duplicated = panel.duplicated([self.date_col, self.asset_col])
        if duplicated.any():
            raise ValueError("panel contains duplicate date/asset rows")

        sorted_panel = panel.sort_values([self.date_col, self.asset_col]).index
        if not sorted_panel.equals(panel.index):
            raise ValueError("panel must be sorted by date and asset to preserve time order")

        if panel[self.label_col].notna().sum() == 0:
            raise ValueError("label column has no usable observations")

    def feature_view(self, panel: pd.DataFrame) -> pd.DataFrame:
        self.validate(panel)
        return panel[[self.date_col, self.asset_col, *self.feature_cols]].copy()
