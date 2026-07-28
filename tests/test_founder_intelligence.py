import unittest
import os
from founder_intelligence.market_scanner.trend_detector import TrendDetector
from founder_intelligence.idea_engine.idea_generator import IdeaGenerator
from founder_intelligence.investor_engine.investor_score import InvestorEngine

class TestFounderIntelligence(unittest.TestCase):
    def test_trend_detector(self):
        td = TrendDetector()
        trends = td.scan_market_trends()
        self.assertGreater(len(trends), 0)
        report = td.save_trend_report(output_dir="tests/test_trends")
        self.assertTrue(os.path.exists(report))

    def test_idea_generator_benchmark(self):
        ig = IdeaGenerator()
        ideas = ig.generate_startup_ideas("Find 10 AI startup opportunities for 2026")
        self.assertEqual(len(ideas), 10)
        path = ig.save_candidates(ideas, output_dir="tests/test_candidates")
        self.assertTrue(os.path.exists(path))

    def test_investor_review(self):
        inv = InvestorEngine()
        path = inv.evaluate_and_pitch("AI Healthcare Agent", 88.5, output_dir="tests/test_reviews")
        self.assertTrue(os.path.exists(path))

if __name__ == "__main__":
    unittest.main()
