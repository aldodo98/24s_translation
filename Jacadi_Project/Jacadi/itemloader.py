from scrapy.loader import ItemLoader
from itemloaders.processors import TakeFirst, MapCompose
from w3lib.html import remove_tags, replace_escape_chars

main_url = 'http://www.jacadi.fr'

def lowercase_processor(values):
    return values.lower()


def processDesc(values):
    result = replace_escape_chars(values, which_ones=('\t', '\r', '\n'), replace_by=u' ')
    return result


def processDataPrice(values):
    result = replace_escape_chars(values, which_ones='€', replace_by=u'')
    result = replace_escape_chars(result, which_ones='EUR', replace_by=u'')
    result = replace_escape_chars(result, which_ones=' ', replace_by=u'')
    # result = replace_escape_chars(result, which_ones='.', replace_by=u'')
    return result


def convertMultipuleBlankToOne(values):
    return ' '.join(values.split())


def url_join(values):
    if values is None or values == '':
        return ''
    if main_url in values:
        return values
    else:
        return main_url + values

def do_strip(values):
    return values and values.strip()

class CategoryTreeItemLoader(ItemLoader):
    default_output_processor = TakeFirst()
    Level_Url_in = MapCompose(remove_tags, url_join)
    CategoryLevel1_in = MapCompose(remove_tags, processDesc, do_strip)
    CategoryLevel2_in = MapCompose(remove_tags, processDesc, do_strip)
    CategoryLevel3_in = MapCompose(remove_tags, processDesc, do_strip)
    CategoryLevel4_in = MapCompose(remove_tags, processDesc, do_strip)
    CategoryLevel5_in = MapCompose(remove_tags, processDesc, do_strip)


class ProductInfoItemLoader(ItemLoader):
    default_output_processor = TakeFirst()
    ProductUrl_in = MapCompose(remove_tags, url_join)
    Price_in = MapCompose(remove_tags, processDesc, processDataPrice)


class ProductItemLoader(ItemLoader):
    default_output_processor = TakeFirst()
    FullDescription_in = MapCompose(remove_tags, processDesc, processDataPrice, convertMultipuleBlankToOne)
    Price_in = MapCompose(remove_tags, processDesc, processDataPrice, convertMultipuleBlankToOne)
    Name_in = MapCompose(remove_tags, processDesc)
    ImageThumbnailUrl_in = MapCompose(remove_tags, url_join)


class VariableClassItemLoader(ItemLoader):
    default_output_processor = TakeFirst()
    DataCode_in = MapCompose(remove_tags, processDesc, convertMultipuleBlankToOne)
    NewPrice_in = MapCompose(remove_tags, processDesc, processDataPrice, convertMultipuleBlankToOne)
    OldPrice_in = MapCompose(remove_tags, processDesc, processDataPrice, convertMultipuleBlankToOne)
    Name_in = MapCompose(remove_tags, processDesc, convertMultipuleBlankToOne)