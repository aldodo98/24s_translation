import scrapy
import datetime
import uuid
import random
import json
from Sandro.items import CategoryTree, ProductInfo
from Sandro.itemloader import CategoryTreeItemLoader, ProductInfoItemLoader
from Sandro.settings import BOT_NAME
from scrapy_redis.spiders import RedisSpider
from scrapy.http.headers import Headers
from scrapy_redis.spiders import RedisSpider


class RoottaskspiderSpider(RedisSpider):
# class RoottaskspiderSpider(scrapy.Spider):
    name = 'RootTaskSpider'
    allowed_domains = ['fr.sandro-paris.com']
    redis_key = BOT_NAME + ':RootTaskSpider'

    # def start_requests(self):
    #     urls = [
    #         "https://fr.sandro-paris.com/",
    #     ]
    #     for url in urls:
    #         yield scrapy.Request(url=url, callback=self.parse, headers=random.choice(self.headers_list), meta={
    #             'RootId': '1'
    #         }, dont_filter=True)

    # __init__方法必须按规定写，使用时只需要修改super()里的类名参数即可
    def __init__(self, *args, **kwargs):
        # 修改这里的类名为当前类名
        super(RoottaskspiderSpider, self).__init__(*args, **kwargs)

    def make_request_from_data(self, data):
        receivedDictData = json.loads(str(data, encoding="utf-8"))
        # print(receivedDictData)
        # here you can use and FormRequest
        formRequest = scrapy.FormRequest(url="https://fr.sandro-paris.com", dont_filter=True,
                                         meta={'RootId': receivedDictData['Id']})
        formRequest.headers = Headers(random.choice(self.headers_list))
        return formRequest

    def schedule_next_requests(self):
        for request in self.next_requests():
            request.headers = Headers(random.choice(self.headers_list))
            self.crawler.engine.crawl(request, spider=self)

    def parse(self, response):
        success = response.status == 200
        if success:
            main_menus = response.css('div.col>div.title')

            for menu in main_menus:
                yield scrapy.Request(url=menu.xpath('./a/@href').get(), callback=self.parse_res,
                                     headers=random.choice(self.headers_list), meta={
                        'RootId': response.meta['RootId'],
                        'Cate_1': menu.xpath('./a/text()').get(),
                        'NeedWebDriver': True
                    }, dont_filter=True)

    def parse_res(self, response):

        success = response.status == 200
        if success:
            levels = self.generate_levels(response)
            for node in levels:
                if node is None:
                    continue
                yield node

    def generate_levels(self, response):
        results = list()
        lis = response.css('ul.level-1>li')
        for li in lis:
            results.append(
                self.getCategoryItem(
                    li.xpath('./a/@href').get(),
                    response.meta['RootId'],
                    response.meta['Cate_1'],
                    li.css('span::text').get()
                )
            )

            for item in li.css('ul.level-2'):
                for level in item.xpath('./li/a'):
                    if item.xpath('./p/text()').get() is None or item.xpath('./p/text()').get() == '':
                        results.append(
                            self.getCategoryItem(
                                level.css('::attr(href)').get(),
                                response.meta['RootId'],
                                response.meta['Cate_1'],
                                li.css('span::text').get(),
                                level.css('::text').get()
                            )
                        )
                    else:
                        results.append(
                            self.getCategoryItem(
                                level.css('::attr(href)').get(),
                                response.meta['RootId'],
                                response.meta['Cate_1'],
                                li.css('span::text').get(),
                                item.xpath('./p/text()').get(),
                                level.css('::text').get()
                            )
                        )

        return results

    def getCategoryItem(self, url, c_rootId, cate_1, cate_2, cate_3='', cate_4=''):
        category_tree = CategoryTree()
        category_itemloader = CategoryTreeItemLoader(item=category_tree)
        category_itemloader.add_value('Id', str(uuid.uuid4()))

        category_itemloader.add_value('ProjectName', BOT_NAME)
        category_itemloader.add_value('Level_Url', url)
        category_itemloader.add_value('CategoryLevel1', cate_1)
        category_itemloader.add_value('CategoryLevel2', cate_2)
        category_itemloader.add_value('CategoryLevel3', cate_3)
        category_itemloader.add_value('CategoryLevel4', cate_4)
        category_itemloader.add_value('CategoryLevel5', '')

        category_itemloader.add_value('RootId', c_rootId)

        item_load = category_itemloader.load_item()

        return item_load

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
