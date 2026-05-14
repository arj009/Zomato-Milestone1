from __future__ import annotations
import re
from phase1.catalog import RestaurantCatalog
from phase1.models import RestaurantRecord
from phase2.models import UserPreferences

def _location_matches(prefs: UserPreferences, record: RestaurantRecord) -> bool:
    needle = prefs.location.casefold()
    # Search in multiple fields for robustness
    haystack = f"{record.location} {record.listed_in_city or ''} {record.address or ''} {record.name}".casefold()
    return needle in haystack

def _budget_matches(prefs: UserPreferences, record: RestaurantRecord) -> bool:
    if record.cost_bucket is None:
        return True # Include if unknown
    return record.cost_bucket == prefs.budget

def _cuisine_matches(prefs: UserPreferences, record: RestaurantRecord) -> bool:
    if not prefs.cuisine:
        return True
    return prefs.cuisine.casefold() in record.cuisines.casefold()

def _rating_matches(prefs: UserPreferences, record: RestaurantRecord) -> bool:
    if record.rating is None:
        return False
    return record.rating >= prefs.min_rating

def _extra_matches(prefs: UserPreferences, record: RestaurantRecord) -> bool:
    if not prefs.extra:
        return True
    hay = f"{record.name} {record.cuisines} {record.rest_type or ''}".casefold()
    words = [w for w in re.findall(r"[a-z0-9]+", prefs.extra.casefold()) if len(w) > 2]
    if not words:
        return True
    return any(w in hay for w in words)

def filter_catalog(catalog: RestaurantCatalog, prefs: UserPreferences) -> list[RestaurantRecord]:
    """Applies hard filters to the catalog based on user preferences."""
    results = []
    for r in catalog.records:
        if not _location_matches(prefs, r): continue
        if not _budget_matches(prefs, r): continue
        if not _cuisine_matches(prefs, r): continue
        if not _rating_matches(prefs, r): continue
        if not _extra_matches(prefs, r): continue
        results.append(r)
    return results
