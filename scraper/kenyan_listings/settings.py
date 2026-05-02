BOT_NAME = "kenyan_listings"

SPIDER_MODULES = ["kenyan_listings.spiders"]
NEWSPIDER_MODULE = "kenyan_listings.spiders"

# Crawl responsibly by identifying yourself
USER_AGENT = "SmartValuer/1.0 (+https://github.com/eliasndungu/Smart-Valuer-Real-Estate-Analytics)"

# Obey robots.txt rules
ROBOTSTXT_OBEY = True

# Rate limiting – be polite to the target sites
DOWNLOAD_DELAY = 2
RANDOMIZE_DOWNLOAD_DELAY = True
CONCURRENT_REQUESTS = 4
CONCURRENT_REQUESTS_PER_DOMAIN = 2

# Disable cookies (saves some bandwidth, avoids session tracking)
COOKIES_ENABLED = False

# Retry on errors but limit retries
RETRY_TIMES = 3
RETRY_HTTP_CODES = [500, 502, 503, 504, 408]

# Pipeline: validate → save to JSON
ITEM_PIPELINES = {
    "kenyan_listings.pipelines.ValidationPipeline": 100,
    "kenyan_listings.pipelines.JsonWriterPipeline": 300,
}

# Output to a JSON lines file for easy downstream ingestion
FEEDS = {
    "output/properties.jsonl": {
        "format": "jsonlines",
        "overwrite": False,
        "encoding": "utf-8",
    }
}

LOG_LEVEL = "INFO"
