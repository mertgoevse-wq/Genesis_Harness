import unittest
from memory_system.research_memory.research_store import ResearchMemoryStore
class TestResearchMemory(unittest.TestCase):
    def test_save(self):
        rms = ResearchMemoryStore()
        self.assertTrue(rms.save_discovery({"concept": "Agentic Workflows"}))
if __name__ == "__main__":
    unittest.main()
