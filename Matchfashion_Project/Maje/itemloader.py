from scrapy.loader import ItemLoader
from scrapy.loader.processors import TakeFirst, MapCompose
from itemloaders import ItemLoader
from itemloaders.processors import TakeFirst, MapCompose, Join
from w3lib.html import remove_tags, replace_escape_chars

def handleTest(val):
    return val+'handled'

class ScrapyTestItemLoader(ItemLoader):
    default_output_processor = TakeFirst()
    test_in = MapCompose(handleTest)
    test_out = Join()
def lowercase_processor(values):
    return values.lower()


def processDesc(values):
    result = replace_escape_chars(values, which_ones=('\t', '\r', '\n'), replace_by=u' ')
    return result

def process_strip(values):
    return values.strip()


def processDataPrice(values):
    result = replace_escape_chars(values, which_ones='€', replace_by=u'.')
    return result


def convertMultipuleBlankToOne(values):
    return ' '.join(values.split())


class MarionnaudItemLoader(ItemLoader):
    default_output_processor = TakeFirst()



class VariableClassItemLoader(ItemLoader):
    default_output_processor = TakeFirst()
    DataCode_in = MapCompose(remove_tags, processDesc, convertMultipuleBlankToOne)
    NewPrice_in = MapCompose(remove_tags, processDesc, processDataPrice, convertMultipuleBlankToOne)
    OldPrice_in = MapCompose(remove_tags, processDesc, processDataPrice, convertMultipuleBlankToOne)
    Name_in = MapCompose(remove_tags, processDesc, convertMultipuleBlankToOne)

def processDefault(values):
    if values is None:
        print('1111111111111111', values, '22222222222222222222222')
        return ''
    else:
        return values


class CategoryTreeItemLoader(ItemLoader):
    default_output_processor = TakeFirst()
    CategoryLevel1_in = MapCompose(processDesc, process_strip)
    CategoryLevel2_in = MapCompose(processDesc, process_strip)
    CategoryLevel3_in = MapCompose(processDesc, process_strip)


class ProductInfoItemLoader(ItemLoader):
    default_output_processor = TakeFirst()
    ProductName_in = MapCompose(processDesc, process_strip)