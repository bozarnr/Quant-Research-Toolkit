# Disclosure Boundary

This repository is a public, clean-room slice of a quant research workflow.

## Included

- Synthetic sample data that shows expected table formats.
- Time-safe panel contracts, leakage checks, diagnostics, and tests.
- Documentation about validation boundaries and rejection criteria.

## Excluded

- Real trading signals, alpha formulas, production parameters, and execution logic.
- Raw experiment logs, vendor datasets, credentials, cookies, tokens, and account identifiers.
- Any claim that the sample data or demo output is tradable.

## Sample Data Rule

Files under `sample_data/` are tiny synthetic fixtures. They are designed to make schemas inspectable in GitHub and CI, not to represent a market edge.
