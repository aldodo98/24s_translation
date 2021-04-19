import scrapy
import datetime
import uuid
import random
import json
from Yoox.items import CategoryTree, ProductInfo
from Yoox.itemloader import CategoryTreeItemLoader, ProductInfoItemLoader
from Yoox.settings import BOT_NAME
from scrapy_redis.spiders import RedisSpider
from scrapy.http.headers import Headers
from scrapy_redis.spiders import RedisSpider


# class RoottaskspiderSpider(scrapy.Spider):
class RoottaskspiderSpider(RedisSpider):
    name = 'RootTaskSpider'
    allowed_domains = ['www.yoox.com']
    redis_key = BOT_NAME+':RootTaskSpider'
    main_url = 'https://www.yoox.com'
    # def start_requests(self):
    #     urls = [
    #         "https://www.yoox.com/fr",
    #         # 'https://www.yoox.com/fr/femme/shoponline/lunettes_mc#/dept=bagsaccwomen&gender=D&attributes=%7b%27ctgr%27%3a%5b%27cchl%27%5d%7d&season=E'
    #
    #     ]
    #     for url in urls:
    #         yield scrapy.Request(url=url, callback=self.parse, headers=random.choice(self.headers_list), meta={
    #             'RootId': '1'
    #         })
    #         # yield scrapy.Request(url=url, callback=self.getProducts, headers=random.choice(self.headers_list), meta={
    #         #     'CategoryId': '1'
    #         # })

    # __init__方法必须按规定写，使用时只需要修改super()里的类名参数即可
    def __init__(self, *args, **kwargs):
        # 修改这里的类名为当前类名
        super(RoottaskspiderSpider, self).__init__(*args, **kwargs)

    def make_request_from_data(self, data):
        receivedDictData = json.loads(str(data, encoding="utf-8"))
        # print(receivedDictData)
        # here you can use and FormRequest
        formRequest = scrapy.FormRequest(url="https://www.yoox.com/fr/designerindex/women", dont_filter=True,
                                         meta={'RootId': receivedDictData['Id']})
        formRequest.headers = Headers(random.choice(self.headers_list))
        return formRequest

    def schedule_next_requests(self):
        for request in self.next_requests():
            request.headers = Headers(random.choice(self.headers_list))
            self.crawler.engine.crawl(request, spider=self)

    def parse(self, response):
        try:
            return self.getCategory(response=response)
        except Exception as err:
            print(err)

    # 获取目录
    def getCategory(self, response):
        success = response.status == 200
        if success:
            cate_list_1 = response.css('li[class^="letter-block-spacer"]')  # 一级目录元素列表
            for ele in cate_list_1:
                cate_1 = ele.css('h3[class^="big-letter"]::text').get()  # 一级目录  # 一级目录商品url
                cate_2_urls = ele.xpath('div/ul/li/a/@href').extract()
                cate_2_names = ele.xpath('div/ul/li/a/text()').extract()
                for cate_2_ele in zip(cate_2_names, cate_2_urls):
                    cate_2 = cate_2_ele[0]
                    cate_2_url = self.main_url + cate_2_ele[1]
                    item = self.getCategoryItem(
                        cate_1,
                        cate_2,
                        None,
                        cate_2_url,
                        response.meta['RootId']
                    )
                    yield item
                    #yield scrapy.Request(url=item['Level_Url'], callback=self.parse_level, headers=random.choice(self.headers_list), meta={
                    #    'RootId': response.meta['RootId'],
                    #    'Cate_1': cate_1
                    #})

    def parse_level(self, response):
        success = response.status == 200
        if success:
            lis = response.css('ul#sections-menu>li')
            cate_3_modals = response.css('div#layer-sections>div')
            for index, li in enumerate(lis):
                cate_2 = li.css('span::text').get()
                divs = cate_3_modals[index].css('div.menu-section-item')
                for div in divs:
                    cate_3 = div.css('a::text').get()
                    url = div.css('a::attr(href)').get()
                    yield self.getCategoryItem(
                        response.meta['Cate_1'],
                        cate_2,
                        cate_3,
                        url,
                        response.meta['RootId']
                    )

    def getCategoryItem(self, cate_1, cate_2, cate_3, url, c_rootId=''):
        category_tree = CategoryTree()
        category_itemloader = CategoryTreeItemLoader(item=category_tree)
        category_itemloader.add_value('Id', str(uuid.uuid4()))

        category_itemloader.add_value('ProjectName', BOT_NAME)
        category_itemloader.add_value('Level_Url', url)
        category_itemloader.add_value('CategoryLevel1', cate_1)
        category_itemloader.add_value('CategoryLevel2', cate_2)
        category_itemloader.add_value('CategoryLevel3', cate_3)

        # time = datetime.datetime.now().isoformat()
        # category_itemloader.add_value('CreateDateTime', time)
        # category_itemloader.add_value('UpdateDateTime', time)

        category_itemloader.add_value('RootId', c_rootId)

        # category_itemloader.add_value('ManufacturerId', 12)
        # category_itemloader.add_value('CategoryId', 20)

        item_load = category_itemloader.load_item()

        return item_load

    # 获取商品
    def getProducts(self, response):
        if response.status != 200:
            return
        category_id = response.meta['CategoryId']
        lists = response.css('ul#instant-search-results-container>li')
        print(len(lists))
        for item in lists:
            product_info = ProductInfo()
            # 无折扣
            regular_big_price = item.css('.price-box>.regular-price>span::text').get()
            regular_small_price = item.css('.price-box>.regular-price>span>small::text').get()
            if regular_small_price is not None:
                regular_small_price = regular_small_price.replace(' ', '')
            regular_price = (regular_big_price or '') + (regular_small_price or '')

            # 有折扣
            special_big_price = item.css('.price-box>.special-price>span>span::text').get()
            special_small_price = item.css('.price-box>.special-price>span>span>small::text').get()
            if special_small_price is not None:
                special_small_price = special_small_price.replace(' ', '')
            special_price = (special_big_price or '') + (special_small_price or '')

            # 商品名称
            product_name = item.css('h2.product-info>a>strong::text').get()
            if product_name is not None:
                product_name = product_name.upper()
            else:
                continue  # 商品缺货,无商品url，不推入数据库

            product_itemloader = ProductInfoItemLoader(item=product_info, response=response)
            product_itemloader.add_value('CategoryTreeId', category_id)
            product_itemloader.add_value('Id', str(uuid.uuid4()))
            product_itemloader.add_value('ProductId', item.css('::attr(data-id)').get())
            product_itemloader.add_value('ProductUrl', item.css('h2.product-info>a::attr(href)').get())
            product_itemloader.add_value('ProductName', product_name)
            product_itemloader.add_value('ProjectName', BOT_NAME)
            product_itemloader.add_value('Price', regular_price or special_price)

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

