from scrapy.loader import ItemLoader
from scrapy.loader.processors import TakeFirst, MapCompose


def processDefault(values):
    if values is None:
        print('1111111111111111', values, '22222222222222222222222')
        return ''
    else:
        return values


class CategoryTreeItemLoader(ItemLoader):
    default_output_processor = TakeFirst()
    # CategoryLevel5_in = MapCompose(processDefault)
    # CategoryLevel4_in = MapCompose(processDefault)
    # CategoryLevel3_in = MapCompose(processDefault)


class ProductInfoItemLoader(ItemLoader):
    default_output_processor = TakeFirst()
