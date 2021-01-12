import scrapy
import datetime
import uuid
import random
from Matchfashion.items import CategoryTree, ProductInfo, TreeLevel
from Matchfashion.itemloader import CategoryTreeItemLoader, ProductInfoItemLoader
from scrapy.http.headers import Headers
from scrapy_redis.spiders import RedisSpider
from Matchfashion.settings import BOT_NAME
import json
from string import Template

# class MatchfashionSpider(RedisSpider):
class MatchfashionSpider(scrapy.Spider):
    redis_key = BOT_NAME + ':RootTaskSpider'
    name = 'RootTaskSpider'
    allowed_domains = ['www.matchesfashion.com']
    main_url = 'https://www.matchesfashion.com'

    # __init__方法必须按规定写，使用时只需要修改super()里的类名参数即可
    def __init__(self, *args, **kwargs):
        # 修改这里的类名为当前类名
        super(MatchfashionSpider, self).__init__(*args, **kwargs)

    def make_request_from_data(self, data):
        receivedDictData = json.loads(str(data, encoding="utf-8"))
        # print(receivedDictData)
        # here you can use and FormRequest
        formRequest = scrapy.FormRequest(url="https://fr.maje.com",dont_filter=True,
                                         meta={'RootId': receivedDictData['Id']})
        formRequest.headers = Headers(random.choice(self.headers_list))
        return formRequest

    def schedule_next_requests(self):
        for request in self.next_requests():
            request.headers = Headers(random.choice(self.headers_list))
            self.crawler.engine.crawl(request, spider=self)

    def start_requests(self):
        urls = [
            "https://www.matchesfashion.com/intl/womens"
        ]
        for url in urls:
            yield scrapy.Request(url=url, callback=self.parse, headers=random.choice(self.headers_list), meta={
                'RootId': '1'
            })

    def parse(self, response):

        success = response.status == 200
        if success:
            levels = self.generate_levels(response)
            for node in levels:
                print(node)
                yield node

    def generate_levels(self, response):
        results = list()
        firstLevel = response.css('#nav_main>ul>li')[:8]
        for level in firstLevel:
            # 一级菜单
            title_one = level.css('li.main-menu__item>span>a')
            title_one_title = title_one.css('a::text').get()
            catrgory_tree_one = self.get_category_tree(
                    title_one.css('a::attr(href)').get(),
                    title_one_title,
                    '',
                    '',
                    response.meta['RootId']
                )
            results.append(catrgory_tree_one)
            if title_one_title == 'Sale':
                title_two_list = level.css('.sub_menu__wrapper>div.submenu__promo>div.sale>div')
                for sec_level in title_two_list:
                    title_two_ele = sec_level.css('p').get()
                    if title_two_ele is None:
                        continue
                    else:
                        title_two_title = sec_level.css('p::text').get()
                        if (sec_level.css('p::text').get()) is None:
                            title_two_title = title_two_list[0].css('p::text').get()
                        title_three_list = sec_level.css('p~a')
                        for third_level in title_three_list:
                            title_three_title = third_level.css('a::text').get()
                            if title_three_title is None:
                                continue
                            catrgory_tree_three = self.get_category_tree(
                                third_level.css('a::attr(href)').get(),
                                title_one_title,
                                title_two_title,
                                title_three_title,
                                response.meta['RootId']
                            )
                            results.append(catrgory_tree_three)
            elif title_one_title == 'Just In':
                title_two_title = level.css('.sub_menu__wrapper .just-in__links p::text').get()
                title_three_list = level.css('.sub_menu__wrapper .just-in__links a')
                for third_level in title_three_list:
                    title_three_title = third_level.css('a::text').get()
                    catrgory_tree_three = self.get_category_tree(
                        third_level.css('a::attr(href)').get(),
                        title_one_title,
                        title_two_title,
                        title_three_title,
                        response.meta['RootId']
                    )
                    results.append(catrgory_tree_three)
            elif title_one_title == 'Stories':
                break
            else:
                # 二级菜单
                title_two_list = level.css('.sub_menu__wrapper>div:nth-child(1)>div')
                for sec_level in title_two_list:
                    title_two_title = sec_level.css('h3::text').get()
                    # catrgory_tree_two = self.get_category_tree(
                    #     sec_level.css('div[role="heading"] a::attr(href)').get(),
                    #     title_one_title,
                    #     title_two_title,
                    #     '',
                    #     # response.meta['RootId']
                    # )
                    # results.append(catrgory_tree_two)
                    title_three_list = sec_level.css('ul>li')
                    for third_level in title_three_list:
                        title_three_title = third_level.css('a::text').get()
                        if title_three_title is None:
                            continue
                        catrgory_tree_three = self.get_category_tree(
                            third_level.css('a::attr(href)').get(),
                            title_one_title,
                            title_two_title,
                            title_three_title,
                            response.meta['RootId']
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