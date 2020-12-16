import scrapy
import datetime
import uuid
import random
from Dior.items import CategoryTree, ProductInfo, TreeLevel
from Dior.itemloader import CategoryTreeItemLoader, ProductInfoItemLoader
from scrapy.http.headers import Headers
from Dior.settings import BOT_NAME
from scrapy_redis.spiders import RedisSpider

import json


# class GetProductListTaskSpider(RedisSpider):
#     name = "GetTreeProductListTaskSpider"
#     redis_key = BOT_NAME+':GetTreeProductListTaskSpider'
#     allowed_domains = ['www.celine.com']
#     main_url = "https://www.celine.com"
#
#     # __init__方法必须按规定写，使用时只需要修改super()里的类名参数即可
#     def __init__(self, *args, **kwargs):
#         # 修改这里的类名为当前类名
#         super(GetProductListTaskSpider, self).__init__(*args, **kwargs)
#
#     def make_request_from_data(self, data):
#         receivedDictData = json.loads(str(data, encoding="utf-8"))
#         # print(receivedDictData)
#         # here you can use and FormRequest
#         formRequest = scrapy.FormRequest(url=receivedDictData['Level_Url'],dont_filter=True,
#                                          meta={'CategoryTreeId': receivedDictData['Id']})
#         formRequest.headers = Headers(random.choice(self.headers_list))
#         return formRequest
#
#     def schedule_next_requests(self):
#         for request in self.next_requests():
#             request.headers = Headers(random.choice(self.headers_list))
#             self.crawler.engine.crawl(request, spider=self)
#
#     def parse(self, response):
#         try:
#             success = response.status == 200
#             if success:
#                 return self.getProducts(response)
#         except Exception as err:
#             print(err)
#
#     def getProducts(self, response):
#         category_id = response.meta['CategoryTreeId']
#         # lists = response.css('ul.o-listing-grid li a')
#         lists = list()
#         products_in_list = response.css('ul.o-listing-grid li a')
#         products_in_row = response.css('ul.o-listing-row li a')
#
#         if len(products_in_list) > 0:
#             lists.extend(products_in_list)
#
#         if len(products_in_row) > 0:
#             lists.extend(products_in_row)
#
#         for item in lists:
#             product_info = ProductInfo()
#             product_itemloader = ProductInfoItemLoader(item=product_info, response=response)
#             product_itemloader.add_value('CategoryTreeId', category_id)
#             product_itemloader.add_value('Id', str(uuid.uuid4()))
#             product_itemloader.add_value('ProjectName', BOT_NAME)
#
#             product_itemloader.add_value('ProductUrl', self.main_url + item.css('::attr(href)').get())
#             product_itemloader.add_value('ProductName',
#                                          item.css('.m-product-listing__meta-title.f-body::text').get() +
#                                          ''.join(item.css('.m-product-listing__meta-title.f-body span::text').getall())
#                                          )
#             product_itemloader.add_value('Price', item.css('strong.f-body--em::text').get())
#             yield product_itemloader.load_item()
#         yield None
#
#     headers_list = [
#         # Chrome
#         {
#             'authority': 'www.marionnaud.fr',
#             'cache-control': 'max-age=0',
#             'sec-ch-ua': '"Chromium";v="86", "\\"Not\\\\A;Brand";v="99", "Google Chrome";v="86"',
#             'sec-ch-ua-mobile': '?0',
#             'dnt': '1',
#             'upgrade-insecure-requests': '1',
#             'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) '
#                           'Chrome/86.0.4240.75 Safari/537.36',
#             'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,'
#                       '*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
#             'sec-fetch-site': 'none',
#             'sec-fetch-mode': 'navigate',
#             'sec-fetch-user': '?1',
#             'sec-fetch-dest': 'document',
#             'accept-language': 'en,fr;q=0.9,en-US;q=0.8,zh-CN;q=0.7,zh;q=0.6',
#         },
#         # IE
#         {
#             "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
#             "Accept-Encoding": "gzip, deflate, br",
#             "Accept-Language": "fr-FR,fr;q=0.8,en-US;q=0.7,en;q=0.5,zh-Hans-CN;q=0.3,zh-Hans;q=0.2",
#             "Upgrade-Insecure-Requests": "1",
#             "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) "
#                           "Chrome/70.0.3538.102 Safari/537.36 Edge/18.19041",
#         },
#         # Firefox
#         {
#             'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:82.0) Gecko/20100101 Firefox/82.0',
#             'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
#             'Accept-Language': 'en-US,en;q=0.5',
#             'Connection': 'keep-alive',
#             'Upgrade-Insecure-Requests': '1',
#             'Cache-Control': 'max-age=0',
#             'TE': 'Trailers',
#         }
#     ]

class GetProductListTaskSpider(RedisSpider):
    name = "GetTreeProductListTaskSpider"
    redis_key = BOT_NAME+':GetTreeProductListTaskSpider'
    main_url = "https://www.dior.com/fr_fr"
    allowed_domains = ['www.dior.com']

    # def start_requests(self):
    #     urls = [
    #         "https://www.dior.cn/zh_cn/gifts/women%E2%80%99s-fashion-and-accessories-gifts"
    #     ]
    #     for url in urls:
    #         yield scrapy.Request(url=url, callback=self.parse, headers=random.choice(self.headers_list))
    # __init__方法必须按规定写，使用时只需要修改super()里的类名参数即可
    def __init__(self, *args, **kwargs):
        # 修改这里的类名为当前类名
        super(GetProductListTaskSpider, self).__init__(*args, **kwargs)

    def make_request_from_data(self, data):
        receivedDictData = json.loads(str(data, encoding="utf-8"))
        # print(receivedDictData)
        # here you can use and FormRequest
        formRequest = scrapy.FormRequest(url=receivedDictData['Level_Url'],dont_filter=True,
                                         meta={'CategoryTreeId': receivedDictData['Id']})
        formRequest.headers = Headers(random.choice(self.headers_list))
        return formRequest

    def schedule_next_requests(self):
        for request in self.next_requests():
            request.headers = Headers(random.choice(self.headers_list))
            self.crawler.engine.crawl(request, spider=self)

    def parse(self, response):
        try:
            success = response.status == 200
            if success:
                return self.getProducts(response)
        except Exception as err:
            print(err)

    def getProducts(self, response):
        category_id = response.meta['CategoryTreeId']
        mutiple_lists = response.css('ul.grid-view-content')
        for lists in mutiple_lists:
            items = lists.css('li.grid-view-element')
            for item in items:
                product_info = ProductInfo()
                product_itemloader = ProductInfoItemLoader(item=product_info, response=response)
                product_itemloader.add_value('CategoryTreeId', category_id)
                product_itemloader.add_value('Id', str(uuid.uuid4()))
                product_itemloader.add_value('ProjectName', BOT_NAME)
                url = item.css('a.product-link::attr(href)').get()
                if url is not None and self.main_url not in url:
                    product_itemloader.add_value('ProductUrl', self.main_url + url)
                else:
                    product_itemloader.add_value('ProductUrl', url)
                product_itemloader.add_value('ProductName',
                                             (item.css('.product-title>span::text').get() or '') +
                                             ''.join((item.css('.product-subtitle::text').get() or ''))
                                             )
                product_itemloader.add_value('Price', item.css('.price-line::text').get())
                yield product_itemloader.load_item()
            yield None

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