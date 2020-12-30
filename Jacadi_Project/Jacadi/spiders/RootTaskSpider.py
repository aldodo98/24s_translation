import scrapy
import datetime
import uuid
import random
from Jacadi.items import CategoryTree, ProductInfo, TreeLevel
from Jacadi.itemloader import CategoryTreeItemLoader, ProductInfoItemLoader
from scrapy.http.headers import Headers
from scrapy_redis.spiders import RedisSpider
from Jacadi.settings import BOT_NAME
import json


class RoottaskspiderSpider(RedisSpider):
# class RoottaskspiderSpider(scrapy.Spider):
    name = 'RootTaskSpider'
    allowed_domains = ['www.jacadi.fr']
    redis_key = BOT_NAME+':RootTaskSpider'

    # __init__方法必须按规定写，使用时只需要修改super()里的类名参数即可
    def __init__(self, *args, **kwargs):
        # 修改这里的类名为当前类名
        super(RoottaskspiderSpider, self).__init__(*args, **kwargs)

    def make_request_from_data(self, data):
        receivedDictData = json.loads(str(data, encoding="utf-8"))
        # print(receivedDictData)
        # here you can use and FormRequest
        formRequest = scrapy.FormRequest(url="https://www.jacadi.fr", dont_filter=True,
                                         meta={'RootId': receivedDictData['Id']})
        formRequest.headers = Headers(random.choice(self.headers_list))
        return formRequest

    def schedule_next_requests(self):
        for request in self.next_requests():
            request.headers = Headers(random.choice(self.headers_list))
            self.crawler.engine.crawl(request, spider=self)

    # def start_requests(self):
    #     urls = [
    #         'http://www.jacadi.fr/'
    #     ]
    #
    #     for url in urls:
    #         yield scrapy.Request(url=url, callback=self.parse, headers=random.choice(self.headers_list), meta={
    #             'RootId': '1'
    #         })


    def parse(self, response):
        success = response.status == 200
        if success:
            levels = self.generate_levels(response)
            for node in levels:
                if node is None:
                    continue
                yield node

            # eaux = response.css('')

    def generate_levels(self, response):
        results = list()
        # 前6个
        lis = response.css('ul.j-nav.smash-list li.j-nav-itemParent')

        for level in lis:
            results.append(
                self.get_category_tree(
                    level.css('a.j-link-parent::attr(href)').get(),
                    response.meta['RootId'],
                    level.css('a.j-link-parent').get()
                )
            )

            for level_two in level.xpath('./ul/li'):
                results.append(
                    self.get_category_tree(
                        level_two.xpath('./a/@href').get(),
                        response.meta['RootId'],
                        level.css('a.j-link-parent').get(),
                        level_two.xpath('./a/text()').get()
                    )
                )

                if len(level_two.xpath('./div')) == 0:
                    continue

                level_three_titles = level_two.css('p.j-title-list')
                level_three_uls = level_two.css('ul.smash-list')

                for index, ul in enumerate(level_three_uls):
                    for a in ul.css('a'):
                        results.append(
                            self.get_category_tree(
                                a.css('::attr(href)').get(),
                                response.meta['RootId'],
                                level.css('a.j-link-parent').get(),
                                level_two.xpath('./a/text()').get(),
                                level_three_titles[index].css('::text').get(),
                                a.css('::text').get()
                            )
                        )

        chambre = response.css('ul.j-nav.smash-list>li.j-nav-mega')
        results.append(
            self.get_category_tree(
                chambre.xpath('./a/@href').get(),
                response.meta['RootId'],
                chambre.xpath('./a/text()').get(),
            )
        )

        chambre_level_two_titles = chambre.css('p.j-title-list')
        chambre_level_two_uls = chambre.css('ul.smash-list')

        for index, ul in enumerate(chambre_level_two_uls):
            for a in ul.css('a'):
                results.append(
                    self.get_category_tree(
                        a.css('::attr(href)').get(),
                        response.meta['RootId'],
                        chambre.xpath('./a/text()').get(),
                        chambre_level_two_titles[index].css('::text').get(),
                        a.css('::text').get()
                    )
                )

        return results

    def get_category_tree(self, url, c_rootId, c_one, c_two='', c_three='', c_four=''):
        if url is None or url == '':
            return None
        category_tree = CategoryTree()
        category_itemloader = CategoryTreeItemLoader(item=category_tree)
        category_itemloader.add_value('Id', str(uuid.uuid4()))
        category_itemloader.add_value('RootId', c_rootId)
        category_itemloader.add_value('Level_Url', url)
        category_itemloader.add_value('ProjectName', BOT_NAME)
        category_itemloader.add_value('CategoryLevel1', c_one)
        category_itemloader.add_value('CategoryLevel2', c_two)
        category_itemloader.add_value('CategoryLevel3', c_three)
        category_itemloader.add_value('CategoryLevel4', c_four)
        category_itemloader.add_value('CategoryLevel5', '')

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