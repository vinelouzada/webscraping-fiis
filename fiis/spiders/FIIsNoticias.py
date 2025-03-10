import scrapy

from datetime import datetime
from fiis.items import FIIsNoticiasItem


class FiisnoticiasSpider(scrapy.Spider):
    name = "FIIsNoticias"
    allowed_domains = ["fiis.com.br"]
    start_urls = ["https://fiis.com.br/noticias"]

    def parse(self, response):
        links = response.css(".wrapper.moreNews .loopNoticias > a::attr(href)").extract()

        for link in links:
            yield response.follow(link, self.parse_article)

    def parse_article(self, response):
        title_selector = response.css(".newsContent__article > h1::text")
        body_selector = response.css(".newsContent__article p::text")

        title = "".join(title_selector.extract()).strip()
        body = "".join(body_selector.extract()).strip()
        created_at = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        yield FIIsNoticiasItem(title=title, body=body, created_at=created_at)
