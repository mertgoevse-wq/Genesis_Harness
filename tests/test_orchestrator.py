"""Tests for genesis.orchestrator."""

import unittest
from unittest.mock import patch

from genesis.orchestrator import MasterGenesisOrchestrator


class TestMasterGenesisOrchestrator(unittest.TestCase):
    def test_evaluate_venture(self) -> None:
        orchestrator = MasterGenesisOrchestrator()
        result = orchestrator.evaluate_venture("AI Note Assistant")
        self.assertIn("idea", result)
        self.assertIn("decision", result)
        self.assertIn("validation", result)
        self.assertIn("opportunities", result)
        self.assertIn("revenue", result)
        self.assertIn("deployment", result)
        self.assertIn("growth", result)

    def test_memory_records_decision(self) -> None:
        orchestrator = MasterGenesisOrchestrator()
        with patch.object(orchestrator.founder_memory, "record_decision") as mock:
            orchestrator.evaluate_venture("AI Note Assistant")
            mock.assert_called_once()
