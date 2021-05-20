import scrapy
import datetime
import uuid
import random
from Celine.items import CategoryTree, ProductInfo, TreeLevel
from Celine.itemloader import CategoryTreeItemLoader, ProductInfoItemLoader
from scrapy.http.headers import Headers
from scrapy_redis.spiders import RedisSpider
from Celine.settings import BOT_NAME

import json


class GetProductListTaskSpider(RedisSpider):
    name = "GetTreeProductListTaskSpider"
    redis_key = BOT_NAME+':GetTreeProductListTaskSpider'
    allowed_domains = ['www.celine.com']
    main_url = "https://www.celine.com"

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
        return formRequest

    def parse(self, response):
        try:
            success = response.status == 200
            if success:
                return self.getProducts(response)
        except Exception as err:
            print(err)

    def getProducts(self, response):
        category_id = response.meta['CategoryTreeId']
        # lists = response.css('ul.o-listing-grid li a')
        lists = list()
        products_in_list = response.css('ul.o-listing-grid li a')
        products_in_row = response.css('ul.o-listing-row li a')

        if len(products_in_list) > 0:
            lists.extend(products_in_list)

        if len(products_in_row) > 0:
            lists.extend(products_in_row)

        for item in lists:
            product_info = ProductInfo()
            product_itemloader = ProductInfoItemLoader(item=product_info, response=response)
            product_itemloader.add_value('CategoryTreeId', category_id)
            product_itemloader.add_value('Id', str(uuid.uuid4()))
            product_itemloader.add_value('ProjectName', BOT_NAME)

            product_itemloader.add_value('ProductUrl', self.main_url + item.css('::attr(href)').get())
            product_itemloader.add_value('ProductName',
                                         item.css('.m-product-listing__meta-title.f-body::text').get() +
                                         ''.join(item.css('.m-product-listing__meta-title.f-body span::text').getall())
                                         )
            product_itemloader.add_value('Price', item.css('strong.f-body--em::text').get())
            yield product_itemloader.load_item()
        yield None