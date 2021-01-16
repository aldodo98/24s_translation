import re

import scrapy
import random

from scrapy import Selector

from Maje.items import Product
from Maje.itemloader import ProductItemLoader
from scrapy.http.headers import Headers
from scrapy_redis.spiders import RedisSpider
import json
from Maje.settings import BOT_NAME
from datetime import datetime
# import datetime
from datetime import datetime
from Maje.items import Product, AttributeBasicInfoClass, MappingClass, ProductAttributeClass, VariableClass
from Maje.itemloader import ProductItemLoader, VariableClassItemLoader


class ProductTaskSpider(RedisSpider):
    # class ProductTaskSpider(scrapy.Spider):
    name = 'ProductTaskSpider'
    redis_key = BOT_NAME + ':ProductTaskSpider'
    allowed_domains = ['fr.maje.com']
    main_url = 'https://fr.maje.com'

    # start_urls = [
    #     'https://fr.maje.com/fr/chaussures/collection/sneakers/120furious/MFACH00437.html?dwvar_MFACH00437_color=O001',
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
        formRequest.headers = Headers(random.choice(self.headers_list))
        return formRequest

    def schedule_next_requests(self):
        for request in self.next_requests():
            request.headers = Headers(random.choice(self.headers_list))
            self.crawler.engine.crawl(request, spider=self)


    def parse(self, response):
        product = Product()
        product['Success'] = response.status == 200
        if response.status == 200:
            self.oriResponse = response
            filterRes = response.css('.product-detail')
            # 获取基本信息
            productItemloader = ProductItemLoader(item=product, response=response)
            productItemloader.add_value('TaskId', response.meta['TaskId'])
            productItemloader.add_value('Name', filterRes.css('span.productSubname::text').get())
            productItemloader.add_value('ShortDescription', '')
            self.Price = filterRes.css('div.product-price span.price-sales::text').get()
            self.OldPrice = filterRes.css('div.product-price span.price-standard::text').get()
            productItemloader.add_value('Price', self.Price)
            productItemloader.add_value('OldPrice', self.OldPrice)
            productItemloader.add_value('LastChangeTime', datetime.utcnow().isoformat())
            productItemloader.add_value('FullDescription', filterRes.css('p[itemprop=description]::text').get())
            img_lis = response.css('.swiper-wrapper>li.swiper-slide img')
            ImageThumbnailUrl = response.css('.swiper-wrapper>li.swiper-slide:nth-child(1) img::attr(src)').get()
            productItemloader.add_value('ImageThumbnailUrl', ImageThumbnailUrl)
            urls = img_lis.css('img::attr(data-src)').extract()
            urls.append(ImageThumbnailUrl)
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
        colorList = response.css('ul.swatches.Color li')
        result = []
        for item in colorList:
            attributeVariable = VariableClass()
            variableClassItemLoader = VariableClassItemLoader(item=attributeVariable, response=response)
            variableClassItemLoader.add_value('DataCode', item.css('::attr("data-code")').get())
            variableClassItemLoader.add_value('NewPrice', self.Price)
            variableClassItemLoader.add_value('OldPrice', self.OldPrice)

            variableClassItemLoader.add_value('Name', item.css('a span::text').get())
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
        list = response.css('.attribute.size li')
        result = []
        for item in list:
            text = item.get()
            selector = Selector(text=text)
            attributeVariable = VariableClass()
            variableClassItemLoader = VariableClassItemLoader(item=attributeVariable, response=text, selector=selector)
            variableClassItemLoader.add_value('DataCode', item.css('li::attr("id")').get())
            variableClassItemLoader.add_value('NewPrice', self.Price)
            variableClassItemLoader.add_value('OldPrice', self.OldPrice)

            variableClassItemLoader.add_css('Name', '.defaultSize::text')
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
        if len(response.css('.attribute.size li')) > 0:
            sizeAttri = self.getSizeAttribute(response)
            result.append(sizeAttri)

        # colorlist = response.css('div.generic-variations')
        if len(response.css('.swatches.Color li')):
            colorAttri = self.getColorAttribute(response)
            result.append(colorAttri)

        return result

    def getColorSquaresRgb(self, response):
        url = re.match(r'^.+?url\((.+?)\)', response).group(1)
        if self.main_url not in url:
            url = self.main_url + url
        return url
