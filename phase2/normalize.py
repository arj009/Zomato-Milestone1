from __future__ import annotations
import re
import unicodedata

# Common aliases for consistent matching
_LOCATION_ALIASES: dict[str, str] = {
    "bengaluru": "Bangalore",
    "bangalore": "Bangalore",
    "bombay": "Mumbai",
    "mumbai": "Mumbai",
    "new delhi": "Delhi",
    "delhi ncr": "Delhi",
    "ncr": "Delhi",
    "gurgaon": "Gurgaon",
    "gurugram": "Gurgaon",
    "calcutta": "Kolkata",
    "kolkata": "Kolkata",
    "madras": "Chennai",
    "chennai": "Chennai",
    "pune": "Pune",
    "hyderabad": "Hyderabad",
}

_BUDGET_SYNONYMS: dict[str, str] = {
    "low": "low",
    "cheap": "low",
    "budget": "low",
    "medium": "medium",
    "mid": "medium",
    "moderate": "medium",
    "high": "high",
    "expensive": "high",
    "premium": "high",
}

def normalize_unicode_text(value: str) -> str:
    s = unicodedata.normalize("NFKC", value).strip()
    s = re.sub(r"\s+", " ", s)
    return s

def normalize_location(value: str) -> str:
    s = normalize_unicode_text(value)
    if not s:
        return ""
    key = s.casefold()
    return _LOCATION_ALIASES.get(key, s)

def normalize_budget_token(value: str) -> str | None:
    s = normalize_unicode_text(value)
    if not s:
        return None
    key = s.casefold()
    return _BUDGET_SYNONYMS.get(key)

def normalize_cuisine(value: str) -> str | None:
    s = normalize_unicode_text(value)
    return s if s else None

def normalize_extra(value: str, max_chars: int) -> str | None:
    s = normalize_unicode_text(value)
    if not s:
        return None
    if len(s) > max_chars:
        return None
    return s
