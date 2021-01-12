import scrapy
import random
from Matchfashion.items import Product
from Matchfashion.itemloader import ProductItemLoader
from scrapy.http.headers import Headers
from scrapy_redis.spiders import RedisSpider
import json
from Matchfashion.settings import BOT_NAME
from datetime import datetime
import time
from Matchfashion.items import Product, AttributeBasicInfoClass, MappingClass, ProductAttributeClass, VariableClass
from Matchfashion.itemloader import ProductItemLoader, VariableClassItemLoader


class ProductTaskSpider(RedisSpider):
# class ProductTaskSpider(scrapy.Spider):
    name = 'ProductTaskSpider'
    redis_key = BOT_NAME + ':ProductTaskSpider'
    allowed_domains = ['www.matchesfashion.com']
    request_url = 'https://www.matchesfashion.com/ajax/p/'

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

    # def start_requests(self):
    #     urls = [
    #         # 'https://www.matchesfashion.com/intl/products/Socksss-Cosmic-Blast-tie-dye-organic-cotton-blend-socks-1395588',
    #         # 'https://www.matchesfashion.com/intl/products/Chlo%C3s%A9-Darryl-medium-leather-shoulder-bag-1361382',
    #         'https://www.matchesfashion.com/intl/products/Jil-Sander-Ribbed-sole-leather-trainers-1384715'
    #     ]
    #     for url in urls:
    #         yield scrapy.Request(url=url, callback=self.parse, headers=random.choice(self.headers_list), meta={
    #             'TaskId': 1
    #         })


    def parse(self, response):
        if response.status == 200:
            product_id = response.css('#currentProductId::attr(value)').get()
            yield scrapy.Request(url=self.request_url + product_id + '?_=' + str(round(time.time() * 1000)), callback=self.parse_res, headers=random.choice(self.headers_list), meta={
                'TaskId': response.meta['TaskId'],
                'HtmlResponse': response
            })

        else:
            print('error!!!!!')

    def parse_res(self, response):
        product = Product()
        product['Success'] = response.status == 200
        html_response = response.meta['HtmlResponse']
        if response.status == 200:
            product_attributes = json.loads(response.text)

            product_itemloader = ProductItemLoader(item=product, response=html_response)
            product_itemloader.add_value('TaskId', response.meta['TaskId'])
            # product_itemloader.add_value('TaskId', 'XXXXXXXXXX')

            product_itemloader.add_value('Name', html_response.css('h1.pdp-headline').get())
            product_itemloader.add_value('ShortDescription', '')

            product_itemloader.add_value('FullDescription', html_response.css('div#mCSB_1_container div.scroller-content').get())

            self.Price = self.getProductPrice(html_response)
            self.OldPrice = html_response.css('p.pdp-price strike::text').get()
            product_itemloader.add_value('Price', self.Price)
            product_itemloader.add_value('OldPrice', self.OldPrice)
            img_urls = html_response.css('div.gallery-panel__main-image-carousel>div')
            product_itemloader.add_value(
                'ImageThumbnailUrl',
                img_urls[0].css('img::attr(src)').get())
            product_itemloader.add_value(
                'ImageUrls',
                ','.join(img_urls.css('img::attr(src)').getall()))
            # product_itemloader.add_value(
            #     'ImageUrls', [])

            product_itemloader.add_value('LastChangeTime', datetime.utcnow().isoformat())
            product_itemloader.add_value('HashCode', '')
            loadItem = product_itemloader.load_item()
            # 暂时没有看到有选项的 size 或者 color 或者等等提供选项的
            product_attributes = self.getProductAttributes(product_attributes)
            loadItem['ProductAttributes'] = product_attributes
            yield loadItem
        else:
            print('error!!!!!')

    def getProductPrice(self, response):
        price = response.css('p.pdp-price span.pdp-price__hilite')
        if len(price) > 0:
            return price.get()
        else:
            return response.css('p.pdp-price::text').get()

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
            variableClassItemLoader.add_value('ColorSquaresRgb', item.css('a::attr("style")').get())
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
        result = []
        for item in response:
            attributeVariable = VariableClass()
            variableClassItemLoader = VariableClassItemLoader(item=attributeVariable)
            # variableClassItemLoader.add_value('DataCode', item.css('li::attr("id")').get())
            variableClassItemLoader.add_value('NewPrice', self.Price)
            variableClassItemLoader.add_value('OldPrice', self.OldPrice)

            variableClassItemLoader.add_value('Name', item['sizeData']['value'])
            variableClassItemLoader.add_value('ColorSquaresRgb', '')
            variableClassItemLoader.add_value('DisplayColorSquaresRgb', False)
            variableClassItemLoader.add_value('PriceAdjustment', 0)
            variableClassItemLoader.add_value('PriceAdjustmentUsePercentage', False)

            variableClassItemLoader.add_value('IsPreSelected', False)
            variableClassItemLoader.add_value('DisplayOrder', False)
            variableClassItemLoader.add_value('DisplayImageSquaresPicture', False)
            variableClassItemLoader.add_value('PictureUrlInStorage', '')
            loadItem = variableClassItemLoader.load_item()
            result.append(loadItem)
        return result

    def getProductAttributes(self, response):
        result = []
        # product_id = response.css('#currentProductId::attr(value)').get()

        if 'variantOptions' in response:
            sizeAttri = self.getSizeAttribute(response['variantOptions'])
            result.append(sizeAttri)

        # if len(response.css('.swatches.Color li')):
        #     colorAttri = self.getColorAttribute(response)
        #     result.append(colorAttri)

        return result

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