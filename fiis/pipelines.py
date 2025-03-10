# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html
import json
import pymongo
import logging
logging.getLogger("pymongo").setLevel(logging.WARNING)

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
        return item


class MongoPipeline:
    COLLECTION_MAP = {
        "FIIsNoticias": "news",
        "InfoMoney": "quotes"
    }

    def __init__(self, mongo_uri, mongo_db):
        self.mongo_uri = mongo_uri
        self.mongo_db = mongo_db

    @classmethod
    def from_crawler(cls, crawler):
        return cls(
            mongo_uri=crawler.settings.get("MONGO_URI"),
            mongo_db=crawler.settings.get("MONGO_DATABASE"),
        )

    def open_spider(self, spider):
        self.client = pymongo.MongoClient(self.mongo_uri)
        self.db = self.client[self.mongo_db]

    def close_spider(self, spider):
        self.client.close()

    def process_item(self, item, spider):
        collection_name = self.COLLECTION_MAP.get(spider.name)
        if collection_name:
            line = json.dumps(ItemAdapter(item).asdict(), ensure_ascii=False)
            self.db[collection_name].insert_one(json.loads(line))
            return item

        else:
            spider.logger.error(f"Item inválido recebido (não é um dicionário): {item}")
            return item