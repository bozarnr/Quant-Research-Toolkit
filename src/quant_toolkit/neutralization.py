from __future__ import annotations

from dataclasses import dataclass

import numpy as np
import pandas as pd


@dataclass(frozen=True)
class NeutralizationDiagnostics:
    observations_before: int
    observations_after: int
    mean_abs_exposure_corr_before: float
    mean_abs_exposure_corr_after: float

    def improved(self) -> bool:
        return self.mean_abs_exposure_corr_after < self.mean_abs_exposure_corr_before


def neutralize_cross_section(
    panel: pd.DataFrame,
    value_col: str,
    exposure_cols: list[str],
    date_col: str = "date",
    min_obs: int | None = None,
    add_intercept: bool = True,
) -> pd.Series:
    """OLS-residualize a factor against exposures independently on each date."""
    if not exposure_cols:
        raise ValueError("exposure_cols cannot be empty")

    required = {date_col, value_col, *exposure_cols}
    missing = sorted(required.difference(panel.columns))
    if missing:
        raise ValueError(f"missing required columns: {missing}")

    minimum = min_obs or (len(exposure_cols) + int(add_intercept) + 1)
    residuals = pd.Series(np.nan, index=panel.index, dtype=float)

    for _, group in panel.groupby(date_col, sort=False):
        usable = group[[value_col, *exposure_cols]].replace([np.inf, -np.inf], np.nan).dropna()
        if len(usable) < minimum:
            continue

        y = usable[value_col].to_numpy(dtype=float)
        x = usable[exposure_cols].to_numpy(dtype=float)
        if add_intercept:
            x = np.column_stack([np.ones(len(x)), x])

        beta, *_ = np.linalg.lstsq(x, y, rcond=None)
        residuals.loc[usable.index] = y - x @ beta

    return residuals


def exposure_correlation_summary(
    panel: pd.DataFrame,
    value_col: str,
    exposure_cols: list[str],
    date_col: str = "date",
) -> float:
    required = {date_col, value_col, *exposure_cols}
    missing = sorted(required.difference(panel.columns))
    if missing:
        raise ValueError(f"missing required columns: {missing}")

    correlations: list[float] = []
    for _, group in panel.groupby(date_col, sort=False):
        usable = group[[value_col, *exposure_cols]].replace([np.inf, -np.inf], np.nan).dropna()
        if len(usable) < 3:
            continue
        for exposure in exposure_cols:
            corr = usable[value_col].corr(usable[exposure])
            if pd.notna(corr):
                correlations.append(abs(float(corr)))

    return float(np.mean(correlations)) if correlations else np.nan


def diagnose_neutralization(
    panel: pd.DataFrame,
    value_col: str,
    exposure_cols: list[str],
    date_col: str = "date",
    neutralized_col: str | None = None,
) -> NeutralizationDiagnostics:
    working = panel.copy()
    output_col = neutralized_col or f"{value_col}_neutralized"
    if output_col not in working:
        working[output_col] = neutralize_cross_section(working, value_col, exposure_cols, date_col=date_col)

    before_cols = working[[date_col, value_col, *exposure_cols]].dropna()
    after_cols = working[[date_col, output_col, *exposure_cols]].dropna()
    return NeutralizationDiagnostics(
        observations_before=int(len(before_cols)),
        observations_after=int(len(after_cols)),
        mean_abs_exposure_corr_before=exposure_correlation_summary(working, value_col, exposure_cols, date_col),
        mean_abs_exposure_corr_after=exposure_correlation_summary(
            working.rename(columns={output_col: "__neutralized_value"}),
            "__neutralized_value",
            exposure_cols,
            date_col,
        ),
    )
