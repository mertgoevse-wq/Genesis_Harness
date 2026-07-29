import os
import sys

# Add root to pythonpath
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from genesis.agents.software_engineer.engineer_agent import SoftwareEngineerAgent
from genesis.tools.filesystem_tool import FileSystemTool
from genesis.tools.documentation_tool import DocumentationTool
from genesis.tools.git_tool import GitTool
from genesis.tools.test_tool import TestTool
from genesis.tools.browser_tool import BrowserTool
from genesis.providers.gemini import GeminiProvider

def main():
    print("==================================================")
    print("PHASE 17: FULL AUTONOMOUS SOFTWARE ENGINEERING TEST")
    print("Task: Verbessere Namaz Trainer Avatar um eine neue Lernanimation.")
    print("==================================================\n")
    
    # 1. Initialize Software Engineer Agent
    agent = SoftwareEngineerAgent(
        agent_id="software_engineer_001",
        name="Lead Code Agent"
    )
    
    # 2. Equip Tools
    tools = [
        FileSystemTool(),
        DocumentationTool(),
        GitTool(),
        TestTool(),
        BrowserTool()
    ]
    agent.equip_tools(tools)
    
    # 3. Assign Provider
    # Using Gemini as an example here with its fallback simulation
    provider = GeminiProvider()
    agent.assign_provider(provider)
    
    # 4. Run the specialized Engineering Loop
    result = agent.run_engineering_loop("Verbessere Namaz Trainer Avatar um eine neue Lernanimation.")
    
    print("\nTest Complete.")
    print("Status:", result["status"])

if __name__ == "__main__":
    main()
