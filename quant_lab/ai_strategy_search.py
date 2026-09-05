"""AI Quant Lab — AI strategy search scaffold.

This module treats an LLM as a hypothesis generator, not an oracle. Strategy
candidates are represented as structured parameter sets, then evaluated by a
backtest function supplied by the user.
"""

from __future__ import annotations

from dataclasses import dataclass
from itertools import product
from statistics import mean, pstdev
from typing import Callable, Iterable


@dataclass(frozen=True)
class Candidate:
    family: str
    params: dict[str, float | int | str]


@dataclass(frozen=True)
class Evaluation:
    candidate: Candidate
    regime_scores: dict[str, float]
    mean_score: float
    score_stability: float
    worst_regime: float


def parameter_grid(family: str, grid: dict[str, list[float | int | str]]) -> list[Candidate]:
    keys = list(grid)
    out: list[Candidate] = []
    for values in product(*(grid[k] for k in keys)):
        out.append(Candidate(family=family, params=dict(zip(keys, values))))
    return out


def evaluate_candidate(
    candidate: Candidate,
    regimes: Iterable[str],
    backtest_fn: Callable[[Candidate, str], float],
) -> Evaluation:
    scores = {regime: float(backtest_fn(candidate, regime)) for regime in regimes}
    vals = list(scores.values())
    avg = mean(vals) if vals else float("nan")
    stability = pstdev(vals) if len(vals) > 1 else 0.0
    worst = min(vals) if vals else float("nan")
    return Evaluation(candidate, scores, avg, stability, worst)


def robust_rank(e: Evaluation, stability_penalty: float = 0.5) -> float:
    """Prefer candidates that are decent everywhere, not amazing once."""
    return e.mean_score + e.worst_regime - stability_penalty * e.score_stability


def search(
    candidates: Iterable[Candidate],
    regimes: Iterable[str],
    backtest_fn: Callable[[Candidate, str], float],
) -> list[Evaluation]:
    results = [evaluate_candidate(c, regimes, backtest_fn) for c in candidates]
    return sorted(results, key=robust_rank, reverse=True)


if __name__ == "__main__":
    # Demo only: replace with real historical backtests.
    def demo_backtest(c: Candidate, regime: str) -> float:
        fast = float(c.params["fast"])
        slow = float(c.params["slow"])
        base = (slow - fast) / max(slow, 1.0)
        adjustment = {"trend": 0.8, "range": -0.2, "high_vol": 0.1}[regime]
        return base + adjustment

    candidates = parameter_grid("ma_cross", {"fast": [5, 10, 20], "slow": [50, 100, 200]})
    ranked = search(candidates, ["trend", "range", "high_vol"], demo_backtest)
    for row in ranked[:5]:
        print(row)
