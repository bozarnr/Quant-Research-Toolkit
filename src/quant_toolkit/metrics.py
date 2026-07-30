from __future__ import annotations

from dataclasses import dataclass

import numpy as np
import pandas as pd


@dataclass(frozen=True)
class FactorDiagnostics:
    observations: int
    dates: int
    coverage: float
    mean_rank_ic: float
    rank_ic_ir: float
    positive_rank_ic_rate: float
    mean_turnover: float
    top_quantile_gross_return: float
    top_quantile_net_return: float

    def verdict(self, min_dates: int = 20, min_rank_ic: float = 0.02, min_net_return: float = 0.0) -> str:
        if self.dates < min_dates:
            return "insufficient_sample"
        if self.mean_rank_ic < min_rank_ic:
            return "reject_low_rank_ic"
        if self.top_quantile_net_return <= min_net_return:
            return "reject_cost_adjusted_return"
        return "diagnosed_candidate"

    def to_frame(self) -> pd.DataFrame:
        return pd.DataFrame([self.__dict__])


def _rank_ic_by_date(panel: pd.DataFrame, factor_col: str, label_col: str, date_col: str) -> pd.Series:
    def corr(group: pd.DataFrame) -> float:
        valid = group[[factor_col, label_col]].dropna()
        if len(valid) < 3:
            return np.nan
        return valid[factor_col].rank().corr(valid[label_col].rank())

    return panel.groupby(date_col, sort=False).apply(corr, include_groups=False).dropna()


def _turnover_by_date(panel: pd.DataFrame, factor_col: str, date_col: str, asset_col: str, quantile: float) -> pd.Series:
    holdings: list[set[str]] = []
    for _, group in panel.groupby(date_col, sort=False):
        valid = group[[asset_col, factor_col]].dropna()
        if valid.empty:
            holdings.append(set())
            continue
        cutoff = valid[factor_col].quantile(1.0 - quantile)
        holdings.append(set(valid.loc[valid[factor_col] >= cutoff, asset_col].astype(str)))

    turnovers = []
    for previous, current in zip(holdings, holdings[1:]):
        if not previous and not current:
            turnovers.append(0.0)
        elif not previous:
            turnovers.append(1.0)
        else:
            turnovers.append(len(previous.symmetric_difference(current)) / max(len(previous | current), 1))
    return pd.Series(turnovers, dtype=float)


def evaluate_factor(
    panel: pd.DataFrame,
    factor_col: str,
    label_col: str = "label_ret_1d",
    date_col: str = "date",
    asset_col: str = "asset",
    top_quantile: float = 0.2,
    transaction_cost_bps: float = 0.0,
) -> FactorDiagnostics:
    if not 0 < top_quantile <= 0.5:
        raise ValueError("top_quantile must be in (0, 0.5]")
    if transaction_cost_bps < 0:
        raise ValueError("transaction_cost_bps cannot be negative")

    required = {date_col, asset_col, factor_col, label_col}
    missing = sorted(required.difference(panel.columns))
    if missing:
        raise ValueError(f"missing required columns: {missing}")

    usable = panel[[date_col, asset_col, factor_col, label_col]].dropna(subset=[factor_col, label_col])
    observations = len(usable)
    total_rows = max(len(panel), 1)
    coverage = observations / total_rows

    rank_ic = _rank_ic_by_date(usable, factor_col, label_col, date_col)
    mean_rank_ic = float(rank_ic.mean()) if len(rank_ic) else np.nan
    rank_ic_ir = float(rank_ic.mean() / rank_ic.std(ddof=1)) if len(rank_ic) > 1 and rank_ic.std(ddof=1) else np.nan
    positive_rate = float((rank_ic > 0).mean()) if len(rank_ic) else np.nan

    turnover = _turnover_by_date(usable, factor_col, date_col, asset_col, top_quantile)
    mean_turnover = float(turnover.mean()) if len(turnover) else 0.0

    top_returns = []
    for _, group in usable.groupby(date_col, sort=False):
        cutoff = group[factor_col].quantile(1.0 - top_quantile)
        selected = group.loc[group[factor_col] >= cutoff, label_col]
        if not selected.empty:
            top_returns.append(float(selected.mean()))
    gross = float(np.mean(top_returns)) if top_returns else np.nan
    cost = mean_turnover * transaction_cost_bps / 10000.0
    net = gross - cost if np.isfinite(gross) else np.nan

    return FactorDiagnostics(
        observations=observations,
        dates=int(usable[date_col].nunique()),
        coverage=float(coverage),
        mean_rank_ic=mean_rank_ic,
        rank_ic_ir=rank_ic_ir,
        positive_rank_ic_rate=positive_rate,
        mean_turnover=mean_turnover,
        top_quantile_gross_return=gross,
        top_quantile_net_return=float(net),
    )
