import os

repo_root = "c:\\Genesis_Harness"

# Directories
dirs = [
    "evolution/evaluation",
    "evolution/optimization",
    "evolution/experiments",
    "evolution/proposals",
    "docs/evolution",
    "tests"
]
for d in dirs:
    os.makedirs(os.path.join(repo_root, d), exist_ok=True)
    with open(os.path.join(repo_root, d, "__init__.py"), "w", encoding="utf-8") as f:
        f.write("# Genesis Evolution Module\n")

# 1. Performance Analyzer: evolution/evaluation/performance_analyzer.py
pa_code = '''from typing import Dict, Any, List

class PerformanceAnalyzer:
    def analyze_execution(self, execution_data: Dict[str, Any]) -> Dict[str, Any]:
        agent_name = execution_data.get("agent", "unknown")
        latency_ms = execution_data.get("latency_ms", 1200)
        score = execution_data.get("evaluation_score", 0.88)
        cost = execution_data.get("cost_usd", 0.02)

        weaknesses = []
        if score < 0.90:
            weaknesses.append(f"Low evaluation score ({score}) for agent {agent_name}")
        if latency_ms > 2000:
            weaknesses.append(f"High execution latency ({latency_ms}ms)")

        return {
            "agent": agent_name,
            "metrics": {"score": score, "latency_ms": latency_ms, "cost_usd": cost},
            "weaknesses": weaknesses,
            "requires_optimization": len(weaknesses) > 0
        }
'''
with open(os.path.join(repo_root, "evolution", "evaluation", "performance_analyzer.py"), "w", encoding="utf-8") as f:
    f.write(pa_code)

# 2. Optimizers: evolution/optimization/agent_optimizer.py, prompt_optimizer.py, skill_optimizer.py
with open(os.path.join(repo_root, "evolution", "optimization", "agent_optimizer.py"), "w", encoding="utf-8") as f:
    f.write('''class AgentOptimizer:\n    def optimize_agent(self, agent_name: str, weakness: str) -> dict:\n        return {"agent": agent_name, "proposal": f"Adjust charter rules for {agent_name} to address: {weakness}"}\n''')

with open(os.path.join(repo_root, "evolution", "optimization", "prompt_optimizer.py"), "w", encoding="utf-8") as f:
    f.write('''class PromptOptimizer:\n    def optimize_prompt(self, prompt_id: str) -> dict:\n        return {"prompt_id": prompt_id, "proposal": "Refine reasoning layer constraints"}\n''')

with open(os.path.join(repo_root, "evolution", "optimization", "skill_optimizer.py"), "w", encoding="utf-8") as f:
    f.write('''class SkillOptimizer:\n    def optimize_skill(self, skill_name: str) -> dict:\n        return {"skill": skill_name, "proposal": "Split into modular sub-skills"}\n''')

# 3. Experiment Runner: evolution/experiments/experiment_runner.py
runner_code = '''from typing import Dict, Any

class ExperimentRunner:
    def run_benchmark_experiment(self, candidate_id: str, baseline_score: float) -> Dict[str, Any]:
        # Simulated benchmark evaluation
        candidate_score = baseline_score + 0.05
        return {
            "candidate_id": candidate_id,
            "baseline_score": baseline_score,
            "candidate_score": candidate_score,
            "improvement": round(candidate_score - baseline_score, 4),
            "outcome": "PASSED" if candidate_score > baseline_score else "REJECTED"
        }
'''
with open(os.path.join(repo_root, "evolution", "experiments", "experiment_runner.py"), "w", encoding="utf-8") as f:
    f.write(runner_code)

# 4. Improvement Generator: evolution/proposals/improvement_generator.py
generator_code = '''import os
from typing import Dict, Any

class ImprovementGenerator:
    def __init__(self, doc_dir: str = "docs/evolution"):
        self.doc_dir = doc_dir
        os.makedirs(self.doc_dir, exist_ok=True)

    def create_report(self, title: str, analysis: dict, experiment: dict) -> str:
        filename = f"EVO_{title.lower().replace(' ', '_')}.md"
        filepath = os.path.join(self.doc_dir, filename)

        content = f"""# Genesis Evolution Report: {title}

**Target Agent:** {analysis.get('agent', 'Global')}
**Baseline Score:** {experiment.get('baseline_score')}
**Optimized Score:** {experiment.get('candidate_score')}
**Improvement:** +{experiment.get('improvement')}

## Pinpointed Weaknesses
{chr(10).join([f"- {w}" for w in analysis.get('weaknesses', [])])}

## Benchmark Experiment Outcome
- Status: **{experiment.get('outcome')}**

## Safety & Governance
> Approval Status: **PENDING REVIEW** (Requires CEO Agent / Human signoff before applying).
"""
        with open(filepath, "w", encoding="utf-8") as f:
            f.write(content)
        return filepath
'''
with open(os.path.join(repo_root, "evolution", "proposals", "improvement_generator.py"), "w", encoding="utf-8") as f:
    f.write(generator_code)

# 5. Unit Tests: tests/test_evolution.py
test_evolution_code = '''import unittest
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
'''
with open(os.path.join(repo_root, "tests", "test_evolution.py"), "w", encoding="utf-8") as f:
    f.write(test_evolution_code)

print("Self Evolution Loop modules and tests successfully built.")
