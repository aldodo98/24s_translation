import scrapy
import datetime
import uuid
import random
from Celine.items import CategoryTree, ProductInfo, TreeLevel
from Celine.itemloader import CategoryTreeItemLoader, ProductInfoItemLoader


class CelineSpider(scrapy.Spider):
    name = 'celine'
    allowed_domains = ['www.celine.com']
    main_url = "https://www.celine.com"

    def start_requests(self):
        urls = [
            "https://www.celine.com/fr-fr/home"
        ]
        for url in urls:
            yield scrapy.Request(url=url, callback=self.parse, headers=random.choice(self.headers_list))

    def parse(self, response):
        try:
            return self.parseP(response=response)
        except Exception as err:
            print(err)

    def parseP(self, response):
        success = response.status == 200
        if success:
            levels = self.generate_levels(response)
            first = levels['1']
            second = levels['2']
            third = levels['3']
            for item in third:
                level_two = ''
                level_one = ''
                for l in second:
                    if level_two != '':
                        for f in first:
                            if l['DomParentId'] == f['DomId']:
                                level_one = f['Name']
                                break
                        break
                    else:
                        for u in l['Urls']:
                            if item['DomParentId'] == u['DomId']:
                                level_two = u['Name']
                                break
                if level_one == '':
                    break

                for url in item['Urls']:
                    category_tree = CategoryTree()
                    category_itemloader = CategoryTreeItemLoader(item=category_tree, response=response)
                    category_itemloader.add_value('Id', str(uuid.uuid4()))
                    if self.main_url not in url['Url']:
                        category_itemloader.add_value('Level_Url', self.main_url + url['Url'])
                    else:
                        category_itemloader.add_value('Level_Url', url['Url'])

                    category_itemloader.add_value('CategoryLevel1', level_one)
                    category_itemloader.add_value('CategoryLevel2', level_two)
                    category_itemloader.add_value('CategoryLevel3', url['Name'])
                    category_itemloader.add_value('CategoryLevel4', '')
                    category_itemloader.add_value('CategoryLevel5', '')

                    time = datetime.datetime.now().isoformat()
                    category_itemloader.add_value('CreateDateTime', time)
                    category_itemloader.add_value('UpdateDateTime', time)

                    category_itemloader.add_value('ManufacturerId', 12)
                    category_itemloader.add_value('CategoryId', 20)

                    item_load = category_itemloader.load_item()

                    yield item_load
                    yield scrapy.Request(url=item_load['Level_Url'], callback=self.getProducts, meta={
                        'CategoryId': item_load['Id']
                    }, headers=random.choice(self.headers_list))

            urls = response.css('nav div.a17-grid__right a.a-btn.a-btn--as-link::attr(href)').extract()

            # for url in set(urls):
            #     category_tree = CategoryTree()
            #     category_itemloader = CategoryTreeItemLoader(item=category_tree, response=response)
            #     category_itemloader.add_value('Id', str(uuid.uuid4()))
            #
            #     if self.main_url not in url:
            #         category_itemloader.add_value('Level_Url', self.main_url + url)
            #     else:
            #         category_itemloader.add_value('Level_Url', url)
            #
            #     levels = self.getLevels(url)
            #     category_itemloader.add_value('CategoryLevel1', levels[1])
            #     category_itemloader.add_value('CategoryLevel2', levels[2])
            #     category_itemloader.add_value('CategoryLevel3', levels[3])
            #     category_itemloader.add_value('CategoryLevel4', levels[4])
            #     category_itemloader.add_value('CategoryLevel5', levels[5])
            #
            #     time = datetime.datetime.now().isoformat()
            #     category_itemloader.add_value('CreateDateTime', time)
            #     category_itemloader.add_value('UpdateDateTime', time)
            #
            #     category_itemloader.add_value('ManufacturerId', 12)
            #     category_itemloader.add_value('CategoryId', 20)
            #
            #     item_load = category_itemloader.load_item()
            #
            #     yield item_load
            #     yield scrapy.Request(url=item_load['Level_Url'], callback=self.getProducts, meta={
            #         'CategoryId': item_load['Id']
            #     }, headers=random.choice(self.headers_list))

    def getProducts(self, response):
        category_id = response.meta['CategoryId']
        lists = response.css('ul.o-listing-grid li a')
        for item in lists:
            product_info = ProductInfo()
            product_itemloader = ProductInfoItemLoader(item=product_info, response=response)
            product_itemloader.add_value('CategoryTreeId', category_id)
            product_itemloader.add_value('Id', str(uuid.uuid4()))

            product_itemloader.add_value('ProductUrl', self.main_url + item.css('::attr(href)').get())
            product_itemloader.add_value('ProductName', item.css('.m-product-listing__meta-title.f-body::text').get())
            product_itemloader.add_value('Price', item.css('strong.f-body--em::text').get())

            product_itemloader.add_value('Seconds', 60)
            product_itemloader.add_value('Enabled', 0)
            product_itemloader.add_value('Status', 'Running')

            yield product_itemloader.load_item()

    def getLevels(self, url):
        level_list = url.split('/')
        level_list = level_list + [None] * (6 - len(level_list))
        return level_list

    def generate_levels(self, response):
        levels = dict()
        first = list()
        second = list()
        third = list()
        for level in response.css('a.a-btn.a-btn--as-link[data-level="0"]'):
            tree_level = TreeLevel()
            tree_level['Level'] = level.css('::attr(data-level)').get()
            tree_level['Name'] = level.css('::text').get()
            tree_level['DomId'] = level.css('::attr(id)').get()
            first.append(tree_level)
        levels['1'] = first

        for level in response.css('div[data-level="1"]'):
            second_list = list()
            tree_level = TreeLevel()
            tree_level['Level'] = level.css('::attr(data-level)').get()
            tree_level['DomParentId'] = level.css('::attr(aria-labelledby)').get()
            tree_level['Urls'] = list(map(self.get_second_names, level.css('ul:first-of-type>li>a[data-level="1"]')))
            second.append(tree_level)
        levels['2'] = second

        for level in response.css('div[data-level="2"]'):
            tree_level = TreeLevel()
            tree_level['Level'] = level.css('::attr(data-level)').get()
            tree_level['DomParentId'] = level.css('::attr(aria-labelledby)').get()
            tree_level['Urls'] = list(map(self.get_level_urls, level.css('a')))
            third.append(tree_level)
        levels['3'] = third
        return levels

    def get_level_urls(self, a):
        level = dict()
        level['Url'] = a.css('::attr(href)').get()
        level['Name'] = a.css('::text').get()
        return level

    def get_second_names(self, a):
        tree_level = TreeLevel()
        tree_level['Name'] = a.css('::text').get()
        tree_level['DomId'] = a.css('::attr(id)').get()
        return tree_level

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
