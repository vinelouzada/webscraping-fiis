import scrapy

from fiis.items import InfoMoneyItem

class InfomoneySpider(scrapy.Spider):
    name = "InfoMoney"
    allowed_domains = ["infomoney.com.br"]
    start_urls = ["https://www.infomoney.com.br/cotacoes/b3/fii/fundos-imobiliarios-mxrf11/"]

    def parse(self, response):
        fii = response.css(".typography__heading--3.spacing--mb1::text").get()
        price = response.css(".typography__display--2-noscale.typography--numeric.spacing--mr1::text").get()
        currency = response.css(".typography__label--2::text").get()

        yield InfoMoneyItem(fii=fii, price=price, currency=currency)
