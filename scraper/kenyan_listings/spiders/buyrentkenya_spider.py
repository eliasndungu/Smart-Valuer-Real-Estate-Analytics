"""
BuyRentKenya spider
====================
Crawls https://www.buyrentkenya.com/property-for-sale (and/or for-rent)
and extracts property listing details.

Usage:
    cd scraper
    scrapy crawl buyrentkenya
    scrapy crawl buyrentkenya -a listing_type=rent -a max_pages=5

NOTE: CSS/XPath selectors are based on the site's structure at time of writing.
      Adjust if the site markup changes.
"""

import json
import re
from datetime import datetime, timezone

import scrapy

from kenyan_listings.items import PropertyItem


class BuyRentKenyaSpider(scrapy.Spider):
    name = "buyrentkenya"
    allowed_domains = ["buyrentkenya.com"]

    # Configurable via -a arguments
    listing_type: str = "sale"   # "sale" | "rent"
    max_pages: int = 50          # safety cap on pagination

    custom_settings = {
        "DOWNLOAD_DELAY": 2,
        "ROBOTSTXT_OBEY": True,
    }

    def __init__(self, listing_type="sale", max_pages=50, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.listing_type = listing_type
        self.max_pages = int(max_pages)
        slug = "property-for-sale" if listing_type == "sale" else "houses-apartments-for-rent"
        self.start_urls = [f"https://www.buyrentkenya.com/{slug}"]

    # ------------------------------------------------------------------
    # Entry point – listing / search result pages
    # ------------------------------------------------------------------

    def parse(self, response, page=1):
        """Parse a listing-results page and follow individual listing links."""
        self.logger.info("Parsing page %d: %s", page, response.url)

        listing_links = response.css("a.listing-card__link::attr(href)").getall()
        if not listing_links:
            # Try alternative selector patterns
            listing_links = response.css(
                "div.property-card a[href*='/listings/']::attr(href)"
            ).getall()

        for href in listing_links:
            url = response.urljoin(href)
            yield scrapy.Request(url, callback=self.parse_listing)

        # ------ Pagination ------
        if page < self.max_pages:
            next_url = response.css("a[rel='next']::attr(href)").get()
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
        """Extract property details from a single listing page."""
        item = PropertyItem()

        item["source_site"] = "buyrentkenya"
        item["listing_url"] = response.url
        item["scraped_at"] = datetime.now(timezone.utc).isoformat()
        item["price_period"] = self.listing_type

        # Title
        item["title"] = self._clean(
            response.css("h1.listing-title::text, h1[class*='title']::text").get()
        )

        # Price – strip non-numeric characters except dots/commas
        raw_price = response.css(
            "span.listing-price::text, div[class*='price'] span::text"
        ).get("")
        item["price"] = self._parse_price(raw_price)

        # Property type
        item["property_type"] = self._clean(
            response.css(
                "span[data-testid='property-type']::text, "
                "li:contains('Property Type') span::text"
            ).get("unknown")
        )

        # Location
        item["neighborhood"] = self._clean(
            response.css(
                "span[data-testid='neighbourhood']::text, "
                "address span.neighbourhood::text"
            ).get()
        )
        item["county"] = self._clean(
            response.css(
                "span[data-testid='county']::text, "
                "address span.county::text"
            ).get()
        )

        # Coordinates (sometimes injected as JSON-LD)
        lat, lon = self._extract_coords(response)
        item["latitude"] = lat
        item["longitude"] = lon

        # Bedrooms / bathrooms
        item["bedrooms"] = self._parse_int(
            response.css(
                "span[data-testid='bedrooms']::text, "
                "li[class*='bedroom'] span::text"
            ).get()
        )
        item["bathrooms"] = self._parse_int(
            response.css(
                "span[data-testid='bathrooms']::text, "
                "li[class*='bathroom'] span::text"
            ).get()
        )

        # Size
        raw_size = response.css(
            "span[data-testid='size']::text, li[class*='size'] span::text"
        ).get("")
        item["size_sqft"] = self._parse_float(re.sub(r"[^\d.]", "", raw_size))

        # Amenities
        item["amenities"] = response.css(
            "ul.amenities li::text, div[class*='amenities'] span::text"
        ).getall()

        # Agent
        item["agent_name"] = self._clean(
            response.css("span.agent-name::text, div[class*='agent'] h3::text").get()
        )
        item["agent_phone"] = self._clean(
            response.css("a[href^='tel:']::attr(href)").get("").replace("tel:", "")
        )

        # Description
        item["description"] = " ".join(
            response.css(
                "div.listing-description *::text, div[class*='description'] p::text"
            ).getall()
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
        """Return price as a float (KES), or None if unparseable."""
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

    @staticmethod
    def _extract_coords(response):
        """Try to extract lat/lon from JSON-LD or meta tags."""
        for script in response.css('script[type="application/ld+json"]::text').getall():
            try:
                data = json.loads(script)
                geo = data.get("geo", {})
                if geo:
                    return geo.get("latitude"), geo.get("longitude")
            except (json.JSONDecodeError, AttributeError):
                pass

        lat = response.css("meta[property='place:location:latitude']::attr(content)").get()
        lon = response.css("meta[property='place:location:longitude']::attr(content)").get()
        return lat, lon
