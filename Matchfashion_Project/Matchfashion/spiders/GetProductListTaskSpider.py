from time import sleep

import scrapy
import datetime
import uuid
import random
from Matchfashion.items import CategoryTree, ProductInfo, TreeLevel
from Matchfashion.itemloader import CategoryTreeItemLoader, ProductInfoItemLoader
from scrapy.http.headers import Headers
from scrapy_redis.spiders import RedisSpider
from Matchfashion.settings import BOT_NAME

import json

class GetProductListTaskSpider(RedisSpider):
    name = "GetTreeProductListTaskSpider"
    redis_key = BOT_NAME+':GetTreeProductListTaskSpider'
    allowed_domains = ['www.matchesfashion.com']
    main_url = 'https://www.matchesfashion.com'

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
        # category_id = 'xxx'
        lists = response.css('.lister__wrapper li')
        for item in lists:
            product_info = ProductInfo()
            product_itemloader = ProductInfoItemLoader(item=product_info, response=response)
            product_itemloader.add_value('CategoryTreeId', category_id)
            product_itemloader.add_value('Id', str(uuid.uuid4()))
            product_itemloader.add_value('ProjectName', BOT_NAME)
            url = item.css('a::attr("href")').get()
            if url is not None and self.main_url not in url:
                product_itemloader.add_value('ProductUrl', self.main_url + url)
            elif url is None:
                continue
            else:
                product_itemloader.add_value('ProductUrl', url)
            product_itemloader.add_value('ProductName', item.css('.lister__item__title::text').get())
            product_itemloader.add_value('Price', item.css('.lister__item__price-full::text').get())

            yield product_itemloader.load_item()
        if len(response.css('.redefine__right__pager .next')) > 0:
            nextUrl = response.css('.redefine__right__pager .next a::attr("href")').get()
            if nextUrl is not None and self.main_url not in nextUrl:
                nextUrl = self.main_url + nextUrl
            sleep(2)
            print(nextUrl)
            yield scrapy.Request(url=nextUrl, callback=self.getProducts, meta={'RootId': category_id})
        else:
            return

