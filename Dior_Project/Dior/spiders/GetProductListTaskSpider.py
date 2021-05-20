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

class GetProductListTaskSpider(RedisSpider):
    name = "GetTreeProductListTaskSpider"
    redis_key = BOT_NAME+':GetTreeProductListTaskSpider'
    main_url = "https://www.dior.com"
    allowed_domains = ['www.dior.com']

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
        mutiple_lists = response.css('ul.grid-view-content')
        count = 0
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
                elif url is None:
                    continue
                else:
                    product_itemloader.add_value('ProductUrl', url)
                product_itemloader.add_value('ProductName',
                                             (item.css('.product-title>span::text').get() or '') +
                                             ''.join((item.css('.product-subtitle::text').get() or ''))
                                             )
                product_itemloader.add_value('Price', item.css('.price-line::text').get())
                yield product_itemloader.load_item()
