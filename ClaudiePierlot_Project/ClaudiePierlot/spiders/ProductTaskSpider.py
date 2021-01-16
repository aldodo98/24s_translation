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
        # print(receivedDictData)
        # here you can use and FormRequest
        formRequest = scrapy.FormRequest(url=receivedDictData['ProductUrl'], dont_filter=True,
                                         meta={'TaskId': receivedDictData['Id']})
        formRequest.headers = Headers(random.choice(self.headers_list))
        return formRequest

    def schedule_next_requests(self):
        for request in self.next_requests():
            request.headers = Headers(random.choice(self.headers_list))
            self.crawler.engine.crawl(request, spider=self)

    # start_urls = [
    #     'https://fr.claudiepierlot.com/fr/accessoires/chaussures/120affinity/CFACH00183.html?dwvar_CFACH00183_color=B001#start=1',
    # ]
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

    headers_list = [
        # Chrome
        {
            'authority': 'www.marionnaud.fr',
            'cache-control': 'max-age=0',
            'sec-ch-ua': '"Chromium";v="86", "\\"Not\\\\A;Brand";v="99", "Google Chrome";v="86"',
            'sec-ch-ua-mobile': '?0',
            'dnt': '1',
            'upgrade-insecure-requests': '1',
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.75 Safari/537.36',
            'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
            'sec-fetch-site': 'none',
            'sec-fetch-mode': 'navigate',
            'sec-fetch-user': '?1',
            'sec-fetch-dest': 'document',
            'accept-language': 'en,fr;q=0.9,en-US;q=0.8,zh-CN;q=0.7,zh;q=0.6',
        },
        # IE
        {
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
            "Accept-Encoding": "gzip, deflate, br",
            "Accept-Language": "fr-FR,fr;q=0.8,en-US;q=0.7,en;q=0.5,zh-Hans-CN;q=0.3,zh-Hans;q=0.2",
            "Upgrade-Insecure-Requests": "1",
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.102 Safari/537.36 Edge/18.19041",
        },
        # Firefox
        {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:82.0) Gecko/20100101 Firefox/82.0',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
            'Accept-Language': 'en-US,en;q=0.5',
            'Connection': 'keep-alive',
            'Upgrade-Insecure-Requests': '1',
            'Cache-Control': 'max-age=0',
            'TE': 'Trailers',
        }
    ]

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
