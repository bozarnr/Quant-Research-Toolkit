# Quant Research Toolkit

Clean-room utilities for time-safe factor research. This repository is a public,
educational slice of a broader quant-research workflow: it keeps the parts that
are useful to inspect on GitHub while excluding employer code, private data,
credentials, and raw experiment logs.

## What it shows

- Market-panel validation: sorted `date`/`asset` panels, required columns, and
  explicit feature/label separation.
- Leakage guardrails: labels and future-looking fields cannot enter the feature
  set.
- First-pass factor diagnostics: cross-sectional Rank IC, coverage, turnover,
  and top-quantile gross/net return.
- Exposure neutralization: per-date residualization against style/risk fields,
  with before/after exposure-correlation diagnostics.
- Factor family hygiene: average cross-sectional correlation matrices and
  redundant-pair flags for crowded factor families.
- Factor registry: small metadata contracts for point-in-time rules, family,
  data requirements, and status.
- Deterministic demo: synthetic data only, intended as a smoke test rather than
  evidence of a tradable strategy.

## Quick Start

```powershell
python -m pip install -e .
python -m quant_toolkit.demo
python -m unittest discover -s tests -v
```

Expected demo behavior: the toy signal produces a diagnostics table and a
conservative verdict. The verdict is deliberately bounded by cost-aware
performance and sample-size checks.

## Minimal API

```python
from quant_toolkit.contracts import MarketPanelContract
from quant_toolkit.correlation import factor_correlation_matrix, find_redundant_factor_pairs
from quant_toolkit.metrics import evaluate_factor
from quant_toolkit.neutralization import diagnose_neutralization, neutralize_cross_section
from quant_toolkit.registry import FactorRegistry, FactorSpec

contract = MarketPanelContract(
    date_col="date",
    asset_col="asset",
    label_col="label_ret_1d",
    feature_cols=["momentum_5d"],
)
contract.validate(panel)

diagnostics = evaluate_factor(
    panel,
    factor_col="momentum_5d",
    label_col="label_ret_1d",
    date_col="date",
    asset_col="asset",
    transaction_cost_bps=30,
)

panel["momentum_5d_neutralized"] = neutralize_cross_section(
    panel,
    value_col="momentum_5d",
    exposure_cols=["size", "volatility"],
)
neutralization_report = diagnose_neutralization(
    panel,
    value_col="momentum_5d",
    exposure_cols=["size", "volatility"],
    neutralized_col="momentum_5d_neutralized",
)

corr = factor_correlation_matrix(panel, ["momentum_5d", "reversal_5d", "quality"])
crowded_pairs = find_redundant_factor_pairs(corr, threshold=0.85)
```

## Evidence Boundary

See [evidence/validation-boundary.md](evidence/validation-boundary.md). The
current repository is a public toolkit foundation, not a production backtest.
