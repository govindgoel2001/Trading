import unittest

from prediction_market_arbitrage import Quote, evaluate_pair, single_venue_edge


class PredictionMarketArbitrageTests(unittest.TestCase):
    def test_single_venue_edge(self):
        self.assertAlmostEqual(single_venue_edge(0.49, 0.48), 0.03)

    def test_costs_can_kill_apparent_edge(self):
        yes = Quote("A", "event", "YES", 0.50, depth_usd=1000)
        no = Quote("B", "event", "NO", 0.47, depth_usd=900)
        self.assertIsNone(evaluate_pair(yes, no, fees=0.02, slippage=0.01, latency_buffer=0.01))

    def test_positive_net_edge_survives(self):
        yes = Quote("A", "event", "YES", 0.50, depth_usd=1000)
        no = Quote("B", "event", "NO", 0.45, depth_usd=900)
        opp = evaluate_pair(yes, no, fees=0.01, slippage=0.01, latency_buffer=0.005)
        self.assertIsNotNone(opp)
        self.assertAlmostEqual(opp.net_edge, 0.025)
        self.assertEqual(opp.max_notional, 900)


if __name__ == "__main__":
    unittest.main()
