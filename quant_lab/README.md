# Backtest Reality Check

A selection-bias / overfitting diagnostic for the moment an AI strategy search produces hundreds or thousands of apparently good backtests.

## Why this exists

If you test enough strategy variants, **the best historical Sharpe will be biased upward even when there is little or no real edge**. This branch turns that into something measurable instead of hand-waving about overfitting.

The included script implements:

- Probabilistic Sharpe Ratio style inference;
- an extreme-value approximation for the Sharpe you would expect to see after many trials;
- a Deflated-Sharpe-style probability that the selected strategy beats that selection benchmark.

## Recommended workflow

`generate N strategies → record every trial → select candidate → compute return moments → DSR-style check → untouched holdout → walk-forward / paper test`

Do **not** calculate the correction using only the winners. The entire trial family matters.

## Upstream research/reference

- `stefan-jansen/machine-learning-for-trading` — MIT — contains multiple-testing and strategy-level overfitting material plus working research examples.
- Bailey & López de Prado, *The Deflated Sharpe Ratio: Correcting for Selection Bias, Backtest Overfitting and Non-Normality*.

The local implementation is intentionally compact and educational. For serious research, validate the formula, return-frequency assumptions and higher moments against a vetted implementation.
