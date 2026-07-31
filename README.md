# Quant Research Toolkit

Small utilities for checking factor-research data before any result is allowed to sound impressive. The package focuses on panel contracts, leakage checks, Rank IC, turnover, and cost-aware top-quantile return.

这个仓库放的是公开版工具层：先确认数据和诊断口径，再谈研究结论。当前 demo 只用合成数据，不包含私有数据、雇主代码、实盘结果或可交易承诺。

## Related repos

- [AI-Alpha-Research-Lab](https://github.com/bozarnr/AI-Alpha-Research-Lab): formula search, evaluation, and rejection gates.
- [Paper-Alpha-Replications](https://github.com/bozarnr/Paper-Alpha-Replications): replication notes with claim ceilings.
- [Quant-Research-Toolkit](https://github.com/bozarnr/Quant-Research-Toolkit): reusable checks for factor panels and diagnostics.
- [Strategy-Game-Agents](https://github.com/bozarnr/Strategy-Game-Agents): repeated-choice experiments and baseline agents.

## What is here

- Market-panel validation: sorted `date`/`asset`, required columns, and feature/label separation.
- Leakage guardrails: labels and future-looking fields cannot enter the feature set.
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
from quant_toolkit.contracts import MarketPanelContract
from quant_toolkit.metrics import evaluate_factor

contract = MarketPanelContract(feature_cols=["momentum_5d"])
contract.validate(panel)

diagnostics = evaluate_factor(
    panel,
    factor_col="momentum_5d",
    label_col="label_ret_1d",
    date_col="date",
    asset_col="asset",
    transaction_cost_bps=30,
)
```

## Evidence boundary

See [evidence/validation-boundary.md](evidence/validation-boundary.md). This is a toolkit foundation, not a production backtest.
