from scrapy.loader import ItemLoader
from scrapy.loader.processors import TakeFirst, MapCompose
from w3lib.html import remove_tags, replace_escape_chars

def lowercase_processor(values):
    return values.lower()


def processDesc(values):
    result = replace_escape_chars(values, which_ones=('\t', '\r', '\n'), replace_by=u' ')
    return result


def processDataPrice(values):
    result = replace_escape_chars(values, which_ones='€', replace_by=u'.')
    result = replace_escape_chars(result, which_ones='EUR', replace_by=u'')
    return result


def convertMultipuleBlankToOne(values):
    return ' '.join(values.split())


class CategoryTreeItemLoader(ItemLoader):
    default_output_processor = TakeFirst()


class ProductInfoItemLoader(ItemLoader):
    default_output_processor = TakeFirst()
    Price_in = MapCompose(remove_tags, processDesc, processDataPrice, convertMultipuleBlankToOne)
    ProductName_in = MapCompose(remove_tags, processDesc)

class ProductItemLoader(ItemLoader):
    default_output_processor = TakeFirst()
    FullDescription_in = MapCompose(remove_tags, processDesc, processDataPrice, convertMultipuleBlankToOne)
    Price_in = MapCompose(remove_tags, processDesc, processDataPrice, convertMultipuleBlankToOne)
    Name_in = MapCompose(remove_tags, processDesc)


class VariableClassItemLoader(ItemLoader):
    default_output_processor = TakeFirst()
    DataCode_in = MapCompose(remove_tags, processDesc, convertMultipuleBlankToOne)
    NewPrice_in = MapCompose(remove_tags, processDesc, processDataPrice, convertMultipuleBlankToOne)
    OldPrice_in = MapCompose(remove_tags, processDesc, processDataPrice, convertMultipuleBlankToOne)
    Name_in = MapCompose(remove_tags, processDesc, convertMultipuleBlankToOne)
    FullDescription_in = MapCompose(remove_tags, processDesc)