# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html
import json

# useful for handling different item types with a single interface
from itemadapter import ItemAdapter


class FiisPipeline:
    def open_spider(self, spider):
        self.file = open("fiis.jsonl", "a")

    def close_spider(self, spider):
        self.file.close()

    def process_item(self, item, spider):
        if spider.name != "InfoMoney":
            return item
        line = json.dumps(ItemAdapter(item).asdict(), ensure_ascii=False) + "\n"
        self.file.write(line)
        return item

class NewsPipeline:
    def open_spider(self, spider):
        self.file = open("news.jsonl", "a")

    def close_spider(self, spider):
        self.file.close()

    def process_item(self, item, spider):
        if spider.name != "FIIsNoticias":
            return item

        line = json.dumps(ItemAdapter(item).asdict(), ensure_ascii=False) + "\n"
        self.file.write(line)
        return line