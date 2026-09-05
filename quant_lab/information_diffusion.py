"""AI Quant Lab — information diffusion / Hawkes-style event-response scaffold.

The goal is to model how timestamped information events excite subsequent price
moves and how much of the observed activity is exogenous versus self-exciting.
This is research code, not a production estimator.
"""

from __future__ import annotations

from dataclasses import dataclass
from math import exp, log
from typing import Iterable, Sequence


@dataclass(frozen=True)
class Event:
    timestamp: float
    stream: str  # e.g. "news" or "price"
    magnitude: float = 1.0


def exponential_kernel(dt: float, alpha: float, beta: float) -> float:
    if dt <= 0:
        return 0.0
    return alpha * exp(-beta * dt)


def intensity(
    t: float,
    history: Iterable[Event],
    *,
    baseline: float,
    alpha_by_pair: dict[tuple[str, str], float],
    beta_by_pair: dict[tuple[str, str], float],
    target_stream: str,
) -> float:
    value = baseline
    for event in history:
        if event.timestamp >= t:
            continue
        pair = (event.stream, target_stream)
        alpha = alpha_by_pair.get(pair, 0.0)
        beta = beta_by_pair.get(pair, 1.0)
        value += event.magnitude * exponential_kernel(t - event.timestamp, alpha, beta)
    return max(value, 0.0)


def half_life(beta: float) -> float:
    if beta <= 0:
        raise ValueError("beta must be positive")
    return log(2.0) / beta


def event_windows(
    news_times: Sequence[float],
    price_times: Sequence[float],
    *,
    horizon: float,
) -> list[dict[str, float]]:
    """Create simple event windows for later estimation/visualization."""
    rows: list[dict[str, float]] = []
    for n in news_times:
        following = [p for p in price_times if n <= p <= n + horizon]
        rows.append(
            {
                "news_time": n,
                "first_price_event": min(following) if following else float("nan"),
                "price_events_in_window": float(len(following)),
            }
        )
    return rows


if __name__ == "__main__":
    history = [
        Event(0.0, "news"),
        Event(0.6, "price"),
        Event(1.0, "price"),
    ]
    a = {("news", "price"): 0.8, ("price", "price"): 0.25}
    b = {("news", "price"): 1.2, ("price", "price"): 2.0}
    print("price intensity:", intensity(1.4, history, baseline=0.05, alpha_by_pair=a, beta_by_pair=b, target_stream="price"))
    print("news→price half-life:", half_life(b[("news", "price")]))
