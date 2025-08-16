import scrapy

from datetime import datetime
from fiis.items import NewsItem


class MoneytimesSpider(scrapy.Spider):
    name = "MoneyTimes"
    allowed_domains = ["www.moneytimes.com.br"]
    start_urls = ["https://www.moneytimes.com.br/ultimas-noticias/"]

    def parse(self, response):
        links = response.css(".news-item > figure > a::attr(href)").extract()

        for link in links:
            yield response.follow(link, self.parse_article)

    def parse_article(self, response):
        title_selector = response.css(".single_title::text")
        body_selector = response.css(".single_block_news_text p *::text, .single_block_news_text h2 *::text, .single_block_news_text table *::text")
        published_at_selector = response.css(".single_meta_author_infos_date_time::text")

        title = "".join(title_selector.extract()).strip()
        body = " ".join(body_selector.extract()).strip()
        published_at = published_at_selector.get().strip()
        url = response.url
        source = self.name
        created_at = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        yield NewsItem(title=title, body=body, published_at=published_at, url=url, source=source, created_at=created_at)