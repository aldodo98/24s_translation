import scrapy
# import datetime
import uuid
import random
import json
from scrapy.http.headers import Headers
from scrapy_redis.spiders import RedisSpider
from Marionnaud.items import CategoryTree, ProductInfo, TreeLevel
from Marionnaud.itemloader import CategoryTreeItemLoader, ProductInfoItemLoader
# from scrapy.http.headers import Headers
# from scrapy_redis.spiders import RedisSpider
from Marionnaud.settings import BOT_NAME


# class GetproductlisttaskspiderSpider(scrapy.Spider):
class GetproductlisttaskspiderSpider(RedisSpider):
    name = 'GetProductListTaskSpider'
    allowed_domains = ['www.marionnaud.fr']
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
                                         meta={
                                             'CategoryTreeId': receivedDictData['Id'],
                                             'Url': receivedDictData['Level_Url']
                                         })
        return formRequest

    def parse(self, response):
        try:
            success = response.status == 200
            if success:
                return self.parse_res(response)
        except Exception as err:
            print(err)

    def parse_res(self, response):
        total_inhtml = response.css('.paginationBar label.totalResults::text').get()
        if total_inhtml is not None:
            total = int(total_inhtml.replace('articles', '').strip())
            if total % 100 == 0:
                pageno = total // 100
            else:
                pageno = total // 100 + 1

            for num in range(0, pageno):
                yield scrapy.Request(url=response.meta['Url'] + '?q=%3Arank-desc&page=' + str(num) + '&pageSize=100',
                                     callback=self.getProductsByList,
                                     meta={
                                        'CategoryTreeId': response.meta['CategoryTreeId']
                                    })
        product_lists = response.css('.slideshowHP div>a.productMainLink')
        if len(product_lists) > 0:
            for product in product_lists:
                product_info = ProductInfo()
                product_itemloader = ProductInfoItemLoader(item=product_info, response=response)
                product_itemloader.add_value('CategoryTreeId', response.meta['CategoryTreeId'])
                product_itemloader.add_value('Id', str(uuid.uuid4()))
                product_itemloader.add_value('ProductId', None)
                product_itemloader.add_value('ProductUrl', product.css('::attr(href)').get())
                product_itemloader.add_value('ProductName', product.css('div.product_name::text').get())
                product_itemloader.add_value('ProjectName', BOT_NAME)
                product_itemloader.add_value('Price', product.css('div.product_price span.lineinner').get())
                yield product_itemloader.load_item()

    # 获取分页商品信息
    def getProductsByList(self, response):
        category_id = response.meta['CategoryTreeId']
        product_list = response.css('ul.product-listing>li')
        for _ele in product_list:
            product_name = _ele.css('.infoTextCarousel>a>.product_name::text').get()
            if product_name is None or product_name == '':
                continue
            product_url = _ele.css('.infoTextCarousel>a.ProductInfoAnchor::attr(href)').get()
            product_id = _ele.css('.infoTextCarousel>.daily-offer-block::attr(data-product-id)').get()
            product_price = _ele.css('.infoTextCarousel span.lineinner').get()

            product_info = ProductInfo()
            product_itemloader = ProductInfoItemLoader(item=product_info, response=response)
            product_itemloader.add_value('CategoryTreeId', category_id)
            product_itemloader.add_value('Id', str(uuid.uuid4()))
            product_itemloader.add_value('ProductId', product_id)
            product_itemloader.add_value('ProductUrl', product_url)
            product_itemloader.add_value('ProductName', product_name)
            product_itemloader.add_value('ProjectName', BOT_NAME)
            product_itemloader.add_value('Price', product_price)

            yield product_itemloader.load_item()

