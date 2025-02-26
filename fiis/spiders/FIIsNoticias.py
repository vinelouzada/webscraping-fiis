import scrapy

from datetime import datetime
from fiis.items import FIIsNoticias


class FiisnoticiasSpider(scrapy.Spider):
    name = "FIIsNoticias"
    allowed_domains = ["fiis.com.br"]
    start_urls = ["https://fiis.com.br/noticias"]

    def parse(self, response):
       links = response.css(".wrapper.moreNews .loopNoticias > a::attr(href)").extract()

       for link in links:
           yield response.follow(link, self.parse_article)

    def parse_article(self, response):
        title = "".join(response.css(".newsContent__article > h1::text").extract())
        body = "".join(response.css(".newsContent__article p::text").extract()).strip()
        created_at = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        yield FIIsNoticias(title=title, body=body, created_at=created_at)