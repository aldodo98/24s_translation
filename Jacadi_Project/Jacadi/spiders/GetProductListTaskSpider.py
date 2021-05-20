import scrapy
# import datetime
import uuid
import random
import json
from scrapy.http.headers import Headers
from scrapy_redis.spiders import RedisSpider
from Jacadi.items import CategoryTree, ProductInfo, TreeLevel
from Jacadi.itemloader import CategoryTreeItemLoader, ProductInfoItemLoader
# from scrapy.http.headers import Headers
# from scrapy_redis.spiders import RedisSpider
from Jacadi.settings import BOT_NAME


class GetproductlisttaskspiderSpider(RedisSpider):
# class GetproductlisttaskspiderSpider(scrapy.Spider):
    name = 'GetProductListTaskSpider'
    allowed_domains = ['www.jacadi.fr']
    start_urls = ['http://www.jacadi.fr/']
    redis_key = BOT_NAME + ':GetTreeProductListTaskSpider'
    main_url = 'http://www.jacadi.fr'

    # __init__方法必须按规定写，使用时只需要修改super()里的类名参数即可
    def __init__(self, *args, **kwargs):
        # 修改这里的类名为当前类名
        super(GetproductlisttaskspiderSpider, self).__init__(*args, **kwargs)

    def make_request_from_data(self, data):
        receivedDictData = json.loads(str(data, encoding="utf-8"))
        # print(receivedDictData)
        # here you can use and FormRequest
        formRequest = scrapy.FormRequest(url=receivedDictData['Level_Url'], dont_filter=True,
                                         meta={'CategoryTreeId': receivedDictData['Id']})
        return formRequest

    def parse(self, response):
        try:
            success = response.status == 200
            if success:
                return self.getProductListByPage(response)
        except Exception as err:
            print(err)

        # 获取商品

    def getProductListByPage(self, response):
        if response.status != 200:
            yield None

        product_lis = response.css('ul.j-list-products>li')
        if len(product_lis) == 0:
            yield None

        for li in product_lis:
            yield self.generateProductItem(
                li.css('p.product-name::text').get(),
                li.css('span.j-price::text').get(),
                li.css('a::attr(href)').get(),
                response.meta['CategoryTreeId'],
                None
            )

        pagination = response.css('ul.j-list-pagination li.j-list-pagination-next')
        if len(pagination) > 0:
            yield scrapy.Request(url=self.url_join(pagination.css('a::attr(href)').get()), callback=self.parse,
                                 meta={
                                    'CategoryTreeId': response.meta['CategoryTreeId']
                                }, dont_filter=True)

    def getProducts(self, response):
        if response.status != 200:
            yield None
        product_lis = response.css('ul.j-list-products>li')
        for li in product_lis:
            yield self.generateProductItem(
                li.css('p.product-name::text').get(),
                li.css('span.j-price::text').get(),
                li.css('a::attr(href)').get(),
                response.meta['CategoryTreeId'],
                None
            )
        yield None

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

    def url_join(self, values):
        if values is None or values == '':
            return ''
        if self.main_url in values:
            return values
        else:
            return self.main_url + values

    
