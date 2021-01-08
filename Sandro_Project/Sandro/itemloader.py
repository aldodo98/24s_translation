from scrapy.loader import ItemLoader
from itemloaders.processors import TakeFirst, MapCompose
from w3lib.html import remove_tags, replace_escape_chars
import re

main_url = 'https://fr.sandro-paris.com'


def url_join(values):
    if values is None or values == '':
        return ''
    if main_url in values:
        return values
    else:
        return main_url + values


def do_strip(values):
    return values and values.strip()


def lowercase_processor(values):
    return values.lower()

def format_color_style(values):
    result = re.findall(r"[(](.*?)[)]", values)
    if len(result) > 0:
        return result[0]
    else:
        return values


def processDesc(values):
    result = replace_escape_chars(values, which_ones=('\t', '\r', '\n'), replace_by=u' ')
    return result


def processDataPrice(values):
    result = replace_escape_chars(values, which_ones='€', replace_by=u'.')
    result = replace_escape_chars(result, which_ones='EUR', replace_by=u'')
    result = replace_escape_chars(result, which_ones=' ', replace_by=u'')
    return result


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


def convertMultipuleBlankToOne(values):
    return ' '.join(values.split())


class ProductItemLoader(ItemLoader):
    default_output_processor = TakeFirst()
    Price_in = MapCompose(remove_tags, processDesc, processDataPrice)
    OldPrice_in = MapCompose(remove_tags, processDesc, processDataPrice)
    Name_in = MapCompose(remove_tags, processDesc, do_strip)
    FullDescription_in = MapCompose(remove_tags, do_strip)
    ImageThumbnailUrl_in = MapCompose(remove_tags, url_join)


class VariableClassItemLoader(ItemLoader):
    default_output_processor = TakeFirst()
    DataCode_in = MapCompose(remove_tags, processDesc, convertMultipuleBlankToOne)
    NewPrice_in = MapCompose(remove_tags, processDesc, processDataPrice)
    OldPrice_in = MapCompose(remove_tags, processDesc, processDataPrice)
    Name_in = MapCompose(remove_tags, format_color_style, processDesc, convertMultipuleBlankToOne, do_strip)
    ColorSquaresRgb_in = MapCompose(remove_tags, format_color_style, url_join, processDesc)
