from __future__ import annotations
from dataclasses import dataclass
from typing import Literal

BudgetTier = Literal["low", "medium", "high"]

@dataclass(frozen=True)
class UserPreferences:
    """Normalized preference object for filtering and LLM integration."""
    location: str
    budget: BudgetTier
    cuisine: str | None
    min_rating: float
    extra: str | None

    def to_json_dict(self) -> dict:
        return {
            "location": self.location,
            "budget": self.budget,
            "cuisine": self.cuisine,
            "min_rating": self.min_rating,
            "extra": self.extra,
        }
