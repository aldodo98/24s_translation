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

    # def start_requests(self):
    #     urls = [
    #         # "https://www.marionnaud.fr/parfum/parfum-femme/eau-de-parfum/c/P0101", # 446
    #         "https://www.marionnaud.fr/parfum/parfum-homme/eau-de-toilette/c/P0202"  # 247
    #         # 'https://www.marionnaud.fr/marques/b/melvita/100923'
    #         # 'https://www.marionnaud.fr/marques/b/darphin/100962'
    #         # 'https://www.marionnaud.fr/marques/b/ioma/100716'
    #         # 'https://www.marionnaud.fr/marques/b/elenature/100976'
    #     ]
    #     for url in urls:
    #         print(url)
    #         yield scrapy.Request(url=url, callback=self.parse, headers=random.choice(self.headers_list), meta={
    #             'CategoryTreeId': '1',
    #             'Url': url
    #         })

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
                                     headers=random.choice(self.headers_list),
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