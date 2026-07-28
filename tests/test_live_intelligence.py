"""Tests for live_intelligence subsystem."""

import shutil
import tempfile
import unittest
from datetime import datetime, timezone

from live_intelligence.base import LiveConnector, ConnectorResult
from live_intelligence.connectors.market_data import MarketDataConnector
from live_intelligence.connectors.saas_trends import SaaSTrendsConnector
from live_intelligence.connectors.github_signals import GitHubSignalsConnector
from live_intelligence.connectors.startup_signals import StartupSignalsConnector
from live_intelligence.orchestrator import LiveIntelligenceOrchestrator


class DummyConnector(LiveConnector):
    def _fetch_live(self, query: str, **kwargs):
        return ConnectorResult(
            source=self.name,
            data={"live": True},
            timestamp=datetime.now(timezone.utc).isoformat(),
            confidence="VERIFIED",
        )

    def _fallback(self, query: str, **kwargs):
        return ConnectorResult(
            source=self.name,
            data={"fallback": True},
            timestamp=datetime.now(timezone.utc).isoformat(),
            confidence="ASSUMED",
        )


class TestLiveConnector(unittest.TestCase):
    def setUp(self):
        self.cache_dir = tempfile.mkdtemp()

    def tearDown(self):
        shutil.rmtree(self.cache_dir, ignore_errors=True)

    def test_cache_and_fallback(self):
        connector = DummyConnector(
            name="dummy",
            cache_dir=self.cache_dir,
        )
        result = connector.fetch("test")
        self.assertEqual(result.source, "dummy")
        self.assertEqual(result.data["live"], True)

    def test_cache_returns_cached_result(self):
        connector = DummyConnector(
            name="dummy",
            cache_dir=self.cache_dir,
        )
        first = connector.fetch("test")
        second = connector.fetch("test")
        self.assertTrue(second.cached)
        self.assertEqual(second.data["live"], True)


class TestConnectors(unittest.TestCase):
    def setUp(self):
        self.cache_dir = tempfile.mkdtemp()

    def tearDown(self):
        shutil.rmtree(self.cache_dir, ignore_errors=True)

    def _assert_fallback(self, connector):
        result = connector.fetch("AI SaaS")
        self.assertTrue(result.fallback)
        self.assertEqual(result.confidence, "ASSUMED")
        self.assertIsInstance(result.data, dict)

    def test_market_data_connector(self):
        self._assert_fallback(MarketDataConnector(cache_dir=self.cache_dir))

    def test_saas_trends_connector(self):
        self._assert_fallback(SaaSTrendsConnector(cache_dir=self.cache_dir))

    def test_github_signals_connector(self):
        self._assert_fallback(GitHubSignalsConnector(cache_dir=self.cache_dir))

    def test_startup_signals_connector(self):
        self._assert_fallback(StartupSignalsConnector(cache_dir=self.cache_dir))


class TestLiveIntelligenceOrchestrator(unittest.TestCase):
    def setUp(self):
        self.cache_dir = tempfile.mkdtemp()

    def tearDown(self):
        shutil.rmtree(self.cache_dir, ignore_errors=True)

    def test_gather_returns_signals(self):
        orchestrator = LiveIntelligenceOrchestrator()
        orchestrator.connectors = [
            DummyConnector(name="dummy", cache_dir=self.cache_dir)
        ]
        report = orchestrator.gather("AI SaaS")
        self.assertIn("signals", report)
        self.assertIn("dummy", report["signals"])


if __name__ == "__main__":
    unittest.main()
