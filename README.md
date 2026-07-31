# Quant Research Toolkit

Clean-room utilities for time-safe factor research. This repository is a public,
educational slice of a broader quant-research workflow: it keeps the parts that
are useful to inspect on GitHub while excluding employer code, private data,
credentials, and raw experiment logs.

## Public Research Stack

This repository is one part of a public AI-quant portfolio:

- [AI Alpha Research Lab](https://github.com/bozarnr/eee): formula-alpha research with strict promotion gates.
- [Paper Alpha Replications](https://github.com/bozarnr/paper-library): evidence-first paper replication ledger.
- [Quant Research Toolkit](https://github.com/bozarnr/experiment): reusable time-safe factor diagnostics.
- [Strategy Game Agents](https://github.com/bozarnr/behavioral-finance-experiment): behavioral experiment tooling plus strategy-agent simulation.

## What it shows

- Market-panel validation: sorted `date`/`asset` panels, required columns, and
  explicit feature/label separation.
- Leakage guardrails: labels and future-looking fields cannot enter the feature
  set.
- First-pass factor diagnostics: cross-sectional Rank IC, coverage, turnover,
  and top-quantile gross/net return.
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
from quant_toolkit.metrics import evaluate_factor
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
```

## 中文说明

这是一个公开版量化研究工具包，目标不是展示“我有一个神奇策略”，而是展示：

- 我理解时间安全、标签泄漏、样本外验证、交易成本这些基本约束。
- 我能把研究流程压成可测试、可复用的工程模块。
- 我会诚实区分 `demo_smoke_test`、`validated_candidate` 和真实可交易结果。

当前版本只包含合成数据演示，不包含任何私有数据、雇主代码、实盘结果或可交易承诺。

## Evidence Boundary

See [evidence/validation-boundary.md](evidence/validation-boundary.md). The
current repository is a public toolkit foundation, not a production backtest.
