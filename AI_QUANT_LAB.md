# AI × Quant Lab

One repository, four branch-based builds.

| Branch | Project | Purpose |
|---|---|---|
| `prediction-market-arbitrage` | Prediction Market Arbitrage | Compare equivalent contracts across venues, subtract execution costs, and surface only net-positive opportunities. |
| `information-diffusion` | Information Diffusion Model | Convert timestamped information + price events into a Hawkes-style response model. |
| `ai-strategy-search` | AI Strategy Search Lab | Let AI generate structured strategy candidates, then test them across market regimes with a real backtest engine. |
| `backtest-reality-check` | Backtest Reality Check | Detect selection bias and lucky backtests using Probabilistic/Deflated-Sharpe-style diagnostics. |

## Use

```bash
git fetch --all
git switch prediction-market-arbitrage
```

Each branch contains its own `quant_lab/README.md` and starter implementation.

## Design rules

- AI proposes hypotheses; numerical validation stays explicit.
- Detection is separate from execution.
- Fees, spread, slippage, latency and liquidity belong in the model.
- Strategy search records every trial, not just winners.
- Holdout / walk-forward validation comes after search.
- Upstream open-source licenses and attribution are preserved.

Educational research only; not financial advice or a promise of profitability.
