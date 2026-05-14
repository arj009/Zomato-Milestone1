from __future__ import annotations
from dataclasses import dataclass
from typing import Optional, Sequence
from phase1.models import RestaurantRecord

@dataclass(frozen=True)
class RankedRecommendation:
    """A single restaurant recommendation with AI justification."""
    rank: int
    record: RestaurantRecord
    explanation: str

@dataclass(frozen=True)
class EngineResult:
    """The complete result from the recommendation engine."""
    summary: Optional[str]
    recommendations: Sequence[RankedRecommendation]
    source: str # e.g., "llm" or "fallback"
    error_note: Optional[str] = None
