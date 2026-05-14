from __future__ import annotations
from typing import cast
from phase2.exceptions import PreferenceValidationError
from phase2.models import BudgetTier, UserPreferences
from phase2.normalize import (
    normalize_budget_token,
    normalize_cuisine,
    normalize_extra,
    normalize_location,
)

def build_user_preferences(
    *,
    location: str,
    budget: str,
    cuisine: str,
    min_rating: str | float,
    extra: str,
    min_rating_floor: float = 0.0,
    min_rating_ceiling: float = 5.0,
    extra_max_chars: int = 500,
) -> UserPreferences:
    """Validate and normalize raw input into a UserPreferences object."""
    errors: list[str] = []

    loc = normalize_location(location)
    if not loc:
        errors.append("Location is required.")

    budget_norm = normalize_budget_token(budget)
    if budget_norm is None:
        errors.append("Budget must be 'low', 'medium', or 'high'.")

    cuisine_norm = normalize_cuisine(cuisine)

    try:
        rating_val = float(str(min_rating).strip())
    except ValueError:
        errors.append("Minimum rating must be a number.")
        rating_val = None

    if rating_val is not None:
        if rating_val < min_rating_floor or rating_val > min_rating_ceiling:
            errors.append(f"Rating must be between {min_rating_floor} and {min_rating_ceiling}.")

    extra_norm = normalize_extra(extra, max_chars=extra_max_chars)
    if extra.strip() and extra_norm is None:
        errors.append(f"Extra info must be under {extra_max_chars} chars.")

    if errors:
        raise PreferenceValidationError(errors)

    return UserPreferences(
        location=loc,
        budget=cast(BudgetTier, budget_norm),
        cuisine=cuisine_norm,
        min_rating=rating_val,
        extra=extra_norm,
    )
