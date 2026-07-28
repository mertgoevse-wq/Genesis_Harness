from typing import Dict, Any, List

class PipelineRunner:
    def __init__(self, name: str):
        self.name = name
        self.steps: List[Dict[str, Any]] = []

    def add_step(self, agent: str, objective: str, input_schema: dict, output_schema: dict, evaluation_criteria: list):
        self.steps.append({
            "agent": agent,
            "objective": objective,
            "input_schema": input_schema,
            "output_schema": output_schema,
            "evaluation_criteria": evaluation_criteria
        })

    def run(self, initial_input: Dict[str, Any]) -> Dict[str, Any]:
        context = initial_input
        for step in self.steps:
            # Simulated execution context mapping
            context[step["agent"]] = {"status": "SUCCESS", "objective": step["objective"]}
        return context
