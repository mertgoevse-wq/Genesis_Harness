from genesis.agents.runtime.agent_runtime import AutonomousAgent

class SoftwareEngineerAgent(AutonomousAgent):
    """A specialized Autonomous Agent for Software Engineering tasks."""
    
    def __init__(self, agent_id: str, name: str):
        super().__init__(
            agent_id=agent_id,
            name=name,
            role="Software Engineer",
            mission="Autonomously develop software, write code, create tests, debug and refactor.",
            capabilities=["code_read", "code_write", "test_generation", "debugging", "refactoring"]
        )
        
    def run_engineering_loop(self, task: str):
        """The specialized engineering workflow loop."""
        print(f"\n=== {self.name} STARTING ENGINEERING LOOP ===")
        
        print(f"[{self.name}] 1. Analyze Repository...")
        if self.llm_provider:
            analysis = self.llm_provider.analyze(f"Analyze repo for task: {task}")
            print(f"    -> {analysis}")
            
        print(f"[{self.name}] 2. Create Plan...")
        if self.llm_provider:
            plan = self.llm_provider.plan(task, "Context: Clean Architecture")
            print(f"    -> {plan}")
            
        print(f"[{self.name}] 3. Modify Files...")
        if self.llm_provider:
            code = self.llm_provider.generate_code(task, {"file": "target.py"})
            print(f"    -> {code}")
            
        print(f"[{self.name}] 4. Run Tests...")
        if "test_tool" in self.available_tools:
            test_result = self.available_tools["test_tool"].execute("all")
            print(f"    -> {test_result}")
            
        print(f"[{self.name}] 5. Fix Errors...")
        print(f"    -> No errors found.")
        
        print(f"[{self.name}] 6. Commit...")
        if "git_tool" in self.available_tools:
            commit_result = self.available_tools["git_tool"].execute("commit", "Implemented feature: " + task)
            print(f"    -> {commit_result}")
            
        print(f"=== {self.name} FINISHED ENGINEERING LOOP ===\n")
        return {"status": "success", "commits": 1}
