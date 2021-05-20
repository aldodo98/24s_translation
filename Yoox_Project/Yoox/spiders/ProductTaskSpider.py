import scrapy
import json
import random
import re
from Yoox.settings import BOT_NAME
from scrapy.http.headers import Headers
from scrapy_redis.spiders import RedisSpider
# from datetime import datetime
# import datetime
from datetime import datetime
from Yoox.items import Product, AttributeBasicInfoClass, MappingClass, ProductAttributeClass, VariableClass
from Yoox.itemloader import ProductItemLoader, VariableClassItemLoader


# class ProducttaskspiderSpider(scrapy.Spider):
class ProducttaskspiderSpider(RedisSpider):
    name = 'ProductTaskSpider'
    allowed_domains = ['www.yoox.com']
    redis_key = BOT_NAME + ':ProductTaskSpider'

    # __init__方法必须按规定写，使用时只需要修改super()里的类名参数即可
    def __init__(self, *args, **kwargs):
        # 修改这里的类名为当前类名
        super(ProducttaskspiderSpider, self).__init__(*args, **kwargs)

    def make_request_from_data(self, data):
        receivedDictData = json.loads(str(data, encoding="utf-8"))
        # print(receivedDictData)
        # here you can use and FormRequest
        formRequest = scrapy.FormRequest(url=receivedDictData['ProductUrl'], dont_filter=True,
                                         meta={'TaskId': receivedDictData['Id']})
        return formRequest

    def parse(self, response):
        try:
            return self.parse_res(response=response)
        except Exception as err:
            print(err)

    def parse_res(self, response):
        product = Product()
        product['Success'] = response.status == 200
        if response.status == 200:
            product_itemloader = ProductItemLoader(item=product, response=response)
            product_itemloader.add_value('TaskId', response.meta['TaskId'])
            # product_itemloader.add_value('TaskId', 'XXXXXXXXXX')

            product_itemloader.add_value('Name', self.get_product_name(response))
            product_itemloader.add_value('ShortDescription', '')

            product_itemloader.add_value('FullDescription', self.get_product_desc(response))

            product_itemloader.add_value('Price', self.get_product_price(response))
            product_itemloader.add_value('OldPrice', response.css('div#item-price div.text-secondary').get())

            product_itemloader.add_value(
                'ImageThumbnailUrl',
                response.css('div#openZoom img::attr(src)').get())

            # product_itemloader.add_value(
            #     'ImageUrls', [])

            product_itemloader.add_value('LastChangeTime', datetime.utcnow().isoformat())
            product_itemloader.add_value('HashCode', '')
            loadItem = product_itemloader.load_item()
            # 暂时没有看到有选项的 size 或者 color 或者等等提供选项的
            product_attributes = self.get_product_attributes(response)
            loadItem['ImageUrls'] = self.get_img_urls(response)
            loadItem['ProductAttributes'] = product_attributes
            yield loadItem

    def get_product_name(self, response):
        title = response.css('div#itemTitle').get()
        return title

    def get_product_desc(self, response):
        # dr = re.compile(r'<[^>]+>', re.S)
        # dd = dr.sub('', response.css('div.product_desc p').get())
        return response.css('li#itemDescription div.info-body::text').get()

    def get_product_price(self, response):
        return response.css('div.font-bold span[itemprop=price]').get()

    def get_thumbnail_url(self, response):
        img = response[0]
        img_url = img.css('::attr(src)').get()
        return img_url

    def get_img_urls(self, response):
        urls = response.css('ul#itemThumbs img')
        if urls is not None:
            return ','.join(urls.css('::attr(src)').extract())
        else:
            return ''

    def get_product_attributes(self, response):
        result = []
        size_link_list = response.css('div#itemSizes li')
        if len(size_link_list) > 0:
            size_attr = self.get_size_attribute(response)
            result.append(size_attr)

        color_list = response.css('div#itemColors li')
        if len(color_list) > 0:
            color_attr = self.get_color_attribute(response)
            result.append(color_attr)

        return result

    def get_size_attribute(self, response):
        # attributeBasicInfo
        attributeBasicInfo = AttributeBasicInfoClass()
        attributeBasicInfo['Name'] = "Size"
        attributeBasicInfo['Description'] = ""

        # mapping
        mapping = MappingClass()
        mapping['TextPrompt'] = "Size"
        mapping['IsRequired'] = True
        mapping['AttributeControlTypeId'] = 2
        mapping['AttributeControlType'] = "RadioList"
        mapping['DisplayOrder'] = 0
        mapping['DefaultValue'] = ""

        productSiteAttribute = ProductAttributeClass()
        productSiteAttribute['AttributeBasicInfo'] = attributeBasicInfo
        productSiteAttribute['Mapping'] = mapping
        productSiteAttribute['Variables'] = self.get_size_variables(response)

        return productSiteAttribute

    def get_color_attribute(self, response):
        # attributeBasicInfo
        attribute_basic_info = AttributeBasicInfoClass()
        attribute_basic_info['Name'] = "Color"
        attribute_basic_info['Description'] = ""

        # mapping
        mapping = MappingClass()
        mapping['TextPrompt'] = "Color"
        mapping['IsRequired'] = True
        mapping['AttributeControlTypeId'] = 2
        mapping['AttributeControlType'] = "RadioList"
        mapping['DisplayOrder'] = 0
        mapping['DefaultValue'] = ""

        product_site_attribute = ProductAttributeClass()
        product_site_attribute['AttributeBasicInfo'] = attribute_basic_info
        product_site_attribute['Mapping'] = mapping
        product_site_attribute['Variables'] = self.get_color_variables(response)

        return product_site_attribute

    def get_size_variables(self, response):
        lis = response.css('div#itemSizes li')
        result = []
        for item in lis:
            attribute_variable = VariableClass()
            variable_class_item_ioader = VariableClassItemLoader(item=attribute_variable)
            variable_class_item_ioader.add_value('DataCode', '')

            variable_class_item_ioader.add_value('NewPrice', self.get_product_price(response))
            variable_class_item_ioader.add_value('Name', item.css('::attr(title)').get())

            variable_class_item_ioader.add_value('OldPrice', response.css('div#item-price span.text-secondary').get())
            variable_class_item_ioader.add_value('ColorSquaresRgb', '')
            variable_class_item_ioader.add_value('DisplayColorSquaresRgb', False)
            variable_class_item_ioader.add_value('PriceAdjustment', 0)
            variable_class_item_ioader.add_value('PriceAdjustmentUsePercentage', False)

            variable_class_item_ioader.add_value('IsPreSelected', self.judge_variable_is_preselect(item.css('::attr(class)').get()))
            variable_class_item_ioader.add_value('DisplayOrder', False)
            variable_class_item_ioader.add_value('DisplayImageSquaresPicture', False)
            variable_class_item_ioader.add_value('PictureUrlInStorage', '')
            loadItem = variable_class_item_ioader.load_item()
            result.append(loadItem)
        return result

    def get_color_variables(self, response):
        list = response.css('div#itemColors li')
        result = []
        for item in list:
            attribute_variable = VariableClass()
            variable_class_item_loader = VariableClassItemLoader(item=attribute_variable, response=response)
            variable_class_item_loader.add_value('DataCode', '')
            variable_class_item_loader.add_value('NewPrice', self.get_product_price(response))
            variable_class_item_loader.add_value('OldPrice', response.css('div#item-price span.text-secondary').get())

            variable_class_item_loader.add_value('Name', item.css('div::attr(style)').get())
            variable_class_item_loader.add_value('ColorSquaresRgb', item.css('div::attr(style)').get())
            variable_class_item_loader.add_value('DisplayColorSquaresRgb', False)
            variable_class_item_loader.add_value('PriceAdjustment', 0)
            variable_class_item_loader.add_value('PriceAdjustmentUsePercentage', False)

            variable_class_item_loader.add_value('IsPreSelected', self.judge_variable_is_preselect(item.css('::attr(class)').get()))
            variable_class_item_loader.add_value('DisplayOrder', False)
            variable_class_item_loader.add_value('DisplayImageSquaresPicture', False)
            variable_class_item_loader.add_value('PictureUrlInStorage', '')
            loadItem = variable_class_item_loader.load_item()
            result.append(loadItem)
        return result

    def judge_variable_is_preselect(self, classname):
        print(classname, 5555555555555555)
        return 'selected' in classname

