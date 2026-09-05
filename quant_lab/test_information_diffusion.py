import math
import unittest

from information_diffusion import Event, half_life, intensity


class InformationDiffusionTests(unittest.TestCase):
    def test_half_life(self):
        self.assertAlmostEqual(half_life(2.0), math.log(2.0) / 2.0)

    def test_news_raises_price_intensity(self):
        history = [Event(0.0, "news")]
        alpha = {("news", "price"): 0.8}
        beta = {("news", "price"): 1.0}
        baseline = 0.05
        self.assertGreater(
            intensity(0.5, history, baseline=baseline, alpha_by_pair=alpha, beta_by_pair=beta, target_stream="price"),
            baseline,
        )


if __name__ == "__main__":
    unittest.main()
