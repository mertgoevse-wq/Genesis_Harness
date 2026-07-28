"""Founder decision memory for Genesis.

Persists failed ideas, successful patterns, market opportunities, previous decisions,
and decision rationale so the system learns from the past.
"""

from .founder_memory_store import FounderMemoryStore

__all__ = ["FounderMemoryStore"]
