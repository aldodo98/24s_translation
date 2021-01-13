import scrapy
import datetime
import uuid
import random
from Marionnaud.items import CategoryTree, ProductInfo
from Marionnaud.itemloader import CategoryTreeItemLoader, ProductInfoItemLoader
from Marionnaud.settings import BOT_NAME
from scrapy.http.headers import Headers
from scrapy_redis.spiders import RedisSpider
import json

# class RoottaskspiderSpider(scrapy.Spider):
class RoottaskspiderSpider(RedisSpider):
    name = 'RootTaskSpider'
    redis_key = BOT_NAME + ':RootTaskSpider'
    allowed_domains = ['www.marionnaud.fr']
    start_urls = ['https://www.marionnaud.fr']
    second_cate_url = 'https://www.marionnaud.fr/brandslist'

    # def start_requests(self):
    #     urls = [
    #         "https://www.marionnaud.fr",
    #         # "https://www.marionnaud.fr/parfum/parfum-femme/eau-de-parfum/c/P0101", # 446
    #         # "https://www.marionnaud.fr/parfum/parfum-homme/eau-de-toilette/c/P0202"  # 247
    #         # 'https://www.marionnaud.fr/marques/b/melvita/100923'
    #         # 'https://www.marionnaud.fr/marques/b/darphin/100962'
    #         # 'https://www.marionnaud.fr/marques/b/ioma/100716'
    #         # 'https://www.marionnaud.fr/marques/b/elenature/100976'
    #     ]
    #     for url in urls:
    #         yield scrapy.Request(url=url, callback=self.parse, headers=random.choice(self.headers_list), meta={
    #             'RootId': '1'
    #         })

    # __init__方法必须按规定写，使用时只需要修改super()里的类名参数即可
    def __init__(self, *args, **kwargs):
        # 修改这里的类名为当前类名
        super(RoottaskspiderSpider, self).__init__(*args, **kwargs)

    def make_request_from_data(self, data):
        receivedDictData = json.loads(str(data, encoding="utf-8"))
        # print(receivedDictData)
        # here you can use and FormRequest
        formRequest = scrapy.FormRequest(url="https://www.marionnaud.fr", dont_filter=True,
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

    # 获取目录(只需获取前两个一级目录)
    def getCategory(self, response):
        success = response.status == 200
        if success:
            cate_list_1 = response.css('.navFirstLevelField ul.nav__list.list-inline>li')  # 一级目录元素列表
            for index, ele in enumerate(cate_list_1):
                cate_1 = self.start_urls[0] + ele.css('a::attr(title)').get() and ele.css(
                    'a::attr(title)').get().upper()  # 一级目录

                url_1 = ele.css('a::attr(href)').get()  # 一级目录商品url
                yield self.getCategoryItem(
                    cate_1,
                    None,
                    None,
                    None,
                    url_1,
                    response.meta['RootId']
                )

                if index == 0:
                    # self.getFirstCategory(response, url_1)
                    ele_list_2 = response.css('.nav-produit.sub-nav>ul>li')  # 二级目录元素列表
                    for _ele in ele_list_2:
                        cate_2 = _ele.css('a::attr(title)').get() and _ele.css('a::attr(title)').get().upper()  # 二级目录
                        url_2 = self.start_urls[0] + _ele.css('a::attr(href)').get()  # 二级目录商品url

                        yield self.getCategoryItem(
                            cate_1,
                            cate_2,
                            None,
                            None,
                            url_2,
                            response.meta['RootId']
                        )

                        cate_list_3 = _ele.css('ul.sub-navigation-container>li')  # 三级目录列表
                        for __ele in cate_list_3:
                            cate_3 = __ele.css('.yCmsComponent.dropdown>a::attr(title)').get() and __ele.css(
                                '.yCmsComponent.dropdown>a::attr(title)').get().upper()  # 三级目录
                            url_3 = self.start_urls[0] + __ele.css(
                                '.yCmsComponent.dropdown>a::attr(href)').get()  # 商品url
                            yield self.getCategoryItem(
                                cate_1,
                                cate_2,
                                cate_3,
                                None,
                                url_3,
                                response.meta['RootId']
                            )

                            cate_list_4 = __ele.css('.yCmsComponent.leaf-node')  # 四级目录列表
                            for ___ele in cate_list_4:
                                cate_4 = ___ele.css('a::attr(title)').get()  # 四级目录
                                url_4 = self.start_urls[0] + ___ele.css('a::attr(href)').get()  # 商品url
                                item_load = self.getCategoryItem(
                                    cate_1,
                                    cate_2,
                                    cate_3,
                                    cate_4,
                                    url_4,
                                    response.meta['RootId']
                                )
                                yield item_load

                elif index == 1:
                    yield scrapy.Request(url=self.second_cate_url,
                                         callback=self.getSecondCategory,
                                         headers=random.choice(self.headers_list), meta={
                            'RootId': '1', 'cate_1': cate_1
                        })

                else:
                    break

    # 获取第二个一级目录下所有子目录
    def getSecondCategory(self, response):
        ele_list_2 = response.css('.pag-listing>.openmobile')  # 二级目录元素列表
        ele_list_3 = response.css('.pag-listing>ul.brands-by-letter')  # 三级目录元素列表

        for inx, _ele in enumerate(ele_list_2):
            cate_2 = _ele.css('h2::text').get() and _ele.css('h2::text').get().strip()  # 二级目录
            ele_list_inx_3 = ele_list_3[inx].css('li.one-brand a')  # 三级元素列表

            for __ele in ele_list_inx_3:
                print(__ele.css('::text').get())
                if __ele.css('::text').get().strip() == '':  # 无内容的多余li，不操作
                    continue
                else:
                    cate_3 = __ele.css('a::attr(title)').get() and __ele.css('a::attr(title)').get().strip()  # 三级目录
                    url_2 = self.start_urls[0] + __ele.css('a::attr(href)').get()  # 三级url(二级无url)

                    item_load = self.getCategoryItem(
                        response.meta['cate_1'],
                        cate_2,
                        cate_3,
                        None,
                        url_2,
                        response.meta['RootId']
                    )
                    yield item_load


    def getCategoryItem(self, cate_1, cate_2, cate_3, cate_4, url, c_rootId=''):
        category_tree = CategoryTree()
        category_itemloader = CategoryTreeItemLoader(item=category_tree)
        category_itemloader.add_value('Id', str(uuid.uuid4()))

        category_itemloader.add_value('ProjectName', BOT_NAME)
        category_itemloader.add_value('Level_Url', url)
        category_itemloader.add_value('CategoryLevel1', cate_1)
        category_itemloader.add_value('CategoryLevel2', cate_2)
        category_itemloader.add_value('CategoryLevel3', cate_3)
        category_itemloader.add_value('CategoryLevel4', cate_4)

        time = datetime.datetime.now().isoformat()
        # category_itemloader.add_value('CreateDateTime', time)
        # category_itemloader.add_value('UpdateDateTime', time)

        category_itemloader.add_value('RootId', c_rootId)

        # category_itemloader.add_value('ManufacturerId', 12)
        # category_itemloader.add_value('CategoryId', 20)

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
