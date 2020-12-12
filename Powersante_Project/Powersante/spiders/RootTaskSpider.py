import scrapy
import datetime
import uuid
import random
from Powersante.items import CategoryTree, ProductInfo
from Powersante.itemloader import CategoryTreeItemLoader, ProductInfoItemLoader
from Powersante.settings import BOT_NAME


class RoottaskspiderSpider(scrapy.Spider):
    name = 'RootTaskSpider'
    redis_key = BOT_NAME+':RootTaskSpider'
    allowed_domains = ['www.powersante.com']
    start_urls = ['http://www.powersante.com/']

    def start_requests(self):
        urls = [
            "https://www.powersante.com",
            # "https://www.powersante.com/bebe-maman/grossesse-allaitement/tests-d-ovulation-et-tests-de-grossesse/",
            # 'https://www.powersante.com/visage/peaux-sensibles-et-atopiques/lotions-toniques/'
            # "https://www.powersante.com/parfum-maquillage/ongles/soins-des-ongles/",
            # 'https://www.powersante.com/visage/nettoyants-demaquillants/laits-huiles/#q=&idx=magento_default_products'
            # '&hFR%5Bcategories.level0%5D%5B0%5D=Visage%20%2F%2F%2F%20Nettoyants%20%26%20D%C3%A9maquillants%20%2F%2F'
            # '%2F%20Laits%20%26%20Huiles&is_v=1 '
        ]
        for url in urls:
            yield scrapy.Request(url=url, callback=self.parse, headers=random.choice(self.headers_list), meta={
                'RootId': '1'
            })
            # yield scrapy.Request(url=url, callback=self.getProducts, headers=random.choice(self.headers_list), meta={
            #     'CategoryId': '1'
            # })

    def parse(self, response):
        try:
            return self.getCategory(response=response)
        except Exception as err:
            print(err)

    # 获取目录
    def getCategory(self, response):
        success = response.status == 200
        if success:
            cate_list_1 = response.css('#responsive-menu>div.section>ul>li:not(.toplinks)')  # 一级目录元素列表

            for ele in cate_list_1:
                cate_1 = ele.css('a::text').get()  # 一级目录
                # url_1 = ele.css('a::attr(href)').get()  # 一级目录商品url
                ele_list_2 = ele.css('.section>.section_inner>ul>li:not(.back):not(.title):not(.all)')  # 二级目录元素列表
                # yield self.getCategoryItem(
                #     cate_1,
                #     None,
                #     None,
                #     url_1,
                #     response.meta['RootId']
                # )

                for _ele in ele_list_2:
                    cate_2 = _ele.css('a::text').get()  # 二级目录
                    url_2 = _ele.css('a::attr(href)').get()  # 二级目录商品url
                    cate_list_3 = _ele.css('.section>ul>li:not(.back):not(.title):not(.all)')  # 三级目录列表
                    yield self.getCategoryItem(
                        cate_1,
                        cate_2,
                        None,
                        url_2,
                        response.meta['RootId']
                    )

                    for __ele in cate_list_3:
                        cate_3 = __ele.css('a::text').get()  # 三级目录
                        url_3 = __ele.css('a::attr(href)').get()  # 商品url
                        item_load = self.getCategoryItem(
                            cate_1,
                            cate_2,
                            cate_3,
                            url_3,
                            response.meta['RootId']
                        )
                        yield item_load
                        yield scrapy.Request(url=url_3, callback=self.getProducts, meta={
                            'CategoryId': item_load['Id'],
                        }, headers=random.choice(self.headers_list))

    def getCategoryItem(self, cate_1, cate_2, cate_3, url, c_rootId=''):
        category_tree = CategoryTree()
        category_itemloader = CategoryTreeItemLoader(item=category_tree)
        category_itemloader.add_value('Id', str(uuid.uuid4()))

        category_itemloader.add_value('ProjectName', BOT_NAME)
        category_itemloader.add_value('Level_Url', url)
        category_itemloader.add_value('CategoryLevel1', cate_1)
        category_itemloader.add_value('CategoryLevel2', cate_2)
        category_itemloader.add_value('CategoryLevel3', cate_3)

        time = datetime.datetime.now().isoformat()
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
