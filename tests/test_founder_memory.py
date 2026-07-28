"""Tests for founder decision memory."""

import os
import tempfile
import unittest

from memory_system.founder_memory.founder_memory_store import FounderMemoryStore


class TestFounderMemoryStore(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.NamedTemporaryFile(delete=False, suffix=".json")
        self.store = FounderMemoryStore(storage_path=self.tmp.name)

    def tearDown(self):
        self.tmp.close()
        os.unlink(self.tmp.name)

    def test_record_decision(self):
        self.store.record_decision("idea", "GO", "strong market", 0.8, {})
        self.assertEqual(len(self.store.previous_decisions()), 1)

    def test_successful_patterns(self):
        self.store.record_decision("good idea", "GO", "strong", 0.9, {})
        self.store.record_decision("bad idea", "REJECT", "weak", 0.3, {})
        self.assertEqual(len(self.store.successful_patterns()), 1)
        self.assertEqual(len(self.store.failed_ideas()), 1)


if __name__ == "__main__":
    unittest.main()
