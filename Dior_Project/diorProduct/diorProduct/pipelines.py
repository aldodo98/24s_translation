# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter
import json

from scrapy.utils.serialize import ScrapyJSONEncoder


class ScrapytestPipeline:
    def open_spider(self, spider):
        self.file = open('items.json', 'w', encoding='utf-8')

    def close_spider(self, spider):
        self.file.close()

    def process_item(self, item, spider):
        line = json.dumps(dict(item), cls=ScrapyJSONEncoder) + "\n"
        self.file.writelines(line)
        return item

class JsonPipeline:
    def open_spider(self, spider):
        print("json pipeline start")

    def close_spider(self, spider):
        print("json pipeline close")

    def process_item(self, item, spider):
        line = json.dumps(dict(item), cls=ScrapyJSONEncoder) + "\n"
        print(line)
        return item
