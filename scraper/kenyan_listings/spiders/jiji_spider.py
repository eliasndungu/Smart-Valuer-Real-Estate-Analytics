"""
Jiji Kenya spider
==================
Crawls https://jiji.co.ke/nairobi/houses-apartments-for-sale (and similar)
and extracts property listing details.

Usage:
    cd scraper
    scrapy crawl jiji
    scrapy crawl jiji -a category=houses-apartments-for-rent -a location=mombasa
"""

import re
from datetime import datetime, timezone

import scrapy

from kenyan_listings.items import PropertyItem


class JijiSpider(scrapy.Spider):
    name = "jiji"
    allowed_domains = ["jiji.co.ke"]

    # Defaults – override via -a arguments
    location: str = "nairobi"
    category: str = "houses-apartments-for-sale"
    max_pages: int = 50

    custom_settings = {
        "DOWNLOAD_DELAY": 2,
        "ROBOTSTXT_OBEY": True,
    }

    def __init__(self, location="nairobi", category="houses-apartments-for-sale",
                 max_pages=50, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.location = location
        self.category = category
        self.max_pages = int(max_pages)
        self.start_urls = [f"https://jiji.co.ke/{location}/{category}"]

    # ------------------------------------------------------------------
    # Listing results page
    # ------------------------------------------------------------------

    def parse(self, response, page=1):
        self.logger.info("Parsing Jiji page %d: %s", page, response.url)

        # Article cards on the listing page
        for card in response.css("article.b-list-advert-base"):
            href = card.css("a.b-list-advert__item-link::attr(href)").get()
            if href:
                yield scrapy.Request(
                    response.urljoin(href),
                    callback=self.parse_listing,
                )

        # Pagination
        if page < self.max_pages:
            next_url = response.css("a.pagination-next::attr(href)").get()
            if next_url:
                yield scrapy.Request(
                    response.urljoin(next_url),
                    callback=self.parse,
                    cb_kwargs={"page": page + 1},
                )

    # ------------------------------------------------------------------
    # Individual listing page
    # ------------------------------------------------------------------

    def parse_listing(self, response):
        item = PropertyItem()

        item["source_site"] = "jiji"
        item["listing_url"] = response.url
        item["scraped_at"] = datetime.now(timezone.utc).isoformat()
        item["price_period"] = (
            "rent" if "for-rent" in self.category else "sale"
        )

        # Title
        item["title"] = self._clean(
            response.css("h1.qa-advert-title::text").get()
        )

        # Price
        raw_price = response.css("span.qa-advert-price::text").get("")
        item["price"] = self._parse_price(raw_price)

        # Attributes table (Jiji renders specs as key-value pairs)
        attrs = {}
        for row in response.css("div.b-advert-attributes div.b-advert-attribute"):
            key = self._clean(row.css("span.b-advert-attribute__name::text").get(""))
            val = self._clean(row.css("span.b-advert-attribute__value::text").get(""))
            if key:
                attrs[key.lower()] = val

        item["property_type"] = attrs.get("type", "unknown")
        item["bedrooms"] = self._parse_int(attrs.get("bedrooms"))
        item["bathrooms"] = self._parse_int(attrs.get("bathrooms"))

        raw_size = attrs.get("size", "")
        item["size_sqft"] = self._parse_float(re.sub(r"[^\d.]", "", raw_size))

        # Location – Jiji shows breadcrumb or address line
        breadcrumb = response.css("ol.breadcrumb li::text").getall()
        item["county"] = breadcrumb[1].strip() if len(breadcrumb) > 1 else None
        item["neighborhood"] = breadcrumb[2].strip() if len(breadcrumb) > 2 else None
        item["latitude"] = None
        item["longitude"] = None

        # Amenities (often in description bullets)
        item["amenities"] = response.css(
            "ul.b-advert-features li::text"
        ).getall()

        # Seller / agent
        item["agent_name"] = self._clean(
            response.css("div.b-seller-info span.b-seller-info__name::text").get()
        )
        item["agent_phone"] = None  # Jiji hides phone behind a reveal button

        # Description
        item["description"] = " ".join(
            response.css("div.b-advert-description *::text").getall()
        ).strip()

        yield item

    # ------------------------------------------------------------------
    # Helpers
    # ------------------------------------------------------------------

    @staticmethod
    def _clean(value):
        return value.strip() if isinstance(value, str) else value

    @staticmethod
    def _parse_price(raw: str) -> float | None:
        if not raw:
            return None
        cleaned = re.sub(r"[^\d.]", "", raw.replace(",", ""))
        try:
            return float(cleaned)
        except ValueError:
            return None

    @staticmethod
    def _parse_int(raw) -> int | None:
        if raw is None:
            return None
        try:
            return int(re.sub(r"[^\d]", "", str(raw)))
        except ValueError:
            return None

    @staticmethod
    def _parse_float(raw) -> float | None:
        if not raw:
            return None
        try:
            return float(raw)
        except ValueError:
            return None
