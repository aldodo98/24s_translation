from time import sleep

import scrapy
import datetime
import uuid
import random
from ClaudiePierlot.items import CategoryTree, ProductInfo, TreeLevel
from ClaudiePierlot.itemloader import CategoryTreeItemLoader, ProductInfoItemLoader
from scrapy.http.headers import Headers
from scrapy_redis.spiders import RedisSpider
from ClaudiePierlot.settings import BOT_NAME

import json

class GetProductListTaskSpider(RedisSpider):
    name = "GetTreeProductListTaskSpider"
    redis_key = BOT_NAME+':GetTreeProductListTaskSpider'
    allowed_domains = ['fr.claudiepierlot.com']
    main_url = "https://fr.claudiepierlot.com"

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
        lists = response.css('#search-result-items li div.product-tile')
        for item in lists:
            product_info = ProductInfo()
            product_itemloader = ProductInfoItemLoader(item=product_info, response=response)
            product_itemloader.add_value('CategoryTreeId', category_id)
            product_itemloader.add_value('Id', str(uuid.uuid4()))
            product_itemloader.add_value('ProjectName', BOT_NAME)
            product_itemloader.add_value('ProductName', item.css('.titleProduct a.name-link::text').get())
            product_itemloader.add_value('Price', item.css('.product-pricing .product-sales-price::text').get())
            url = item.css('a.thumb-link::attr("href")').get()
            if url is None:
                continue
            else:
                if self.main_url not in url:
                    product_itemloader.add_value('ProductUrl', self.main_url + url)
                else:
                    product_itemloader.add_value('ProductUrl', url)
                yield product_itemloader.load_item()
        if len(response.css('.c-pagination__more')) > 0:
            nextUrl = response.css('.c-pagination__more::attr("href")').get()
            yield scrapy.Request(url=nextUrl, callback=self.getProducts, meta={'CategoryTreeId': category_id}, dont_filter=True)
        else:
            return