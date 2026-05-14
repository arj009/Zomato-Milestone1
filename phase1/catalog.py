from __future__ import annotations

import json
import logging
from pathlib import Path

from phase1.models import RestaurantRecord, record_from_json_dict

logger = logging.getLogger(__name__)


class RestaurantCatalog:
    """In-memory restaurant catalog for downstream phases."""

    def __init__(self, records: tuple[RestaurantRecord, ...]):
        self._records = records
        self._by_id = {r.id: r for r in records}

    @property
    def records(self) -> tuple[RestaurantRecord, ...]:
        return self._records

    @property
    def size(self) -> int:
        return len(self._records)

    def get(self, record_id: str) -> RestaurantRecord | None:
        return self._by_id.get(record_id)


def save_catalog_jsonl(catalog: RestaurantCatalog, path: str | Path) -> None:
    p = Path(path)
    p.parent.mkdir(parents=True, exist_ok=True)
    with p.open("w", encoding="utf-8") as f:
        for r in catalog.records:
            f.write(json.dumps(r.to_json_dict(), ensure_ascii=False) + "\n")
    logger.info("Wrote %s records to %s", catalog.size, p)


def load_catalog_jsonl(path: str | Path) -> RestaurantCatalog:
    p = Path(path)
    records: list[RestaurantRecord] = []
    with p.open(encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            records.append(record_from_json_dict(json.loads(line)))
    logger.info("Loaded %s records from %s", len(records), p)
    return RestaurantCatalog(records=tuple(records))
