from scrapy.loader import ItemLoader
from scrapy.loader.processors import TakeFirst


class CategoryTreeItemLoader(ItemLoader):
    default_output_processor = TakeFirst()


class ProductInfoItemLoader(ItemLoader):
    default_output_processor = TakeFirst()
