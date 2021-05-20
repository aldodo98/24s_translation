import re
from datetime import datetime

import scrapy
import json
import random

from ClaudiePierlot.itemloader import VariableClassItemLoader, ProductInfoItemLoader, ProductItemLoader
from ClaudiePierlot.items import Product, AttributeBasicInfoClass, ProductAttributeClass, MappingClass, VariableClass
from scrapy.selector import Selector
from scrapy.loader import ItemLoader
import requests

from scrapy.http.headers import Headers
from scrapy_redis.spiders import RedisSpider

from ClaudiePierlot.settings import BOT_NAME


class ProductTaskSpider(RedisSpider):
    name = 'ProductTaskSpider'
    redis_key = BOT_NAME + ':ProductTaskSpider'
    allowed_domains = ['fr.claudiepierlot.com']
    main_url = 'https://fr.claudiepierlot.com'
    def __init__(self, *args, **kwargs):
        # 修改这里的类名为当前类名
        super(ProductTaskSpider, self).__init__(*args, **kwargs)

    def make_request_from_data(self, data):
        receivedDictData = json.loads(str(data, encoding="utf-8"))
        formRequest = scrapy.FormRequest(url=receivedDictData['ProductUrl'], dont_filter=True,
                                         meta={'TaskId': receivedDictData['Id']})
        return formRequest

    def parse(self, response):
        product = Product()
        product['Success'] = response.status == 200
        if response.status == 200:
            self.oriResponse = response
            filterRes = response.css('.product-detail')
            # 获取基本信息
            text = filterRes.get()
            selector = Selector(text=text)
            productItemloader = ProductItemLoader(item=product, response=text, selector=selector)
            productItemloader.add_value('TaskId', response.meta['TaskId'])
            productItemloader.add_css('Name', 'h1.product-name::text')
            productItemloader.add_value('ShortDescription', '')
            self.Price = filterRes.css('span.price-sales::text').get()
            self.OldPrice = filterRes.css('span.price-standard::text ').get()
            productItemloader.add_value('Price', self.Price)
            productItemloader.add_value('OldPrice', self.OldPrice)
            productItemloader.add_value('LastChangeTime', datetime.utcnow())
            productItemloader.add_css('FullDescription', 'div.jspPane>p::text')
            img_lis = response.css('#main-slide-product .main-image.image-zoom img')
            productItemloader.add_value('ImageThumbnailUrl', self.get_thumbnail_url(img_lis))
            urls = img_lis.css('img::attr(data-src)').extract()
            item = productItemloader.load_item()
            # 获取属性
            productAttributes = self.getProductAttributes(response)
            item['ProductAttributes'] = productAttributes
            item['ImageUrls'] = ','.join(urls)
            yield item
        else:
            print('error!!!!!')

    def get_thumbnail_url(self, response):
        li = response[0]
        # print(li.get(), 888888888888888888)
        img_url = li.css('img::attr(data-src)').get()
        # if img_url is None:
        #     return li.css('video').xpath('@src').get()
        return img_url

    def getColorAttribute(self, response):
        # attributeBasicInfo
        attributeBasicInfo = AttributeBasicInfoClass()
        attributeBasicInfo['Name'] = "Color"
        attributeBasicInfo['Description'] = ""

        # mapping
        mapping = MappingClass()
        mapping['TextPrompt'] = "Color"
        mapping['IsRequired'] = True
        mapping['AttributeControlTypeId'] = 2
        mapping['AttributeControlType'] = "RadioList"
        mapping['DisplayOrder'] = 0
        mapping['DefaultValue'] = ""

        productSiteAttribute = ProductAttributeClass()
        productSiteAttribute['AttributeBasicInfo'] = attributeBasicInfo
        productSiteAttribute['Mapping'] = mapping
        productSiteAttribute['Variables'] = self.getColorVariables(response)

        return productSiteAttribute

    def getSizeAttribute(self, response):
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
        productSiteAttribute['Variables'] = self.getSizeVariables(response)

        return productSiteAttribute

    def getColorVariables(self, response):
        colorList = response.css('.swatchs.Color li')
        result = []
        for item in colorList:
            attributeVariable = VariableClass()
            variableClassItemLoader = VariableClassItemLoader(item=attributeVariable, response=response)
            variableClassItemLoader.add_value('DataCode', item.css('::attr("data-code")').get())
            variableClassItemLoader.add_value('NewPrice', self.Price)
            variableClassItemLoader.add_value('OldPrice', self.OldPrice)

            variableClassItemLoader.add_value('Name', item.css('span[itemprop=color]::text').get())
            variableClassItemLoader.add_value('ColorSquaresRgb', self.getColorSquaresRgb(item.css('a::attr("style")').get()))
            variableClassItemLoader.add_value('DisplayColorSquaresRgb', False)
            variableClassItemLoader.add_value('PriceAdjustment', 0)
            variableClassItemLoader.add_value('PriceAdjustmentUsePercentage', False)

            variableClassItemLoader.add_value('IsPreSelected', len(item.css('.selected')) > 0)
            variableClassItemLoader.add_value('DisplayOrder', False)
            variableClassItemLoader.add_value('DisplayImageSquaresPicture', False)
            variableClassItemLoader.add_value('PictureUrlInStorage', '')
            loadItem = variableClassItemLoader.load_item()
            result.append((loadItem))

        return result

    def getSizeVariables(self, response):

        list = response.css('.siz-list-container .swatchs.size li')
        result = []
        for item in list:
            href = item.css('a::attr("href")').get()
            text = item.get()
            selector = Selector(text=text)
            attributeVariable = VariableClass()
            variableClassItemLoader = VariableClassItemLoader(item=attributeVariable, response=text, selector=selector)
            variableClassItemLoader.add_value('DataCode', item.css('li::attr("id")').get())
            variableClassItemLoader.add_value('NewPrice', self.Price)
            variableClassItemLoader.add_value('OldPrice', self.OldPrice)

            variableClassItemLoader.add_css('Name', '.sizeDisplayValue::text')
            variableClassItemLoader.add_value('ColorSquaresRgb', '')
            variableClassItemLoader.add_value('DisplayColorSquaresRgb', False)
            variableClassItemLoader.add_value('PriceAdjustment', 0)
            variableClassItemLoader.add_value('PriceAdjustmentUsePercentage', False)

            variableClassItemLoader.add_value('IsPreSelected', len(item.css('.selected')) > 0)
            variableClassItemLoader.add_value('DisplayOrder', False)
            variableClassItemLoader.add_value('DisplayImageSquaresPicture', False)
            variableClassItemLoader.add_value('PictureUrlInStorage', '')
            loadItem = variableClassItemLoader.load_item()
            result.append(loadItem)
        return result

    def getProductAttributes(self, response):
        result = []
        if len(response.css('.siz-list-container .swatchs.size li')) > 0:
            sizeAttri = self.getSizeAttribute(response)
            result.append(sizeAttri)

        # colorlist = response.css('div.generic-variations')
        if len(response.css('.swatchs.Color li')):
            colorAttri = self.getColorAttribute(response)
            result.append(colorAttri)

        return result

    def getColorSquaresRgb(self, response):
        url = re.match(r'^.+?url\((.+?)\)', response).group(1)
        if self.main_url not in url:
            url = self.main_url + url
        return url
