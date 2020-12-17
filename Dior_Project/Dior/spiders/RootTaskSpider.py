import scrapy
import uuid
import random
from Dior.items import CategoryTree, ProductInfo, TreeLevel
from Dior.itemloader import CategoryTreeItemLoader, ProductInfoItemLoader
from scrapy.http.headers import Headers
from scrapy_redis.spiders import RedisSpider
from Dior.settings import BOT_NAME
import json
from string import Template


# class CelineRootTaskSpider(RedisSpider):
#     name = "RootTaskSpider"
#     redis_key = BOT_NAME+':RootTaskSpider'
#     main_url = "https://www.celine.com"
#     allowed_domains = ['www.celine.com']
#
#     # __init__方法必须按规定写，使用时只需要修改super()里的类名参数即可
#     def __init__(self, *args, **kwargs):
#         # 修改这里的类名为当前类名
#         super(CelineRootTaskSpider, self).__init__(*args, **kwargs)
#
#     def make_request_from_data(self, data):
#         receivedDictData = json.loads(str(data, encoding="utf-8"))
#         # print(receivedDictData)
#         # here you can use and FormRequest
#         formRequest = scrapy.FormRequest(url="https://www.celine.com/fr-fr/home",dont_filter=True,
#                                          meta={'RootId': receivedDictData['Id']})
#         formRequest.headers = Headers(random.choice(self.headers_list))
#         return formRequest
#
#     def schedule_next_requests(self):
#         for request in self.next_requests():
#             request.headers = Headers(random.choice(self.headers_list))
#             self.crawler.engine.crawl(request, spider=self)
#
#     def parse(self, response):
#         success = response.status == 200
#         if success:
#             levels = self.generate_levels(response)
#             for node in levels:
#                 print(node)
#                 yield node
#
#     def generate_levels(self, response):
#         results = list()
#         for level in response.css('a.a-btn.a-btn--as-link[data-level="0"]')[:2]:
#             s = Template('[aria-labelledby="${Level_Id}"]')
#             s_selector = s.substitute(Level_Id=level.css("::attr(id)").get())
#
#             title_one_list = response.css('div[data-level="1"]' + s_selector + '>ul>li:not(.s-hide-on-desktop) a['
#                                                                                'data-level="1"]')
#             for title in title_one_list:
#                 catrgory_tree_one = self.get_category_tree(
#                     title.css('::attr(href)').get(),
#                     level.css('::text').get(),
#                     title.css('::text').get(),
#                     '',
#                     response.meta['RootId']
#                 )
#                 results.append(catrgory_tree_one)
#             title_two_list = response.css('div[data-level="1"]' + s_selector + '>ul>li')
#             for item in title_two_list:
#                 for li in item.css('ul>li:not(.s-hide-on-desktop)'):
#                     catrgory_tree_two = self.get_category_tree(
#                         li.css('a::attr(href)').get(),
#                         level.css('::text').get(),
#                         item.css('a:first-of-type::text').get(),
#                         li.css('a::text').get(),
#                         response.meta['RootId']
#                     )
#                     results.append(catrgory_tree_two)
#
#         return results
#
#     def get_category_tree(self, url, c_one, c_two, c_three='', c_rootId=''):
#
#         category_tree = CategoryTree()
#         category_itemloader = CategoryTreeItemLoader(item=category_tree)
#         category_itemloader.add_value('Id', str(uuid.uuid4()))
#         category_itemloader.add_value('RootId', c_rootId)
#         if self.main_url not in url:
#             category_itemloader.add_value('Level_Url', self.main_url + url)
#         else:
#             category_itemloader.add_value('Level_Url', url)
#
#         category_itemloader.add_value('ProjectName', BOT_NAME)
#         category_itemloader.add_value('CategoryLevel1', c_one)
#         category_itemloader.add_value('CategoryLevel2', c_two)
#         category_itemloader.add_value('CategoryLevel3', c_three)
#         category_itemloader.add_value('CategoryLevel4', '')
#         category_itemloader.add_value('CategoryLevel5', '')
#
#         item_load = category_itemloader.load_item()
#         return item_load
#
#     headers_list = [
#         # Chrome
#         {
#             'authority': 'www.marionnaud.fr',
#             'cache-control': 'max-age=0',
#             'sec-ch-ua': '"Chromium";v="86", "\\"Not\\\\A;Brand";v="99", "Google Chrome";v="86"',
#             'sec-ch-ua-mobile': '?0',
#             'dnt': '1',
#             'upgrade-insecure-requests': '1',
#             'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) '
#                           'Chrome/86.0.4240.75 Safari/537.36',
#             'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,'
#                       '*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
#             'sec-fetch-site': 'none',
#             'sec-fetch-mode': 'navigate',
#             'sec-fetch-user': '?1',
#             'sec-fetch-dest': 'document',
#             'accept-language': 'en,fr;q=0.9,en-US;q=0.8,zh-CN;q=0.7,zh;q=0.6',
#         },
#         # IE
#         {
#             "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
#             "Accept-Encoding": "gzip, deflate, br",
#             "Accept-Language": "fr-FR,fr;q=0.8,en-US;q=0.7,en;q=0.5,zh-Hans-CN;q=0.3,zh-Hans;q=0.2",
#             "Upgrade-Insecure-Requests": "1",
#             "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) "
#                           "Chrome/70.0.3538.102 Safari/537.36 Edge/18.19041",
#         },
#         # Firefox
#         {
#             'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:82.0) Gecko/20100101 Firefox/82.0',
#             'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
#             'Accept-Language': 'en-US,en;q=0.5',
#             'Connection': 'keep-alive',
#             'Upgrade-Insecure-Requests': '1',
#             'Cache-Control': 'max-age=0',
#             'TE': 'Trailers',
#         }
#     ]

class DiorSpider(RedisSpider):
    name = 'RootTaskSpider'
    main_url = 'https://www.dior.com'
    redis_key = BOT_NAME + ':RootTaskSpider'
    allowed_domains = ['https://www.dior.com']
    # def start_requests(self):
    #     urls = [
    #         "https://www.dior.com/fr_fr"
    #     ]
    #     for url in urls:
    #         yield scrapy.Request(url=url, callback=self.parse, headers=random.choice(self.headers_list))

    def __init__(self, *args, **kwargs):
            super(DiorSpider, self).__init__(*args, **kwargs)

    def make_request_from_data(self, data):
        receivedDictData = json.loads(str(data, encoding="utf-8"))
        # print(receivedDictData)
        # here you can use and FormRequest
        formRequest = scrapy.FormRequest(url="https://www.dior.com/fr_fr",dont_filter=True,
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
            levels = self.generate_levels(response)
            for node in levels:
                print(node)
                yield node

    def generate_levels(self, response):
        results = list()
        for level in response.css('ul.navigation-desktop-menu>li.navigation-tab'):
            # 一级菜单
            title_one = level.css('div.navigation-tab-head')
            title_one_title = title_one.css('span::text').get()
            catrgory_tree_one = self.get_category_tree(
                    title_one.css('a::attr(href)').get(),
                    title_one_title,
                    ''
                    '',
                    response.meta['RootId']
                )
            results.append(catrgory_tree_one)
            # 二级菜单
            title_two_list = level.css('.navigation-tab-content>ul>li.navigation-tab-content-column')
            for sec_level in title_two_list:
                title_two_title = sec_level.css('div[role="heading"] .multiline-text::text').get()
                if title_three_title is None:
                    break
                catrgory_tree_two = self.get_category_tree(
                    sec_level.css('div[role="heading"] a::attr(href)').get(),
                    title_one_title,
                    title_two_title,
                    '',
                    response.meta['RootId']
                )
                results.append(catrgory_tree_two)
                title_three_list = sec_level.css('.navigation-desktop-section-link')
                for third_level in title_three_list:
                    title_three_title = third_level.css('span::text').get()
                    catrgory_tree_three = self.get_category_tree(
                        third_level.css('a::attr(href)').get(),
                        title_one_title,
                        title_two_title,
                        title_three_title
                    )
                    results.append(catrgory_tree_three)

        return results

    def get_category_tree(self, url, c_one, c_two='', c_three='', c_rootId=''):
        if url is None:
            return None
        category_tree = CategoryTree()
        category_itemloader = CategoryTreeItemLoader(item=category_tree)
        category_itemloader.add_value('Id', str(uuid.uuid4()))
        category_itemloader.add_value('RootId', c_rootId)
        if self.main_url not in url:
            category_itemloader.add_value('Level_Url', self.main_url + url)
        else:
            category_itemloader.add_value('Level_Url', url)

        category_itemloader.add_value('ProjectName', BOT_NAME)
        category_itemloader.add_value('CategoryLevel1', c_one)
        category_itemloader.add_value('CategoryLevel2', c_two)
        category_itemloader.add_value('CategoryLevel3', c_three)
        category_itemloader.add_value('CategoryLevel4', '')
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