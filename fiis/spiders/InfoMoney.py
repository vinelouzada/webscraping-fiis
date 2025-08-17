from datetime import datetime

import scrapy

from fiis.items import NewsItem


class InfomoneySpider(scrapy.Spider):
    name = "InfoMoney"
    allowed_domains = ["infomoney.com.br"]
    start_urls = ["https://www.infomoney.com.br/mercados/"]

    def parse(self, response):
        links = response.css("div[data-ds-component='card-sm'] > div > div > div > a::attr(href)").extract()

        for link in links:
            yield response.follow(link, self.parse_article)

    def parse_article(self, response):
        title_selector = response.css("h1::text")
        body_selector = response.css("article[data-ds-component='article'] p *::text, article[data-ds-component='article'] h2 *::text, article[data-ds-component='article'] table *::text")
        published_at_selector = response.css('time::text')

        title = "".join(title_selector.extract()).strip()
        body = " ".join(body_selector.extract()).strip()
        published_at = published_at_selector.get().strip()
        url = response.url
        source = self.name
        created_at = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        yield NewsItem(title=title, body=body, published_at=published_at, url=url, source=source, created_at=created_at)
