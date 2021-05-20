import scrapy
import random

from scrapy import Selector


from scrapy.http.headers import Headers
import json
from Dior.settings import BOT_NAME
from datetime import datetime
from Dior.items import Product, AttributeBasicInfoClass, MappingClass, ProductAttributeClass, VariableClass
from Dior.itemloader import ProductItemLoader, VariableClassItemLoader
from scrapy_redis.spiders import RedisSpider


class ProductTaskSpider(RedisSpider):
    # class ProductTaskSpider(scrapy.Spider):
    name = 'ProductTaskSpider'
    redis_key = BOT_NAME + ':ProductTaskSpider'
    main_url = 'https://www.dior.com'
    allowed_domains = ['www.dior.com']
    #
    # start_urls = [
    #     'https://www.dior.cn/zh_cn/products/couture-051R09A1166_X9000-%E7%9F%AD%E6%AC%BE%E8%BF%9E%E8%A1%A3%E8%A3%99-%E9%BB%91%E8%89%B2%E7%BE%8A%E6%AF%9B%E5%92%8C%E6%A1%91%E8%9A%95%E4%B8%9D%E6%B7%B7%E7%BA%BA',
    # ]

    # __init__方法必须按规定写，使用时只需要修改super()里的类名参数即可
    def __init__(self, *args, **kwargs):
        # 修改这里的类名为当前类名
        super(ProductTaskSpider, self).__init__(*args, **kwargs)

    def make_request_from_data(self, data):
        receivedDictData = json.loads(str(data, encoding="utf-8"))
        # print(receivedDictData)
        # here you can use and FormRequest
        formRequest = scrapy.FormRequest(url=receivedDictData['ProductUrl'], dont_filter=True,
                                         meta={'TaskId': receivedDictData['Id']})
        return formRequest

    def parse(self, response):
        product = Product()
        product['Success'] = response.status == 200
        if response.status == 200:
            self.oriResponse = response
            for filterRes in response.css('div.top-content-desktop-right'):
                # 获取基本信息
                text = filterRes.css('div.top-content-desktop-right').get()
                selector = Selector(text=text)
                productItemloader = ProductItemLoader(item=product, response=text, selector=selector)
                productItemloader.add_value('TaskId', response.meta['TaskId'])
                productItemloader.add_css('Name', 'span.multiline-text.product-titles-title::text')
                productItemloader.add_css('ShortDescription', 'span.multiline-text.product-titles-subtitle::text')

                price = response.css('div.product-actions__price span.price-line::text').get()
                if price is None or price == '':
                    price = response.css('span.variation-option-price::text').get()
                productItemloader.add_value('Price', price)
                # productItemloader.add_css('Price', 'div.product-actions__price span.price-line::text')

                img_lis = response.css('div.product-media__image')
                productItemloader.add_value('ImageThumbnailUrl', self.get_thumbnail_url(img_lis))
                urls = img_lis.css('img::attr(src)').extract()

                productItemloader.add_value('LastChangeTime', datetime.utcnow().isoformat())
                productItemloader.add_css('FullDescription', 'div.product-description-item__content')
                item = productItemloader.load_item()
                # 获取属性
                productAttributes = self.getProductAttributes(filterRes)
                item['ImageUrls'] = ','.join(urls)
                item['ProductAttributes'] = productAttributes
                yield item
        else:
            print('error!!!!!')

    def get_thumbnail_url(self, response):
        li = response[0]
        # print(li.get(), 888888888888888888)
        img_url = li.css('img::attr(src)').get()
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
        colorList = response.css('div.generic-variations span.swatch.variation')
        list = response.css('#variation-selection-options li')
        result = []
        for index in range(len(colorList)):
            # colorItem.css('div.image img::attr("src")')
            colorUrl = colorList[index].css('div.image img::attr("src")').get()
            loadItem = self.setSizeOrColorWithDetailInfo(list[index], colorUrl)
            result.append(loadItem)
            # attributeVariable = VariableClass()
            # variableClassItemLoader = VariableClassItemLoader(item=attributeVariable, response=response)
            # variableClassItemLoader.add_value('DataCode', item.css('::attr("data-code")').get())
            # variableClassItemLoader.add_value('NewPrice', item.css('::attr("data-igc-markdown-price")').get())
            # variableClassItemLoader.add_value('OldPrice', item.css('::attr("data-price")').get())
            #
            # variableClassItemLoader.add_value('Name', item.css('::text').get())
            # variableClassItemLoader.add_value('ColorSquaresRgb', item.css('::attr("data-color")').get())
            # variableClassItemLoader.add_value('DisplayColorSquaresRgb', False)
            # variableClassItemLoader.add_value('PriceAdjustment', 0)
            # variableClassItemLoader.add_value('PriceAdjustmentUsePercentage', False)
            #
            # variableClassItemLoader.add_value('IsPreSelected', len(item.css('span.selected')) > 0)
            # variableClassItemLoader.add_value('DisplayOrder', False)
            # variableClassItemLoader.add_value('DisplayImageSquaresPicture', False)
            # variableClassItemLoader.add_value('PictureUrlInStorage', '')
            # loadItem = variableClassItemLoader.load_item()

        return result

    def getSizeVariables(self, response):
        list = response.css('#variation-selection-options li')
        list2 = response.css('#size-selector-options li')
        result = []
        for item in (list if len(list) > 0 else list2):
            # text = item.get()
            # selector = Selector(text=text)
            # attributeVariable = VariableClass()
            # variableClassItemLoader = VariableClassItemLoader(item=attributeVariable, response=text, selector=selector)
            # variableClassItemLoader.add_value('DataCode', item.css('li::attr("id")').get())
            # variableClassItemLoader.add_css('NewPrice', 'span.variation-option-price::text')
            # variableClassItemLoader.add_value('OldPrice', '')
            #
            # variableClassItemLoader.add_css('Name', '.variation-option-infos-titles span::text')
            # variableClassItemLoader.add_value('ColorSquaresRgb', '')
            # variableClassItemLoader.add_value('DisplayColorSquaresRgb', False)
            # variableClassItemLoader.add_value('PriceAdjustment', 0)
            # variableClassItemLoader.add_value('PriceAdjustmentUsePercentage', False)
            #
            # variableClassItemLoader.add_value('IsPreSelected', len(item.css('span.is-selected')) > 0)
            # variableClassItemLoader.add_value('DisplayOrder', False)
            # variableClassItemLoader.add_value('DisplayImageSquaresPicture', False)
            # variableClassItemLoader.add_value('PictureUrlInStorage', '')
            # loadItem = variableClassItemLoader.load_item()
            loadItem = self.setSizeOrColorWithDetailInfo(item)
            result.append(loadItem)
        return result

    def getProductAttributes(self, response):
        result = []
        # 美妆类
        sizeLinklist = response.css('#variation-selection-options li')
        # 鞋靴类
        sizeLinklist2 = response.css('#size-selector-options li')
        colorSelectorList = response.css('div.generic-variations span.swatch.variation')
        if (len(sizeLinklist) > 0 or len(sizeLinklist2) > 0) and len(colorSelectorList) == 0:
            sizeAttri = self.getSizeAttribute(response)
            result.append(sizeAttri)

        # colorlist = response.css('div.generic-variations')
        if len(colorSelectorList) > 0:
            colorAttri = self.getColorAttribute(response)
            result.append(colorAttri)

        return result

    def setSizeOrColorWithDetailInfo(self, item, picUrl=''):
        text = item.get()
        selector = Selector(text=text)
        attributeVariable = VariableClass()
        variableClassItemLoader = VariableClassItemLoader(item=attributeVariable, response=text, selector=selector)
        variableClassItemLoader.add_value('DataCode', item.css('li::attr("id")').get())
        variableClassItemLoader.add_css('NewPrice', 'span.variation-option-price::text')
        variableClassItemLoader.add_value('NewPrice', self.oriResponse.css('div.product-actions__price span.price-line::text').get())
        variableClassItemLoader.add_value('OldPrice', '')

        variableClassItemLoader.add_css('Name', '.variation-option-infos-titles span::text')
        variableClassItemLoader.add_css('Name', '.size-title::text')

        variableClassItemLoader.add_value('ColorSquaresRgb', '')
        variableClassItemLoader.add_value('ColorSquaresRgb', picUrl)
        variableClassItemLoader.add_value('DisplayColorSquaresRgb', False)
        variableClassItemLoader.add_value('PriceAdjustment', 0)
        variableClassItemLoader.add_value('PriceAdjustmentUsePercentage', False)

        variableClassItemLoader.add_value('IsPreSelected', len(item.css('span.is-selected')) > 0)
        variableClassItemLoader.add_value('DisplayOrder', False)
        variableClassItemLoader.add_value('DisplayImageSquaresPicture', False)
        variableClassItemLoader.add_value('PictureUrlInStorage', '')
        loadItem = variableClassItemLoader.load_item()
        return loadItem

    @staticmethod
    def get_prefume_price(text):
        if text.replace('\n', '').strip() == '':
            return False
        return text.split('-')[1]

    @staticmethod
    def get_prefume_name(text):
        return text.split('-')[0]
