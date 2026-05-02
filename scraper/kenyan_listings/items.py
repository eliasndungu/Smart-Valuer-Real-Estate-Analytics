import scrapy


class PropertyItem(scrapy.Item):
    """Represents a single property listing scraped from a Kenyan property site."""

    # Source metadata
    source_site = scrapy.Field()        # e.g. "buyrentkenya" | "jiji"
    listing_url = scrapy.Field()        # canonical URL of the listing page
    scraped_at = scrapy.Field()         # ISO-8601 timestamp

    # Core listing attributes
    title = scrapy.Field()              # listing headline
    price = scrapy.Field()              # numeric price in KES
    price_period = scrapy.Field()       # "sale" | "monthly" | "daily"
    property_type = scrapy.Field()      # "apartment" | "house" | "land" | ...

    # Location
    neighborhood = scrapy.Field()       # suburb / estate name
    county = scrapy.Field()             # Kenyan county
    latitude = scrapy.Field()           # float, when available
    longitude = scrapy.Field()          # float, when available

    # Physical attributes
    bedrooms = scrapy.Field()           # int
    bathrooms = scrapy.Field()          # int
    size_sqft = scrapy.Field()          # float, square feet

    # Amenities (list of strings)
    amenities = scrapy.Field()

    # Contact / agent
    agent_name = scrapy.Field()
    agent_phone = scrapy.Field()

    # Raw description for NLP
    description = scrapy.Field()
