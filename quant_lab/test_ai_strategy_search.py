import unittest

from ai_strategy_search import Candidate, parameter_grid, search


class AIStrategySearchTests(unittest.TestCase):
    def test_grid_size(self):
        rows = parameter_grid("x", {"a": [1, 2], "b": [10, 20, 30]})
        self.assertEqual(len(rows), 6)

    def test_search_ranks(self):
        candidates = [Candidate("x", {"v": 1}), Candidate("x", {"v": 2})]

        def bt(c, regime):
            base = float(c.params["v"])
            return base if regime == "a" else base - 0.1

        ranked = search(candidates, ["a", "b"], bt)
        self.assertEqual(ranked[0].candidate.params["v"], 2)


if __name__ == "__main__":
    unittest.main()
