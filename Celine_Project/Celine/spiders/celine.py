import scrapy
import datetime
import uuid
import random
from string import Template
from Celine.items import CategoryTree, ProductInfo, TreeLevel
from Celine.itemloader import CategoryTreeItemLoader, ProductInfoItemLoader


class CelineSpider(scrapy.Spider):
    name = 'celine'
    allowed_domains = ['www.celine.com']
    main_url = "https://www.celine.com"

    def start_requests(self):
        urls = [
            "https://www.celine.com/fr-fr/home",
            # "https://www.celine.com/fr-fr/celine-boutique-femme/petite-maroquinerie/",
            # "https://www.celine.com/fr-fr/celine-boutique-femme/sacs/16/"
        ]

        for url in urls:
            yield scrapy.Request(url=url, callback=self.parse, meta={
                        'Type': 'menu',
                    }, headers=random.choice(self.headers_list))

    def parse(self, response):
        try:
            return self.parseP(response=response)
        except Exception as err:
            print(err)

    def parseP(self, response):
        success = response.status == 200
        if success:
            levels = self.generate_levels(response)


            for node in levels:
                print(node)
                yield node
                yield scrapy.Request(url=node['Level_Url'], callback=self.getProducts, meta={
                            'CategoryId': node['Id'],
                            'Type': 'product'
                        }, headers=random.choice(self.headers_list))

    def getProducts(self, response):
        category_id = response.meta['CategoryId']
        # lists = response.css('ul.o-listing-grid li a')
        lists = list()
        products_in_list = response.css('ul.o-listing-grid li a')
        products_in_row = response.css('ul.o-listing-row li a')

        if len(products_in_list) > 0:
            lists.extend(products_in_list)

        if len(products_in_row) > 0:
            lists.extend(products_in_row)

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
        results = list()
        for level in response.css('a.a-btn.a-btn--as-link[data-level="0"]')[:2]:
            s = Template('[aria-labelledby="${Level_Id}"]')
            s_selector = s.substitute(Level_Id=level.css("::attr(id)").get())

            title_one_list = response.css('div[data-level="1"]' + s_selector + '>ul>li:not(.s-hide-on-desktop) a['
                                                                               'data-level="1"]')
            for title in title_one_list:
                catrgory_tree_one = self.get_category_tree(
                    title.css('::attr(href)').get(),
                    level.css('::text').get(),
                    title.css('::text').get(),
                )
                results.append(catrgory_tree_one)
            title_two_list = response.css('div[data-level="1"]' + s_selector + '>ul>li')
            for item in title_two_list:
                for li in item.css('ul>li:not(.s-hide-on-desktop)'):
                    catrgory_tree_two = self.get_category_tree(
                        li.css('a::attr(href)').get(),
                        level.css('::text').get(),
                        item.css('a:first-of-type::text').get(),
                        li.css('a::text').get()
                    )
                    results.append(catrgory_tree_two)

        return results

    def get_category_tree(self, url, c_one, c_two, c_three=''):

        category_tree = CategoryTree()
        category_itemloader = CategoryTreeItemLoader(item=category_tree)
        category_itemloader.add_value('Id', str(uuid.uuid4()))
        if self.main_url not in url:
            category_itemloader.add_value('Level_Url', self.main_url + url)
        else:
            category_itemloader.add_value('Level_Url', url)

        category_itemloader.add_value('CategoryLevel1', c_one)
        category_itemloader.add_value('CategoryLevel2', c_two)
        category_itemloader.add_value('CategoryLevel3', c_three)
        category_itemloader.add_value('CategoryLevel4', '')
        category_itemloader.add_value('CategoryLevel5', '')

        time = datetime.datetime.now().isoformat()
        category_itemloader.add_value('CreateDateTime', time)
        category_itemloader.add_value('UpdateDateTime', time)

        category_itemloader.add_value('ManufacturerId', 12)
        category_itemloader.add_value('CategoryId', 20)

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
