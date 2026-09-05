# AI Strategy Search Lab

Use AI to generate **structured hypotheses**, then let a real backtest engine decide whether they survive.

## Core workflow

`idea generator → parameterized candidates → backtest engine → regime matrix → robustness score → holdout validation`

The included scaffold:

- expands strategy parameter grids;
- evaluates each candidate across multiple market regimes;
- penalizes instability rather than ranking only by the single best Sharpe-like score;
- keeps the LLM outside the numerical evaluation loop.

## Where to plug in your existing work

Reuse your existing portfolio-manager / hedge-fund strategy definitions and data loaders as candidate families. Replace the demo `backtest_fn` with your actual engine.

## Recommended backbone

- `stefan-jansen/machine-learning-for-trading` — MIT — broad ML-for-trading workflow, strategy simulation and diagnostics.
- `stefan-jansen/zipline-reloaded` — Apache-2.0 — event-driven backtesting.

A useful visual for this branch is a **strategy × market-regime heatmap**: rows are generated strategies, columns are trend/range/high-vol/low-vol/etc. The point is to see *where* a strategy works, not just whether one aggregate metric is high.

## Rule

Do not let the same data both generate and validate the hypothesis. Search on one period/universe, then validate on a genuinely untouched holdout.
