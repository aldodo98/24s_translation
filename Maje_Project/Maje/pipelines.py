# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
import json

from itemadapter import ItemAdapter
from scrapy.utils.serialize import ScrapyJSONEncoder
from scrapy_redis.pipelines import RedisPipeline

from Maje.items import CategoryTree, ProductInfo, Product


class JsonPipeline:
    def open_spider(self, spider):
        self.file = open('items.json', 'w', encoding='utf-8')
    def close_spider(self, spider):
        self.file.close()

    def process_item(self, item, spider):
        line = json.dumps(dict(item), cls=ScrapyJSONEncoder) + "\n"
        self.file.writelines(line)
        return item

class RedisPipeline(RedisPipeline):

    def _process_item(self, item, spider):
        if item.__class__ == CategoryTree:
            hName = 'RootTaskSpider:TaskResult'
            hKey = item['Id']
            hValue = self.serialize(item)
            self.server.hset(name=hName, key=hKey, value=hValue)
            return item
        elif item.__class__ == ProductInfo:
            hName = 'GetTreeProductListTaskSpider:TaskResult'
            hKey = item['Id']
            hValue = self.serialize(item)
            self.server.hset(name=hName, key=hKey, value=hValue)
            return item
        elif item.__class__ == Product:
            hName = 'ProductTaskSpider:TaskResult'
            hKey = item['TaskId']
            hValue = self.serialize(item)
            self.server.hset(name=hName, key=hKey, value=hValue)
            return item
