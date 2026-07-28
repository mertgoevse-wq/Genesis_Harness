class AgentRunner:
    def run(self, agent_name: str, context: dict) -> dict:
        return {"status": "SUCCESS", "output": f"Runner executed {agent_name}"}
