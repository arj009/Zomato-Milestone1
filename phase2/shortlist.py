from __future__ import annotations
from phase1.models import RestaurantRecord

def shortlist_candidates(
    records: list[RestaurantRecord],
    max_n: int = 10
) -> list[RestaurantRecord]:
    """Ranks candidates by rating and cost, then caps the list for the LLM."""
    
    def ranking_key(r: RestaurantRecord):
        rating = r.rating if r.rating is not None else 0.0
        cost = r.cost_for_two_inr if r.cost_for_two_inr is not None else 0.0
        # Sort by Rating (Desc), then Cost (Desc) for luxury/popular feel
        return (-rating, -cost, r.name.casefold())

    sorted_records = sorted(records, key=ranking_key)
    return sorted_records[:max(0, max_n)]
