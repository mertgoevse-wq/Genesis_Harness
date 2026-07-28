"""Base classes for live intelligence connectors."""

from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from datetime import datetime, timedelta, timezone
from typing import Any, Dict, List, Optional
import json
import os


@dataclass
class ConnectorResult:
    """Result from a live intelligence connector."""

    source: str
    data: Any
    timestamp: str
    confidence: str  # VERIFIED, KNOWN, ASSUMED, UNKNOWN
    cached: bool = False
    fallback: bool = False
    error: Optional[str] = None


class LiveConnector(ABC):
    """Abstract base class for live intelligence connectors.

    Connectors can operate in three modes:
    - live: fetch from real external API
    - cached: return cached data if available and fresh
    - fallback: return placeholder/assumed data when live data is unavailable
    """

    def __init__(
        self,
        name: str,
        cache_ttl_seconds: int = 3600,
        fallback_enabled: bool = True,
        cache_dir: str = ".cache/live_intelligence",
    ):
        self.name = name
        self.cache_ttl = timedelta(seconds=cache_ttl_seconds)
        self.fallback_enabled = fallback_enabled
        self.cache_dir = cache_dir
        os.makedirs(cache_dir, exist_ok=True)

    def fetch(self, query: str, **kwargs) -> ConnectorResult:
        """Fetch data with caching and fallback."""
        cache_key = self._cache_key(query, kwargs)

        # Try cache first
        cached = self._read_cache(cache_key)
        if cached and self._cache_valid(cached):
            cached.cached = True
            return cached

        # Try live fetch
        try:
            result = self._fetch_live(query, **kwargs)
            result.cached = False
            self._write_cache(cache_key, result)
            return result
        except Exception as e:
            if self.fallback_enabled:
                fallback = self._fallback(query, **kwargs)
                fallback.fallback = True
                fallback.error = str(e)
                return fallback
            raise

    @abstractmethod
    def _fetch_live(self, query: str, **kwargs) -> ConnectorResult:
        """Implement live fetch logic. Must raise on failure."""
        raise NotImplementedError

    @abstractmethod
    def _fallback(self, query: str, **kwargs) -> ConnectorResult:
        """Return fallback data when live fetch fails."""
        raise NotImplementedError

    def _cache_key(self, query: str, kwargs: Dict[str, Any]) -> str:
        raw = f"{self.name}_{query}_{json.dumps(kwargs, sort_keys=True, default=str)}"
        for char in ["/", "\\", ":", "?", "*", '"', "<", ">", "|"]:
            raw = raw.replace(char, "_")
        return raw[:200]

    def _cache_path(self, key: str) -> str:
        return os.path.join(self.cache_dir, f"{key}.json")

    def _read_cache(self, key: str) -> Optional[ConnectorResult]:
        path = self._cache_path(key)
        if not os.path.exists(path):
            return None
        try:
            with open(path, "r", encoding="utf-8") as f:
                payload = json.load(f)
            return ConnectorResult(**payload)
        except Exception:
            return None

    def _write_cache(self, key: str, result: ConnectorResult) -> None:
        path = self._cache_path(key)
        payload = {
            "source": result.source,
            "data": result.data,
            "timestamp": result.timestamp,
            "confidence": result.confidence,
            "cached": result.cached,
            "fallback": result.fallback,
            "error": result.error,
        }
        os.makedirs(os.path.dirname(path), exist_ok=True)
        with open(path, "w", encoding="utf-8") as f:
            json.dump(payload, f, default=str)

    def _cache_valid(self, result: ConnectorResult) -> bool:
        try:
            ts = datetime.fromisoformat(result.timestamp)
            now = datetime.now(timezone.utc) if ts.tzinfo else datetime.utcnow()
            return now - ts < self.cache_ttl
        except Exception:
            return False
