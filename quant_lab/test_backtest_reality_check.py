import unittest

from backtest_reality_check import (
    deflated_sharpe_probability,
    expected_max_sharpe,
    probabilistic_sharpe_ratio,
)


class BacktestRealityCheckTests(unittest.TestCase):
    def test_psr_is_probability(self):
        p = probabilistic_sharpe_ratio(1.0, 0.0, 252)
        self.assertGreaterEqual(p, 0.0)
        self.assertLessEqual(p, 1.0)

    def test_expected_max_exceeds_mean_for_varied_trials(self):
        srs = [-0.3, -0.1, 0.0, 0.2, 0.4]
        self.assertGreater(expected_max_sharpe(srs), sum(srs) / len(srs))

    def test_deflated_probability_is_probability(self):
        srs = [i / 100 for i in range(-20, 81)]
        _, p = deflated_sharpe_probability(max(srs), srs, 504)
        self.assertGreaterEqual(p, 0.0)
        self.assertLessEqual(p, 1.0)


if __name__ == "__main__":
    unittest.main()
