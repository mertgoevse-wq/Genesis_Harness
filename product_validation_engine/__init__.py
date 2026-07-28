"""Product Validation Engine.

Evaluates product ideas using market demand, competition, pricing potential,
customer pain, implementation complexity, acquisition difficulty, and expected
revenue. Produces GO / MODIFY / REJECT decisions with confidence scores.
"""

from .validation_engine import ProductValidationEngine, ValidationDecision
from .scoring import ValidationScorer

__all__ = [
    "ProductValidationEngine",
    "ValidationDecision",
    "ValidationScorer",
]
