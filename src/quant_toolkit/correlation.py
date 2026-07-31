from __future__ import annotations

import numpy as np
import pandas as pd


def factor_correlation_matrix(
    panel: pd.DataFrame,
    factor_cols: list[str],
    date_col: str = "date",
    method: str = "spearman",
) -> pd.DataFrame:
    if method not in {"spearman", "pearson"}:
        raise ValueError("method must be 'spearman' or 'pearson'")
    if len(factor_cols) < 2:
        raise ValueError("at least two factor columns are required")

    required = {date_col, *factor_cols}
    missing = sorted(required.difference(panel.columns))
    if missing:
        raise ValueError(f"missing required columns: {missing}")

    matrices = []
    for _, group in panel.groupby(date_col, sort=False):
        usable = group[factor_cols].replace([np.inf, -np.inf], np.nan).dropna()
        if len(usable) >= 3:
            matrices.append(usable.corr(method=method))

    if not matrices:
        raise ValueError("no date has enough complete observations for correlation")
    return sum(matrices) / len(matrices)


def find_redundant_factor_pairs(correlation: pd.DataFrame, threshold: float = 0.8) -> list[dict[str, float | str]]:
    if not 0 <= threshold <= 1:
        raise ValueError("threshold must be in [0, 1]")

    factors = list(correlation.columns)
    pairs: list[dict[str, float | str]] = []
    for left_index, left in enumerate(factors):
        for right in factors[left_index + 1 :]:
            corr = correlation.loc[left, right]
            if pd.notna(corr) and abs(float(corr)) >= threshold:
                pairs.append({"left": left, "right": right, "correlation": float(corr)})
    return pairs
