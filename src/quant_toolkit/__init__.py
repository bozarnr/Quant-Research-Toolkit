"""Public clean-room quant research utilities."""

from .contracts import MarketPanelContract
from .manifest import DataManifest
from .metrics import FactorDiagnostics, evaluate_factor
from .registry import FactorRegistry, FactorSpec
from .splits import WalkForwardSplit, apply_split, build_walk_forward_splits

__all__ = [
    "DataManifest",
    "FactorDiagnostics",
    "FactorRegistry",
    "FactorSpec",
    "MarketPanelContract",
    "WalkForwardSplit",
    "apply_split",
    "build_walk_forward_splits",
    "evaluate_factor",
]
