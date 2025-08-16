import scrapy

from fiis.items import NewsItem
from datetime import datetime


class CnnbrasilSpider(scrapy.Spider):
    name = "CNNBrasil"
    allowed_domains = ["www.cnnbrasil.com.br"]
    start_urls = ["https://www.cnnbrasil.com.br/tudo-sobre/mercado-financeiro/"]

    def parse(self, response):
        links = response.css("ul[data-section='article_list'] > li > figure > a::attr(href)").extract()

        for link in links:
            yield response.follow(link, self.parse_article)

    def parse_article(self, response):
        title_selector = response.css("h1::text")
        body_selector = response.css("div[data-single-content='true'] p *::text, div[data-single-content='true'] h2 *::text, div[data-single-content='true'] table *::text")
        published_at_selector = response.css(".timestamp__date::text")

        title = "".join(title_selector.extract()).strip()
        body = " ".join(body_selector.extract()).strip()
        published_at = published_at_selector.get().strip()
        url = response.url
        source = self.name
        created_at = datetime.now().strftime("%Y-%m-%d %H:%M:%S")


        yield NewsItem(title=title, body=body, published_at=published_at, url=url, source=source, created_at=created_at)
