import unittest
import os
from evolution.evaluation.performance_analyzer import PerformanceAnalyzer
from evolution.experiments.experiment_runner import ExperimentRunner
from evolution.proposals.improvement_generator import ImprovementGenerator

class TestGenesisEvolution(unittest.TestCase):
    def test_performance_analysis(self):
        pa = PerformanceAnalyzer()
        res = pa.analyze_execution({"agent": "coding", "evaluation_score": 0.85, "latency_ms": 2500})
        self.assertTrue(res["requires_optimization"])
        self.assertEqual(len(res["weaknesses"]), 2)

    def test_experiment_runner(self):
        runner = ExperimentRunner()
        exp = runner.run_benchmark_experiment("opt_coding_prompt_v2", 0.85)
        self.assertEqual(exp["outcome"], "PASSED")
        self.assertGreater(exp["candidate_score"], 0.85)

    def test_report_generation(self):
        gen = ImprovementGenerator(doc_dir="tests/evolution_test_docs")
        report = gen.create_report(
            title="Coding Agent Optimization",
            analysis={"agent": "coding", "weaknesses": ["Low score"]},
            experiment={"baseline_score": 0.85, "candidate_score": 0.90, "improvement": 0.05, "outcome": "PASSED"}
        )
        self.assertTrue(os.path.exists(report))

if __name__ == "__main__":
    unittest.main()
