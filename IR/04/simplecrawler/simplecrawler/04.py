import scrapy
from urllib.parse import urlparse


class BasicSpider(scrapy.Spider):
    name = "basic"

    def __init__(self, start_url=None, max_pages=10, *args, **kwargs):
        super().__init__(*args, **kwargs)

        if not start_url:
            raise ValueError("Please provide a seed URL using -a start_url=...")

        self.start_urls = [start_url]
        self.max_pages = int(max_pages)
        self.crawled = 0

        # Restrict crawling to the seed URL's domain
        self.allowed_domains = [urlparse(start_url).hostname]

    def parse(self, response):
        self.crawled += 1

        # Extract and report the page title and URL
        title = response.css("title::text").get(default="No title").strip()

        yield {
            "title": title,
            "url": response.url
        }

        self.logger.info(
            "Crawled %s/%s: %s",
            self.crawled, self.max_pages, response.url
        )

        # Stop when the page limit is reached
        if self.crawled >= self.max_pages:
            self.crawler.engine.close_spider(
                self, reason="page_limit_reached"
            )
            return

        # Extract hyperlinks and follow them recursively
        for link in response.css("a::attr(href)").getall():
            if link:
                yield response.follow(link, callback=self.parse)

