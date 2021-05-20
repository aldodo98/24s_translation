import scrapy
# import datetime
import uuid
import random
import json
from scrapy.http.headers import Headers
from scrapy_redis.spiders import RedisSpider
from Sandro.items import CategoryTree, ProductInfo, TreeLevel
from Sandro.itemloader import CategoryTreeItemLoader, ProductInfoItemLoader
from Sandro.settings import BOT_NAME


# class GetproductlisttaskspiderSpider(scrapy.Spider):
class GetproductlisttaskspiderSpider(RedisSpider):
    name = 'GetProductListTaskSpider'
    allowed_domains = ['fr.sandro-paris.com/']
    redis_key = BOT_NAME + ':GetTreeProductListTaskSpider'

    # __init__方法必须按规定写，使用时只需要修改super()里的类名参数即可
    def __init__(self, *args, **kwargs):
        # 修改这里的类名为当前类名
        super(GetproductlisttaskspiderSpider, self).__init__(*args, **kwargs)

    def make_request_from_data(self, data):
        receivedDictData = json.loads(str(data, encoding="utf-8"))
        # print(receivedDictData)
        # here you can use and FormRequest
        formRequest = scrapy.FormRequest(url=receivedDictData['Level_Url'], dont_filter=True,
                                         meta={'CategoryTreeId': receivedDictData['Id'],
                                               'Url': receivedDictData['Level_Url']})
        return formRequest

    def parse(self, response):
        try:
            success = response.status == 200
            if success:
                return self.getMoreParams(response)
        except Exception as err:
            print(err)

    # 动态加载更多
    def getMoreParams(self, response):
        pagination = response.css('.pagination li a.viewAll::attr(href)').get()

        if pagination:
            total = pagination.split('?')[1].split('=')[1]
        else:
            total = ""

        url = response.meta['Url'] + '?sz=' + total

        yield scrapy.Request(url=url, callback=self.getProducts, meta={
            'CategoryTreeId': response.meta['CategoryTreeId']
        }, dont_filter=True)

    def getProducts(self, response):
        category_id = response.meta['CategoryTreeId']
        lists = response.css('ul#search-result-items li.grid-tile')

        for item in lists:
            yield self.generateProductItem(
                item.css('.product-name div a::text').get(),
                item.css('.product-pricing span.product-sales-price::text').get(),
                item.css('a.thumb-link::attr(href)').get(),
                response.meta['CategoryTreeId'],
                None
            )

    def generateProductItem(self, name, price, url, tree_id, product_id):
        if url is None or url == '':
            return None
        product_info = ProductInfo()
        product_itemloader = ProductInfoItemLoader(item=product_info)
        product_itemloader.add_value('CategoryTreeId', tree_id)
        product_itemloader.add_value('Id', str(uuid.uuid4()))
        product_itemloader.add_value('ProductId', product_id)
        product_itemloader.add_value('ProductUrl', url)
        product_itemloader.add_value('ProductName', name)
        product_itemloader.add_value('ProjectName', BOT_NAME)
        product_itemloader.add_value('Price', price)
        return product_itemloader.load_item()

