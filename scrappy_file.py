import scrapy
from scrapy.crawler import CrawlerProcess

# List of URLs you want to scrape
URLS = [
    "https://example.com/page1",
    "https://example.com/page2",
    "https://example.com/page3",
]

class SimpleSpider(scrapy.Spider):
    name = "simple_spider"
    start_urls = URLS

    def parse(self, response):
        filename = response.url.split("/")[-1] + ".html"
        with open(filename, "wb") as f:
            f.write(response.body)
        self.log(f"Saved {filename}")

# Configure Scrapy settings programmatically
settings = {
    "USER_AGENT": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
                  "(KHTML, like Gecko) Chrome/116.0.0.0 Safari/537.36",
    "ROBOTSTXT_OBEY": False,
    "AUTOTHROTTLE_ENABLED": True,
    "AUTOTHROTTLE_START_DELAY": 1,
    "AUTOTHROTTLE_MAX_DELAY": 10,
    "CONCURRENT_REQUESTS": 4,
    "DOWNLOAD_DELAY": 1,
    "RETRY_HTTP_CODES": [429, 500, 502, 503, 504],
    "RETRY_TIMES": 5,
    "DOWNLOADER_MIDDLEWARES": {
        'scrapy.downloadermiddlewares.useragent.UserAgentMiddleware': None,
        'scrapy_user_agents.middlewares.RandomUserAgentMiddleware': 400,
    },
    # Uncomment these lines if you have proxies
    # "ROTATING_PROXY_LIST": [
    #     "http://user:pass@proxy1:8000",
    #     "http://user:pass@proxy2:8000",
    # ],
    # "DOWNLOADER_MIDDLEWARES.update": {
    #     'rotating_proxies.middlewares.RotatingProxyMiddleware': 610,
    #     'rotating_proxies.middlewares.BanDetectionMiddleware': 620,
    # },
}



process = CrawlerProcess(settings)
process.crawl(SimpleSpider)
process.start()
