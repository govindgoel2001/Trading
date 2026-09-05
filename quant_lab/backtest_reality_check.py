"""AI Quant Lab — backtest reality check.

Implements a compact Probabilistic Sharpe Ratio / Deflated Sharpe style
selection adjustment inspired by Bailey & Lopez de Prado. Use this as an
educational diagnostic, then compare against a vetted implementation before
making research decisions.
"""

from __future__ import annotations

from math import exp, sqrt
from statistics import NormalDist, mean, pstdev
from typing import Sequence


_NORMAL = NormalDist()
_EULER_GAMMA = 0.5772156649015329


def probabilistic_sharpe_ratio(
    observed_sr: float,
    benchmark_sr: float,
    n_returns: int,
    *,
    skewness: float = 0.0,
    kurtosis: float = 3.0,
) -> float:
    """Probability that observed Sharpe exceeds a benchmark.

    `kurtosis` is ordinary kurtosis (Normal = 3), not excess kurtosis.
    """
    if n_returns <= 1:
        raise ValueError("n_returns must be > 1")
    variance_term = 1.0 - skewness * observed_sr + ((kurtosis - 1.0) / 4.0) * observed_sr**2
    if variance_term <= 0:
        raise ValueError("invalid moment combination: variance term <= 0")
    z = (observed_sr - benchmark_sr) * sqrt(n_returns - 1) / sqrt(variance_term)
    return _NORMAL.cdf(z)


def expected_max_sharpe(sharpes: Sequence[float]) -> float:
    """Approximate expected maximum Sharpe after trying N variants.

    Uses the extreme-value approximation commonly paired with the Deflated
    Sharpe Ratio. At least two trial Sharpes are required.
    """
    n = len(sharpes)
    if n < 2:
        raise ValueError("need at least two trial Sharpes")
    mu = mean(sharpes)
    sigma = pstdev(sharpes)
    if sigma == 0:
        return mu

    z1 = _NORMAL.inv_cdf(1.0 - 1.0 / n)
    z2 = _NORMAL.inv_cdf(1.0 - 1.0 / (n * exp(1.0)))
    return mu + sigma * ((1.0 - _EULER_GAMMA) * z1 + _EULER_GAMMA * z2)


def deflated_sharpe_probability(
    selected_sr: float,
    all_trial_sharpes: Sequence[float],
    n_returns: int,
    *,
    skewness: float = 0.0,
    kurtosis: float = 3.0,
) -> tuple[float, float]:
    """Return (selection benchmark, probability selected SR beats it)."""
    benchmark = expected_max_sharpe(all_trial_sharpes)
    probability = probabilistic_sharpe_ratio(
        selected_sr,
        benchmark,
        n_returns,
        skewness=skewness,
        kurtosis=kurtosis,
    )
    return benchmark, probability


def verdict(probability: float, threshold: float = 0.95) -> str:
    return "SURVIVES" if probability >= threshold else "DOES NOT SURVIVE"


if __name__ == "__main__":
    # Pretend an AI searched 1,000 variants. In real research, pass the actual
    # trial distribution and the selected strategy's return moments.
    trial_srs = [-0.4 + (i % 80) * 0.012 for i in range(1000)]
    selected = max(trial_srs)
    benchmark, p = deflated_sharpe_probability(selected, trial_srs, 756)
    print(f"selected SR: {selected:.3f}")
    print(f"selection benchmark: {benchmark:.3f}")
    print(f"DSR-style probability: {p:.3%}")
    print(verdict(p))
