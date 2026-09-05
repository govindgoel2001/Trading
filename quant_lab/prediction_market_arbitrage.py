"""AI Quant Lab — prediction market arbitrage scaffold.

Educational research code. This module deliberately separates detection from
execution so costs, liquidity and latency can be modelled before a trade is
considered executable.
"""

from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class Quote:
    venue: str
    event_key: str
    outcome: str
    ask: float
    bid: float | None = None
    depth_usd: float = 0.0


@dataclass(frozen=True)
class Opportunity:
    event_key: str
    buy_yes_venue: str
    buy_no_venue: str
    gross_edge: float
    estimated_costs: float
    net_edge: float
    max_notional: float


def single_venue_edge(yes_ask: float, no_ask: float) -> float:
    """Theoretical same-venue edge before fees/slippage."""
    return 1.0 - (yes_ask + no_ask)


def cross_venue_edge(yes_ask: float, no_ask: float) -> float:
    """Theoretical cross-venue complete-set edge before costs."""
    return 1.0 - (yes_ask + no_ask)


def estimate_costs(*, fees: float, slippage: float, latency_buffer: float) -> float:
    return max(0.0, fees) + max(0.0, slippage) + max(0.0, latency_buffer)


def kelly_fraction(win_probability: float, payout_multiple: float) -> float:
    """Binary Kelly fraction, clipped to [0, 1].

    payout_multiple is net profit per $1 risked when the position wins.
    """
    if payout_multiple <= 0:
        return 0.0
    p = min(max(win_probability, 0.0), 1.0)
    q = 1.0 - p
    raw = (payout_multiple * p - q) / payout_multiple
    return min(max(raw, 0.0), 1.0)


def evaluate_pair(
    yes_quote: Quote,
    no_quote: Quote,
    *,
    fees: float = 0.0,
    slippage: float = 0.0,
    latency_buffer: float = 0.0,
) -> Opportunity | None:
    if yes_quote.event_key != no_quote.event_key:
        return None
    gross = cross_venue_edge(yes_quote.ask, no_quote.ask)
    costs = estimate_costs(fees=fees, slippage=slippage, latency_buffer=latency_buffer)
    net = gross - costs
    if net <= 0:
        return None
    return Opportunity(
        event_key=yes_quote.event_key,
        buy_yes_venue=yes_quote.venue,
        buy_no_venue=no_quote.venue,
        gross_edge=gross,
        estimated_costs=costs,
        net_edge=net,
        max_notional=min(yes_quote.depth_usd, no_quote.depth_usd),
    )


if __name__ == "__main__":
    polymarket_yes = Quote("Polymarket", "demo-election", "YES", ask=0.55, depth_usd=5000)
    kalshi_no = Quote("Kalshi", "demo-election", "NO", ask=0.40, depth_usd=3000)
    print(evaluate_pair(polymarket_yes, kalshi_no, fees=0.01, slippage=0.01, latency_buffer=0.005))
