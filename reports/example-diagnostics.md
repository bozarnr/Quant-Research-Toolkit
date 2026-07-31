# Example Diagnostics Report

This report is generated from the deterministic synthetic demo. It is a smoke-test artifact, not a backtest.

| Metric | Value | Read |
|---|---:|---|
| observations | 1200 | full synthetic panel used |
| dates | 40 | enough for a small pipeline smoke |
| coverage | 1.000000 | no missing factor/label rows in the demo |
| mean Rank IC | 0.062314 | weak positive rank relationship in synthetic data |
| Rank IC IR | 0.382932 | not enough to call robust |
| positive Rank IC rate | 0.625000 | more positive than negative days |
| mean turnover | 0.686991 | too high for a casual daily signal |
| top-quantile gross return | 0.000743 | positive before costs |
| top-quantile net return, 30 bps | -0.001318 | rejected after turnover costs |
| verdict | `reject_cost_adjusted_return` | correct conservative behavior |

## What this shows

The package does not stop at an IC number. It carries the result through coverage, turnover, transaction costs, and a simple verdict. The useful feature is not that the toy factor works; it is that the toolkit refuses to dress up a cost-eroded signal.

## Next useful artifact

The next version should add a public point-in-time sample dataset and a walk-forward split. That would move the repo from toolkit foundation to a small reproducible research example.
