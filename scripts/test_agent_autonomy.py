import os
import sys

# Add root to pythonpath
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from genesis.agents.runtime.agent_runtime import AutonomousAgent
from genesis.tools.filesystem_tool import FileSystemTool
from genesis.tools.documentation_tool import DocumentationTool
from genesis.providers.claude import ClaudeProvider

def main():
    print("==================================================")
    print("PHASE 16: TRUE AGENT INTELLIGENCE LAYER TEST")
    print("Task: Verbessere den Namaz Trainer Avatar")
    print("==================================================\n")
    
    # 1. Initialize Agent
    agent = AutonomousAgent(
        agent_id="agent_avatar_improver_001",
        name="UI/Animation Agent",
        role="Frontend & Animation Specialist",
        mission="Create smooth, engaging avatar interactions for the user.",
        capabilities=["ui-design", "avatar-animation", "python-fastapi-backend"]
    )
    
    # 2. Equip Tools
    fs_tool = FileSystemTool()
    doc_tool = DocumentationTool()
    agent.equip_tools([fs_tool, doc_tool])
    
    # 3. Assign Provider
    claude = ClaudeProvider()
    agent.assign_provider(claude)
    
    # 4. Run Decision Loop (OODA)
    result = agent.run_decision_loop("Verbessere den Namaz Trainer Avatar, baue neue Transitions ein.")
    
    print("\nTest Complete.")
    print("Agent Memory Context:", agent.memory.get_context())

if __name__ == "__main__":
    main()
