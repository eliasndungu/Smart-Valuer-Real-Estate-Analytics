"""
Scrapy pipelines for the kenyan_listings project.

Order of execution (configured in settings.py):
  1. ValidationPipeline  – drops items missing required fields
  2. JsonWriterPipeline  – writes valid items to JSONL (handled by FEEDS setting,
                           but this pipeline also keeps an in-memory list that
                           tests / other consumers can reference)
"""

import json
import logging
from datetime import datetime, timezone
from pathlib import Path

from itemadapter import ItemAdapter
from scrapy.exceptions import DropItem

logger = logging.getLogger(__name__)

REQUIRED_FIELDS = {"listing_url", "price", "neighborhood", "property_type"}


class ValidationPipeline:
    """Drop items that are missing required fields or have obviously bad data."""

    def process_item(self, item, spider):
        adapter = ItemAdapter(item)

        # Check required fields exist and are non-empty
        for field in REQUIRED_FIELDS:
            value = adapter.get(field)
            if value is None or (isinstance(value, str) and not value.strip()):
                raise DropItem(f"Missing required field '{field}' in item from {spider.name}")

        # Coerce price to a positive number
        raw_price = adapter.get("price")
        try:
            price_val = float(str(raw_price).replace(",", "").strip())
            if price_val <= 0:
                raise ValueError("Price must be positive")
            adapter["price"] = price_val
        except (TypeError, ValueError) as exc:
            raise DropItem(f"Invalid price '{raw_price}': {exc}") from exc

        # Stamp scrape time if not already set
        if not adapter.get("scraped_at"):
            adapter["scraped_at"] = datetime.now(timezone.utc).isoformat()

        return item


class JsonWriterPipeline:
    """Append each valid item to a JSONL file (mirrors the FEEDS setting for explicitness)."""

    def __init__(self):
        self.items: list = []

    def open_spider(self, spider):
        output_dir = Path("output")
        output_dir.mkdir(exist_ok=True)
        self._file = open(output_dir / "properties.jsonl", "a", encoding="utf-8")

    def close_spider(self, spider):
        self._file.close()
        logger.info("JsonWriterPipeline closed – %d items written", len(self.items))

    def process_item(self, item, spider):
        adapter = ItemAdapter(item)
        line = json.dumps(dict(adapter)) + "\n"
        self._file.write(line)
        self.items.append(dict(adapter))
        return item
