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

    # def start_requests(self):
    #     urls = [
    #         # 'https://fr.sandro-paris.com/fr/femme-collection-ete/',
    #         # 'https://fr.sandro-paris.com/fr/femme-offres-privees-la-maroquinerie/',
    #         # 'https://fr.sandro-paris.com/fr/femme-offres-privees-pantalons-jeans/',
    #         # 'https://fr.sandro-paris.com/fr/femme-offres-privees-50/'
    #         # 'https://fr.sandro-paris.com/fr/femme/pulls-et-cardigans/',
    #         # 'https://fr.sandro-paris.com/fr/femme/chaussures/toutes-les-chaussures/'
    #     ]
    #     for url in urls:
    #         print(url)
    #         yield scrapy.Request(url=url, callback=self.parse, headers=random.choice(self.headers_list), meta={
    #             'CategoryTreeId': '1',
    #             'Url': url
    #         }, dont_filter=True)

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
        }, headers=random.choice(self.headers_list), dont_filter=True)

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