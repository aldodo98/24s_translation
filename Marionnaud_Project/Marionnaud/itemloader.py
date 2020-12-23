from scrapy.loader import ItemLoader
from itemloaders.processors import TakeFirst, MapCompose
from w3lib.html import remove_tags, replace_escape_chars

main_url = 'https://www.yoox.com'


def url_join(values):
    if values is None or values == '':
        return ''
    if main_url in values:
        return values
    else:
        return main_url + values


def processDefault(values):
    if values is None:
        print('1111111111111111', values, '22222222222222222222222')
        return ''
    else:
        return values

def lowercase_processor(values):
    return values.lower()

# 把值里面的 \t \r \n 替换
def processDesc(values):
    result = replace_escape_chars(values, which_ones=('\t', '\r', '\n'), replace_by=u' ')
    return result

# 把值里面的 3中情况替换
def processDataPrice(values):
    result = replace_escape_chars(values, which_ones='€', replace_by=u'.')
    result = replace_escape_chars(result, which_ones='EUR', replace_by=u'')
    result = replace_escape_chars(result, which_ones=' ', replace_by=u'')
    return result


def convertMultipuleBlankToOne(values):
    return ' '.join(values.split())

class CategoryTreeItemLoader(ItemLoader):
    default_output_processor = TakeFirst()
    # CategoryLevel5_in = MapCompose(processDefault)
    # CategoryLevel4_in = MapCompose(processDefault)
    # CategoryLevel3_in = MapCompose(processDefault)


class ProductInfoItemLoader(ItemLoader):
    default_output_processor = TakeFirst()
    Price_in = MapCompose(remove_tags, processDesc, processDataPrice)
    ProductUrl_in = MapCompose(remove_tags, url_join)

class ProductItemLoader(ItemLoader):
    default_output_processor = TakeFirst()


class VariableClassItemLoader(ItemLoader):
    default_output_processor = TakeFirst()
    DataCode_in = MapCompose(remove_tags, processDesc, convertMultipuleBlankToOne)
    NewPrice_in = MapCompose(remove_tags, processDesc, processDataPrice, convertMultipuleBlankToOne)
    OldPrice_in = MapCompose(remove_tags, processDesc, processDataPrice, convertMultipuleBlankToOne)
    Name_in = MapCompose(remove_tags, processDesc, convertMultipuleBlankToOne)