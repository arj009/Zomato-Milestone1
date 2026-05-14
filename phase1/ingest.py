from __future__ import annotations

import hashlib
import logging
import re
import unicodedata
from collections.abc import Iterable, Iterator

from datasets import Dataset, load_dataset

from phase1.catalog import RestaurantCatalog
from phase1.models import RestaurantRecord

logger = logging.getLogger(__name__)

# Cost categories in INR for two people
_COST_LOW_MAX_INR = 400.0
_COST_MED_MAX_INR = 800.0


def normalize_text(value: object | None) -> str:
    if value is None:
        return ""
    s = str(value).strip()
    if not s or s.lower() in {"nan", "none", "null"}:
        return ""
    # Standardize Unicode (NFKC) to ensure consistent matching
    s = unicodedata.normalize("NFKC", s)
    return s


def parse_rate(raw: object | None) -> float | None:
    s = normalize_text(raw)
    if not s:
        return None
    up = s.upper()
    if up in {"NEW", "-", "NAN"}:
        return None
    # Extracts the numeric part (e.g., "4.1/5" -> 4.1)
    m = re.match(r"^([\d.]+)", s)
    if not m:
        return None
    try:
        val = float(m.group(1))
    except ValueError:
        return None
    if val < 0 or val > 5.0:
        return None
    return val


def parse_cost_inr(raw: object | None) -> float | None:
    s = normalize_text(raw)
    if not s:
        return None
    # Remove commas and non-numeric chars (e.g., "1,200" -> 1200)
    digits = re.sub(r"[^\d.]", "", s)
    if not digits:
        return None
    try:
        val = float(digits)
    except ValueError:
        return None
    return val


def cost_bucket_from_inr(cost: float | None) -> str | None:
    if cost is None:
        return None
    if cost <= _COST_LOW_MAX_INR:
        return "low"
    if cost <= _COST_MED_MAX_INR:
        return "medium"
    return "high"


def stable_record_id(name: str, location: str, address: str) -> str:
    # Create a unique, deterministic ID for deduplication
    key = f"{name.lower().strip()}|{location.lower().strip()}|{address.lower().strip()}"
    return hashlib.sha256(key.encode("utf-8")).hexdigest()[:16]


def row_dict_to_record(row: dict) -> RestaurantRecord | None:
    name = normalize_text(row.get("name"))
    location = normalize_text(row.get("location")) or normalize_text(row.get("listed_in(city)"))
    if not name or not location:
        return None

    address = normalize_text(row.get("address")) or None
    rid = stable_record_id(name, location, address or "")

    cuisines = normalize_text(row.get("cuisines")) or "(unknown)"
    rating = parse_rate(row.get("rate"))
    cost = parse_cost_inr(row.get("approx_cost(for two people)"))
    bucket = cost_bucket_from_inr(cost)

    return RestaurantRecord(
        id=rid,
        name=name,
        location=location,
        cuisines=cuisines,
        rating=rating,
        cost_for_two_inr=cost,
        cost_bucket=bucket,
        address=address,
        rest_type=normalize_text(row.get("rest_type")) or None,
        listed_in_type=normalize_text(row.get("listed_in(type)")) or None,
        listed_in_city=normalize_text(row.get("listed_in(city)")) or None,
        url=normalize_text(row.get("url")) or None,
    )


def iter_normalized_records(dataset: Dataset) -> Iterator[RestaurantRecord]:
    for row in dataset:
        rec = row_dict_to_record(row)
        if rec is not None:
            yield rec


def dedupe_records(records: Iterable[RestaurantRecord]) -> list[RestaurantRecord]:
    by_id: dict[str, RestaurantRecord] = {}
    for r in records:
        existing = by_id.get(r.id)
        if existing is None:
            by_id[r.id] = r
            continue
        # If duplicate, keep the one with more data
        by_id[r.id] = _prefer_richer_record(existing, r)
    return list(by_id.values())


def _prefer_richer_record(a: RestaurantRecord, b: RestaurantRecord) -> RestaurantRecord:
    return a if _completeness_score(a) >= _completeness_score(b) else b


def _completeness_score(r: RestaurantRecord) -> int:
    score = 0
    if r.rating is not None: score += 2
    if r.cost_for_two_inr is not None: score += 2
    if r.address: score += 1
    if r.rest_type: score += 1
    return score


def build_catalog_from_hf_dataset(dataset_id: str, split: str = "train") -> RestaurantCatalog:
    logger.info("Fetching dataset: %s", dataset_id)
    ds = load_dataset(dataset_id, split=split)
    records = dedupe_records(iter_normalized_records(ds))
    logger.info("Built catalog with %s unique records", len(records))
    return RestaurantCatalog(records=tuple(records))
