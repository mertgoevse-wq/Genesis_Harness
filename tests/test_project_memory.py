import unittest
from memory_system.project_memory.project_store import ProjectStore
class TestProjectMemory(unittest.TestCase):
    def test_milestone(self):
        ps = ProjectStore()
        count = ps.record_milestone("Architecture", {"stack": "FastHTML"})
        self.assertEqual(count, 1)
if __name__ == "__main__":
    unittest.main()
