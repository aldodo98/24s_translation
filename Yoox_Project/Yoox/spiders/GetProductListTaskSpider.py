import scrapy
# import datetime
import uuid
import random
import json
from scrapy.http.headers import Headers
# from scrapy_redis.spiders import RedisSpider
from Yoox.items import CategoryTree, ProductInfo, TreeLevel
from Yoox.itemloader import CategoryTreeItemLoader, ProductInfoItemLoader
# from scrapy.http.headers import Headers
from scrapy_redis.spiders import RedisSpider
from Yoox.settings import BOT_NAME


class GetproductlisttaskspiderSpider(RedisSpider):
# class GetproductlisttaskspiderSpider(scrapy.Spider):
    name = 'GetProductListTaskSpider'
    allowed_domains = ['www.yoox.com']
    redis_key = BOT_NAME + ':GetTreeProductListTaskSpider'

    # __init__方法必须按规定写，使用时只需要修改super()里的类名参数即可
    def __init__(self, *args, **kwargs):
        # 修改这里的类名为当前类名
        super(GetproductlisttaskspiderSpider, self).__init__(*args, **kwargs)

    def make_request_from_data(self, data):
        receivedDictData = json.loads(str(data, encoding="utf-8"))
        # print(receivedDictData)
        # here you can use and FormRequest
        formRequest = scrapy.FormRequest(url=receivedDictData['Level_Url'],dont_filter=True,
                                         meta={'CategoryTreeId': receivedDictData['Id'], 'Url': receivedDictData['Level_Url']})
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

        total_page = response.css('div#navigation-bar-bottom div ul li.text-light a::attr(data-total-page)').get()
        if total_page is None:
            yield scrapy.Request(url=response.url, callback=self.getProducts, headers=random.choice(self.headers_list),
                                 meta={
                                     'CategoryTreeId': response.meta['CategoryTreeId']
                                 }, dont_filter=True)
        else:
            url = response.css('div#navigation-bar-bottom div ul li.text-light a::attr(href)')
            # print(total_page, url[-1].get(), 9090909099090909090)
            if url[-1].get() is None or url[-1].get() == '':
                _url = response.css('div#navigation-bar-bottom div ul li.text-light a::attr(rel)')
                for page in range(1, int(total_page) + 1):
                    suffix_url = _url[-1].get().replace('address:','')
                    page_url = response.meta['Url'].split('#/')[0] + '#/' + suffix_url.replace('page=' + str(total_page),'page='+str(page))
                    yield scrapy.Request(url=page_url, callback=self.getProducts, headers=random.choice(self.headers_list),meta={
                        'CategoryTreeId': response.meta['CategoryTreeId']
                    }, dont_filter=True)

            else:
                if total_page and url:
                    for page in range(1, int(total_page) + 1):
                        page_url = url[-1].get().replace('page=' + str(total_page), 'page=' + str(page)).replace(str(total_page) + '#', str(page) + '#')
                        yield scrapy.Request(url=page_url, callback=self.getProducts, headers=random.choice(self.headers_list), meta={
                            'CategoryTreeId': response.meta['CategoryTreeId']
                        }, dont_filter=True)
                else:
                    lis = response.css('li.slide__2s7ZY')
                    for li in lis:
                        yield self.generateProductItem(
                            li.css('div.title__1-Nny span::text').get(),
                            li.css('div.current__2yHPu::text').get(),
                            li.css('a::attr(href)').get(),
                            response.meta['CategoryTreeId'],
                            None
                        )


    def getProducts(self, response):
        if response.status != 200:
            yield None
        category_id = response.meta['CategoryTreeId']
        lists = response.css('div#itemsGrid .col-8-24')
        # print(len(lists),'000000000000000000000000000')
        for item in lists:
            product_price = item.css('div::attr(data-discountprice_eur)').get()
            # 商品名称
            product_name = item.css('div::attr(data-brand)').get()

            yield self.generateProductItem(
                product_name,
                product_price,
                item.css('a.itemlink::attr(href)').get(),
                category_id,
                item.css('div::attr(data-brand-id)').get()
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


