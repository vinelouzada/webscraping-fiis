from datetime import datetime

import scrapy

from fiis.items import InfoMoneyItem

class InfomoneySpider(scrapy.Spider):
    name = "InfoMoney"
    allowed_domains = ["infomoney.com.br"]

    def start_requests(self):
        fiis_to_search = ["mxrf11", "btlg11", "xpml11"]

        for fi in fiis_to_search:
            url = f"https://www.infomoney.com.br/cotacoes/b3/fii/fundos-imobiliarios-{fi}/"
            yield scrapy.Request(url, callback=self.parse)

    def parse(self, response):
        fii = response.css(".typography__heading--3.spacing--mb1::text").get()
        price = response.css(".typography__display--2-noscale.typography--numeric.spacing--mr1::text").get()
        currency = response.css(".typography__label--2::text").get()
        created_at = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        yield InfoMoneyItem(fii=fii, price=price, currency=currency, created_at=created_at)
