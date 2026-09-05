# Prediction Market Arbitrage

Research scaffold for finding complete-set mispricing in binary prediction markets.

## Pipeline

`venue adapters → contract normalization → order-book snapshot → gross edge → fees/slippage/latency → size → paper execution`

The included `prediction_market_arbitrage.py` keeps **detection separate from execution**. A price discrepancy is not treated as an opportunity until estimated trading costs are removed and both books have enough depth.

## Extend this branch

1. Add authenticated venue adapters under `quant_lab/adapters/`.
2. Normalize equivalent contracts into one `event_key` before comparing them.
3. Replace flat slippage with depth-aware VWAP from the order book.
4. Log every detected opportunity, including the ones that disappear before execution.
5. Backtest against recorded order-book snapshots rather than candle data.

## Existing project reuse

This branch is intended to absorb the useful pieces of the user's existing Polymarket / PolyEdge projects rather than replace them with a toy clone. Preserve any existing tests, venue-specific parsing and realistic cost logic that are already stronger than this scaffold.

## Safety

Educational research only. Prediction-market access, eligibility and trading rules vary by jurisdiction and venue.
