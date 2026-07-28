"""Tests for the CLI entry point."""

import json
import unittest
from io import StringIO
from unittest.mock import patch

from genesis.__main__ import main


class TestCLI(unittest.TestCase):
    def test_cli_analyze(self) -> None:
        with patch("sys.stdout", new_callable=StringIO) as mock_stdout:
            main(["analyze", "AI Customer Support"])
            output = mock_stdout.getvalue()
        result = json.loads(output)
        self.assertIn("idea", result)
        self.assertIn("decision", result)
