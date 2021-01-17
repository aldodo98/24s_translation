import scrapy
import random
from Sandro.items import Product
from Sandro.itemloader import ProductItemLoader
from scrapy.http.headers import Headers
from scrapy_redis.spiders import RedisSpider
import json
import re
from Sandro.settings import BOT_NAME
from datetime import datetime
# import datetime
from datetime import datetime
from Sandro.items import Product, AttributeBasicInfoClass, MappingClass, ProductAttributeClass, VariableClass
from Sandro.itemloader import ProductItemLoader, VariableClassItemLoader


# class ProductTaskSpider(scrapy.Spider):
class ProductTaskSpider(RedisSpider):
    name = 'ProductTaskSpider'
    allowed_domains = ['fr.sandro-paris.com/']
    redis_key = BOT_NAME + ':ProductTaskSpider'
    main_url = 'https://fr.sandro-paris.com'

    # def start_requests(self):
    #     urls = [
    #         'https://fr.sandro-paris.com/fr/femme-sandro-clara-luciani/bottines-en-cuir/SFACH00535.html?dwvar_SFACH00535_color=44#start=1'
    #     ]
    #
    #     for url in urls:
    #         yield scrapy.Request(url=url, callback=self.parse, headers=random.choice(self.headers_list), meta={
    #             'TaskId': '1'
    #         }, dont_filter=True)

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

            product_itemloader.add_value('Name', response.css('h1#title::text').get())
            product_itemloader.add_value('ShortDescription', '')
            product_itemloader.add_value('FullDescription', response.css('div.shortDescription>div').get())
            #
            product_itemloader.add_value('Price', response.css(
                'span.price-sales::attr(content)').get())
            product_itemloader.add_value('OldPrice', '')
            #
            img_lis = response.css('div.product-images img')

            product_itemloader.add_value(
                'ImageThumbnailUrl',
                self.get_thumbnail_url(img_lis))
            urls = self.get_img_urls(img_lis.css('::attr(src)').getall())

            product_itemloader.add_value('LastChangeTime', datetime.utcnow())
            product_itemloader.add_value('HashCode', '')
            loadItem = product_itemloader.load_item()
            #
            product_attributes = self.get_product_attributes(response)
            if len(urls) > 0:
                urls = urls[:-1]
            loadItem['ImageUrls'] = urls
            loadItem['ProductAttributes'] = product_attributes
            yield loadItem

    def get_product_name(self, response):
        result = ''
        title = response.css('span.o-product__title-truncate.f-body--em::text').get()
        sub_title = response.css('span.o-product__title-truncate.f-body--em.s-multilines span')
        if title is not None:
            result = title
        if sub_title is not None:
            for sub in sub_title:
                result += sub.css('::text').get()
        return result

    def get_thumbnail_url(self, response):
        li = response[0]
        # print(li.get(), 888888888888888888)
        img_url = li.css('::attr(src)').get()
        # if img_url is None:
        #     return li.css('video').xpath('@src').get()
        return img_url

    def get_img_urls(self, urls):
        result = ''
        for url in urls:
            if self.main_url in url:
                result += url + ','
            else:
                result += self.main_url + url + ','

        return result

    def get_product_attributes(self, response):
        result = []
        size_link_list = response.css('ul.swatches.size>li')
        if len(size_link_list) > 0:
            size_attr = self.get_size_attribute(response)
            result.append(size_attr)

        color_list = response.css('ul#fixedColorList>li')
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
        lists = response.css('ul.swatches.size>li')

        result = []
        for item in lists:
            attribute_variable = VariableClass()
            variable_class_item_ioader = VariableClassItemLoader(item=attribute_variable, response=response)
            variable_class_item_ioader.add_value('DataCode', '')
            global_price = response.css(
                'span.price-sales::attr(content)').get()
            variable_class_item_ioader.add_value('NewPrice', global_price)
            variable_class_item_ioader.add_value('Name', item.css('a').get())

            variable_class_item_ioader.add_value('OldPrice', '')
            variable_class_item_ioader.add_value('ColorSquaresRgb', '')
            variable_class_item_ioader.add_value('DisplayColorSquaresRgb', False)
            variable_class_item_ioader.add_value('PriceAdjustment', 0)
            variable_class_item_ioader.add_value('PriceAdjustmentUsePercentage', False)

            variable_class_item_ioader.add_value('IsPreSelected', False)
            variable_class_item_ioader.add_value('DisplayOrder', False)
            variable_class_item_ioader.add_value('DisplayImageSquaresPicture', False)
            variable_class_item_ioader.add_value('PictureUrlInStorage', '')
            loadItem = variable_class_item_ioader.load_item()
            result.append(loadItem)
        return result

    def get_color_variables(self, response):
        list = response.css('ul#fixedColorList>li')
        result = []
        for item in list:
            attribute_variable = VariableClass()
            variable_class_item_loader = VariableClassItemLoader(item=attribute_variable, response=response)
            variable_class_item_loader.add_value('DataCode', '')
            global_price = response.css(
                'span.price-sales::attr(content)').get()
            variable_class_item_loader.add_value('NewPrice', global_price)
            variable_class_item_loader.add_value('OldPrice', '')

            variable_class_item_loader.add_value('Name', item.css('span>a::text').get())
            variable_class_item_loader.add_value('ColorSquaresRgb', item.css('a::attr(style)').get())
            variable_class_item_loader.add_value('DisplayColorSquaresRgb', False)
            variable_class_item_loader.add_value('PriceAdjustment', 0)
            variable_class_item_loader.add_value('PriceAdjustmentUsePercentage', False)

            variable_class_item_loader.add_value('IsPreSelected', item.css('::attr(class)').get() > 'selected')
            variable_class_item_loader.add_value('DisplayOrder', False)
            variable_class_item_loader.add_value('DisplayImageSquaresPicture', False)
            variable_class_item_loader.add_value('PictureUrlInStorage', '')
            loadItem = variable_class_item_loader.load_item()
            result.append(loadItem)
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
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) '
                          'Chrome/86.0.4240.75 Safari/537.36',
            'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,'
                      '*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
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
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) "
                          "Chrome/70.0.3538.102 Safari/537.36 Edge/18.19041",
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
