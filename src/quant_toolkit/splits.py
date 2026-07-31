from __future__ import annotations

from dataclasses import dataclass
from typing import Iterable

import pandas as pd


@dataclass(frozen=True)
class WalkForwardSplit:
    """Index-window split with strict train-before-test ordering."""

    train_start: pd.Timestamp
    train_end: pd.Timestamp
    test_start: pd.Timestamp
    test_end: pd.Timestamp

    def __post_init__(self) -> None:
        if not self.train_start <= self.train_end < self.test_start <= self.test_end:
            raise ValueError("split dates must satisfy train_start <= train_end < test_start <= test_end")

    def as_dict(self) -> dict[str, str]:
        return {
            "train_start": self.train_start.date().isoformat(),
            "train_end": self.train_end.date().isoformat(),
            "test_start": self.test_start.date().isoformat(),
            "test_end": self.test_end.date().isoformat(),
        }


def build_walk_forward_splits(
    dates: Iterable[object],
    train_window: int,
    test_window: int,
    step: int | None = None,
) -> list[WalkForwardSplit]:
    if train_window <= 0 or test_window <= 0:
        raise ValueError("train_window and test_window must be positive")
    step = test_window if step is None else step
    if step <= 0:
        raise ValueError("step must be positive")

    unique_dates = pd.Index(pd.to_datetime(list(dates))).drop_duplicates().sort_values()
    splits: list[WalkForwardSplit] = []
    start = 0
    while start + train_window + test_window <= len(unique_dates):
        train_start = unique_dates[start]
        train_end = unique_dates[start + train_window - 1]
        test_start = unique_dates[start + train_window]
        test_end = unique_dates[start + train_window + test_window - 1]
        splits.append(WalkForwardSplit(train_start, train_end, test_start, test_end))
        start += step
    return splits


def apply_split(
    panel: pd.DataFrame,
    split: WalkForwardSplit,
    date_col: str = "date",
) -> tuple[pd.DataFrame, pd.DataFrame]:
    if date_col not in panel.columns:
        raise ValueError(f"missing date column: {date_col}")
    dates = pd.to_datetime(panel[date_col])
    train_mask = (dates >= split.train_start) & (dates <= split.train_end)
    test_mask = (dates >= split.test_start) & (dates <= split.test_end)
    return panel.loc[train_mask].copy(), panel.loc[test_mask].copy()
