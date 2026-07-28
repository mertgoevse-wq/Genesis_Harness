"""Tests for genesis.memory."""

import os
import tempfile
import unittest

from genesis.memory import FounderMemoryStore, KnowledgeStore


class TestFounderMemoryStore(unittest.TestCase):
    def setUp(self) -> None:
        self.tmp = tempfile.NamedTemporaryFile(delete=False, suffix=".json")
        self.store = FounderMemoryStore(storage_path=self.tmp.name)

    def tearDown(self) -> None:
        self.tmp.close()
        os.unlink(self.tmp.name)

    def test_record_decision(self) -> None:
        self.store.record_decision("idea", "GO", "strong market", 0.8, {})
        self.assertEqual(len(self.store.previous_decisions()), 1)

    def test_successful_patterns(self) -> None:
        self.store.record_decision("good idea", "GO", "strong", 0.9, {})
        self.store.record_decision("bad idea", "REJECT", "weak", 0.3, {})
        self.assertEqual(len(self.store.successful_patterns()), 1)
        self.assertEqual(len(self.store.failed_ideas()), 1)


class TestKnowledgeStore(unittest.TestCase):
    def setUp(self) -> None:
        self.tmp = tempfile.NamedTemporaryFile(delete=False, suffix=".json")
        self.store = KnowledgeStore(db_path=self.tmp.name)

    def tearDown(self) -> None:
        self.tmp.close()
        os.unlink(self.tmp.name)

    def test_save_record(self) -> None:
        record = self.store.save_record("test", {"key": "value"})
        self.assertEqual(record["category"], "test")
        self.assertEqual(len(self.store.records), 1)
