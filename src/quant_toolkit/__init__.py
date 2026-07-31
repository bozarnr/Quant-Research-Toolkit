"""Public clean-room quant research utilities."""

from .contracts import MarketPanelContract
from .correlation import factor_correlation_matrix, find_redundant_factor_pairs
from .manifest import DataManifest
from .metrics import FactorDiagnostics, evaluate_factor
from .neutralization import NeutralizationDiagnostics, diagnose_neutralization, neutralize_cross_section
from .registry import FactorRegistry, FactorSpec
from .splits import WalkForwardSplit, apply_split, build_walk_forward_splits

__all__ = [
    "DataManifest",
    "FactorDiagnostics",
    "FactorRegistry",
    "FactorSpec",
    "MarketPanelContract",
    "NeutralizationDiagnostics",
    "WalkForwardSplit",
    "apply_split",
    "build_walk_forward_splits",
    "diagnose_neutralization",
    "evaluate_factor",
    "factor_correlation_matrix",
    "find_redundant_factor_pairs",
    "neutralize_cross_section",
]
