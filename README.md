# Quant Research Toolkit

Small utilities for checking factor-research data before any result is allowed to sound impressive. The package focuses on panel contracts, leakage checks, walk-forward splits, dataset manifests, Rank IC, turnover, and cost-aware top-quantile return.

## Showcase

- [Example Diagnostics Report](reports/example-diagnostics.md): a compact demo with Rank IC, turnover, gross return, net return, rejection verdict, walk-forward split checks, and data manifest boundaries.

## Related repos

- [AI-Alpha-Research-Lab](https://github.com/bozarnr/AI-Alpha-Research-Lab): formula search, evaluation, and rejection gates.
- [Paper-Alpha-Replications](https://github.com/bozarnr/Paper-Alpha-Replications): replication notes with claim ceilings.
- [Quant-Research-Toolkit](https://github.com/bozarnr/Quant-Research-Toolkit): reusable checks for factor panels and diagnostics.
- [Strategy-Game-Agents](https://github.com/bozarnr/Strategy-Game-Agents): repeated-choice experiments and baseline agents.

## What is here

- Market-panel validation: sorted `date`/`asset`, required columns, and feature/label separation.
- Leakage guardrails: labels and future-looking fields cannot enter the feature set.
- Walk-forward evaluation helpers: strict train-before-test windows and panel slicing.
- Data manifest helper: source, row count, columns, identity fields, and known limitations.
- First-pass diagnostics: Rank IC, coverage, turnover, and top-quantile gross/net return.
- Factor registry metadata: family, input fields, point-in-time rule, and status.
- Deterministic synthetic demo with a conservative verdict.

## Run

```powershell
python -m pip install -e .
python -m quant_toolkit.demo
python -m unittest discover -s tests -v
```

## Minimal API

```python
from quant_toolkit import (
    DataManifest,
    MarketPanelContract,
    build_walk_forward_splits,
    apply_split,
    evaluate_factor,
)

contract = MarketPanelContract(feature_cols=["momentum_5d"])
contract.validate(panel)

manifest = DataManifest.from_panel(panel, source="synthetic-public-demo")
split = build_walk_forward_splits(panel["date"], train_window=20, test_window=5)[0]
train, test = apply_split(panel, split)

diagnostics = evaluate_factor(
    test,
    factor_col="momentum_5d",
    label_col="label_ret_1d",
    date_col="date",
    asset_col="asset",
    transaction_cost_bps=30,
)
```

## Evidence boundary

See [evidence/validation-boundary.md](evidence/validation-boundary.md). This is a toolkit foundation, not a production backtest.
