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

    # def start_requests(self):
    #     urls = [
    #         # 'http://www.yoox.com/fr/femme/shoponline/lunettes_mc#/dept=bagsaccwomen&gender=D&attributes=%7b%27ctgr%27%3a%5b%27cchl%27%5d%7d&season=E',
    #         # "https://www.yoox.com/fr/femme/shoponline?dept=newarrivalswomen&attributes={'nwrrvls'%3a['nwtpbrnds']}",
    #         # "https://www.yoox.com/fr/femme/shoponline?dept=newarrivalswomen&attributes=#/dept=newarrivalswomen&gender=D&page=2&season=X",
    #         # 'https://www.yoox.com/fr/femme/shoponline/robes_mc#/dept=clothingwomen&gender=D&attributes=%7b%27ctgr%27%3a%5b%27vstt%27%5d%7d&season=E'
    #         # 'https://www.yoox.com/fr/homme',
    #         # 'https://www.yoox.com/fr/enfant',
    #         'https://www.yoox.com/nl/men/shoponline/adidas_md#/Md=1319&dept=men&gender=U',
    #         # 'https://www.yoox.com/nl/women/shoponline?dept=salewomen&attributes=%7b%27smrtfnd%27%3a%5b%27smbstndr%27%5d%7d'
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
        formRequest = scrapy.FormRequest(url=receivedDictData['Level_Url'],dont_filter=True,
                                         meta={'CategoryTreeId': receivedDictData['Id'], 'Url': receivedDictData['Level_Url']})
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
                return self.getProductListByPage(response)
        except Exception as err:
            print(err)

    # 获取商品
    def getProductListByPage(self, response):
        if response.status != 200:
            yield None

        total_page = response.css('div#navigation-bar-bottom .text-light a::attr(data-total-page)').get()
        url = response.css('div#navigation-bar-bottom .text-light a::attr(href)')

        if url[-1].get() is None or url[-1].get() == '':
            _url = response.css('div#navigation-bar-bottom .text-light a::attr(rel)')
            for page in range(1, int(total_page) + 1):
                suffix_url = _url[-1].get().replace('address:','')
                page_url = response.meta['Url'].split('#/')[0] + '#/' + suffix_url.replace('page=' + str(total_page),'page='+str(page))
                yield scrapy.Request(url=page_url, callback=self.getProducts, headers=random.choice(self.headers_list),meta={
                     'CategoryTreeId': response.meta['CategoryTreeId']
                 })

        else:
            if total_page and url:
                for page in range(1, int(total_page) + 1):
                    page_url = url[-1].get().replace('page=' + str(total_page), 'page=' + str(page)).replace(str(total_page) + '#', str(page) + '#')
                    yield scrapy.Request(url=page_url, callback=self.getProducts, headers=random.choice(self.headers_list), meta={
                        'CategoryTreeId': response.meta['CategoryTreeId']
                    })
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
