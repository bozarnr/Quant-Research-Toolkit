# Example Diagnostics

This public demo is intentionally synthetic. It shows the research workflow shape without exposing employer data, private alpha formulas, or tradable production signals.

## Current Capability

- `MarketPanelContract` validates a point-in-time market panel and rejects obvious leakage fields.
- `FactorRegistry` records factor lineage, input fields, and point-in-time rules.
- `evaluate_factor` reports rank IC, turnover, gross return, net return, and a rejection verdict when costs overwhelm the demo signal.
- `DataManifest` records dataset shape, identity columns, and known limitations for reproducible handoff.
- `build_walk_forward_splits` and `apply_split` create rolling train/test windows with strict train-before-test ordering.

## Why It Matters

The useful signal for recruiters is not that the synthetic factor is profitable. The useful signal is that the project treats alpha work as a research system: data contract first, leakage checks first, walk-forward evaluation first, and rejection reasons preserved instead of hidden.
