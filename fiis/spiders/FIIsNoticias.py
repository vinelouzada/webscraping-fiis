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
        body_selector = response.css(".newsContent__article p *::text, .newsContent__article h2 *::text, .newsContent__article table *::text")
        published_at_selector = response.css(".contentInfo__desc > ul > li::text")

        title = "".join(title_selector.extract()).strip()
        body = " ".join(body_selector.extract()).strip()
        published_at = published_at_selector.get().strip()
        url = response.url
        source = self.name
        created_at = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        yield FIIsNoticiasItem(title=title, body=body, published_at=published_at, url=url, source=source, created_at=created_at)
