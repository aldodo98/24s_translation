# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter
from Celine.items import CategoryTree
from Celine.items import ProductInfo
from Celine.items import Product
from scrapy_redis.pipelines import RedisPipeline


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
