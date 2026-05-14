from __future__ import annotations

from dataclasses import asdict, dataclass


@dataclass(frozen=True)
class RestaurantRecord:
    """Normalized row used by later phases for filtering and display."""

    id: str
    name: str
    location: str
    cuisines: str
    rating: float | None
    cost_for_two_inr: float | None
    cost_bucket: str | None
    address: str | None = None
    rest_type: str | None = None
    listed_in_type: str | None = None
    listed_in_city: str | None = None
    url: str | None = None

    def to_json_dict(self) -> dict:
        return asdict(self)


def record_from_json_dict(data: dict) -> RestaurantRecord:
    return RestaurantRecord(
        id=str(data["id"]),
        name=str(data["name"]),
        location=str(data["location"]),
        cuisines=str(data["cuisines"]),
        rating=_optional_float(data.get("rating")),
        cost_for_two_inr=_optional_float(data.get("cost_for_two_inr")),
        cost_bucket=_optional_str(data.get("cost_bucket")),
        address=_optional_str(data.get("address")),
        rest_type=_optional_str(data.get("rest_type")),
        listed_in_type=_optional_str(data.get("listed_in_type")),
        listed_in_city=_optional_str(data.get("listed_in_city")),
        url=_optional_str(data.get("url")),
    )


def _optional_float(v: object) -> float | None:
    if v is None:
        return None
    if isinstance(v, (int, float)):
        return float(v)
    return None


def _optional_str(v: object) -> str | None:
    if v is None:
        return None
    s = str(v).strip()
    return s or None
