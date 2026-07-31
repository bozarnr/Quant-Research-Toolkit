from __future__ import annotations

from dataclasses import dataclass
from typing import Iterable

import pandas as pd


@dataclass(frozen=True)
class DataManifest:
    source: str
    created_at: str
    rows: int
    columns: tuple[str, ...]
    date_col: str
    asset_col: str
    known_limits: tuple[str, ...] = ()

    @classmethod
    def from_panel(
        cls,
        panel: pd.DataFrame,
        source: str,
        date_col: str = "date",
        asset_col: str = "asset",
        known_limits: Iterable[str] = (),
    ) -> "DataManifest":
        missing = [col for col in (date_col, asset_col) if col not in panel.columns]
        if missing:
            raise ValueError(f"missing manifest identity columns: {missing}")
        return cls(
            source=source,
            created_at=pd.Timestamp.utcnow().isoformat(),
            rows=int(len(panel)),
            columns=tuple(str(col) for col in panel.columns),
            date_col=date_col,
            asset_col=asset_col,
            known_limits=tuple(known_limits),
        )

    def to_dict(self) -> dict[str, object]:
        return {
            "source": self.source,
            "created_at": self.created_at,
            "rows": self.rows,
            "columns": list(self.columns),
            "date_col": self.date_col,
            "asset_col": self.asset_col,
            "known_limits": list(self.known_limits),
        }
