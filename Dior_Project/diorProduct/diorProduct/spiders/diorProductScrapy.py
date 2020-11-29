from datetime import datetime

import scrapy
import json
import random

from diorProduct.itemloader import VariableClassItemLoader, MarionnaudItemLoader
from diorProduct.items import Product, AttributeBasicInfoClass, ProductAttributeClass, MappingClass, VariableClass
from scrapy.selector import Selector
from scrapy.loader import ItemLoader


class Scrapytest1Spider(scrapy.Spider):
    name = 'diorProductScrapy'
    # start_urls = ['https://www.dior.com/en_us/products/couture-051R07A1238_X9330-short-dress-black-and-white-check-wool'

    def start_requests(self):
        urls =[
            # 'https://www.dior.cn/zh_cn/products/beauty-Y0996177-%E5%85%A8%E6%96%B0-%E8%BF%AA%E5%A5%A5%E7%83%88%E8%89%B3%E8%93%9D%E9%87%91%E5%94%87%E8%86%8F-%E6%9B%BF%E6%8D%A2%E8%8A%AF-%E9%AB%98%E8%AE%A2%E8%89%B2%E6%B3%BD-4%E6%AC%BE%E5%A6%86%E6%95%88-%E4%B8%9D%E7%BB%92%E3%80%81%E7%BC%8E%E5%85%89%E3%80%81%E5%93%91%E5%85%89%E3%80%81%E9%8E%8F%E9%87%91-%E8%8A%B1%E8%90%83%E6%B6%A6%E6%8A%A4-%E8%88%92%E6%82%A6%E6%8C%81%E8%89%B2-7%E6%AC%BE%E6%9B%BF%E6%8D%A2%E8%8A%AF%E4%BE%9B%E9%80%89%E8%B4%AD',
            # 'https://www.dior.cn/zh_cn/products/couture-051R09A1166_X9000-%E7%9F%AD%E6%AC%BE%E8%BF%9E%E8%A1%A3%E8%A3%99-%E9%BB%91%E8%89%B2%E7%BE%8A%E6%AF%9B%E5%92%8C%E6%A1%91%E8%9A%95%E4%B8%9D%E6%B7%B7%E7%BA%BA'
            # 'https://www.dior.cn/zh_cn/products/couture-HYJ01ATT1L_C970-%E9%A4%90%E7%9B%98%E5%A5%97%E8%A3%85%EF%BC%884-%E4%BB%B6%E8%A3%85%EF%BC%89-l-imperatrice%E3%80%81le-monde%E3%80%81l-amoureux%E3%80%81la-mort-%E5%9B%BE%E6%A1%88',
            # 'https://www.dior.cn/zh_cn/products/beauty-Y0670530-',
            # 'https://www.dior.cn/zh_cn/products/beauty-Y0771350-',
            'https://www.dior.cn/zh_cn/products/beauty-Y0670320-'
        ]
        for url in urls:
            # Pick a random browser headers
            headers = random.choice(self.headers_list)
            print(headers)
            yield scrapy.Request(url=url, callback=self.parse, headers=headers)

    def parse(self, response):
        product = Product()
        product['Success'] = response.status == 200
        if response.status == 200:
            self.oriResponse = response
            for filterRes in response.css('div.top-content-desktop-right'):
                # 获取基本信息
                text = filterRes.css('div.top-content-desktop-right').get()
                selector = Selector(text=text)
                productItemloader = MarionnaudItemLoader(item=product, response=text, selector=selector)
                productItemloader.add_value('TaskId', 'test')
                productItemloader.add_css('Name', 'span.multiline-text.product-titles-title::text')
                productItemloader.add_css('ShortDescription', 'span.multiline-text.product-titles-subtitle::text')

                productItemloader.add_css('Price', 'span.variation-option-price::text')
                productItemloader.add_css('Price', 'div.product-actions__price span.price-line::text')
                productItemloader.add_value('LastChangeTime', datetime.utcnow())
                productItemloader.add_css('FullDescription', 'div.product-description-item__content')
                item = productItemloader.load_item()
                # 获取属性
                productAttributes = self.getProductAttributes(filterRes)
                item['ProductAttributes'] = productAttributes
                yield item
        else:
            print('error!!!!!')

    headers_list = [
        # Chrome
        {
            'authority': 'www.marionnaud.fr',
            'cache-control': 'max-age=0',
            'sec-ch-ua': '"Chromium";v="86", "\\"Not\\\\A;Brand";v="99", "Google Chrome";v="86"',
            'sec-ch-ua-mobile': '?0',
            'dnt': '1',
            'upgrade-insecure-requests': '1',
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.75 Safari/537.36',
            'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
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
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.102 Safari/537.36 Edge/18.19041",
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
    def getColorAttribute(self, response):
        # attributeBasicInfo
        attributeBasicInfo = AttributeBasicInfoClass()
        attributeBasicInfo['Name'] = "Color"
        attributeBasicInfo['Description'] = ""

        # mapping
        mapping = MappingClass()
        mapping['TextPrompt'] = "Color"
        mapping['IsRequired'] = True
        mapping['AttributeControlTypeId'] = 2
        mapping['AttributeControlType'] = "RadioList"
        mapping['DisplayOrder'] = 0
        mapping['DefaultValue'] = ""

        productSiteAttribute = ProductAttributeClass()
        productSiteAttribute['AttributeBasicInfo'] = attributeBasicInfo
        productSiteAttribute['Mapping'] = mapping
        productSiteAttribute['Variables'] = self.getColorVariables(response)

        return productSiteAttribute

    def getSizeAttribute(self, response):
        # attributeBasicInfo
        attributeBasicInfo = AttributeBasicInfoClass()
        attributeBasicInfo['Name'] = "Size"
        attributeBasicInfo['Description'] = ""

        # mapping
        mapping = MappingClass()
        mapping['TextPrompt'] = "Size"
        mapping['IsRequired'] = True
        mapping['AttributeControlTypeId'] = 2
        mapping['AttributeControlType'] = "RadioList"
        mapping['DisplayOrder'] = 0
        mapping['DefaultValue'] = ""

        productSiteAttribute = ProductAttributeClass()
        productSiteAttribute['AttributeBasicInfo'] = attributeBasicInfo
        productSiteAttribute['Mapping'] = mapping
        productSiteAttribute['Variables'] = self.getSizeVariables(response)

        return productSiteAttribute

    def getColorVariables(self, response):
        colorList = response.css('div.generic-variations span.swatch.variation')
        list = response.css('#variation-selection-options li')
        result = []
        for index in range(len(colorList)):
            # colorItem.css('div.image img::attr("src")')
            colorUrl = colorList[index].css('div.image img::attr("src")').get()
            loadItem = self.setSizeOrColorWithDetailInfo(list[index], colorUrl)
            result.append(loadItem)
            # attributeVariable = VariableClass()
            # variableClassItemLoader = VariableClassItemLoader(item=attributeVariable, response=response)
            # variableClassItemLoader.add_value('DataCode', item.css('::attr("data-code")').get())
            # variableClassItemLoader.add_value('NewPrice', item.css('::attr("data-igc-markdown-price")').get())
            # variableClassItemLoader.add_value('OldPrice', item.css('::attr("data-price")').get())
            #
            # variableClassItemLoader.add_value('Name', item.css('::text').get())
            # variableClassItemLoader.add_value('ColorSquaresRgb', item.css('::attr("data-color")').get())
            # variableClassItemLoader.add_value('DisplayColorSquaresRgb', False)
            # variableClassItemLoader.add_value('PriceAdjustment', 0)
            # variableClassItemLoader.add_value('PriceAdjustmentUsePercentage', False)
            #
            # variableClassItemLoader.add_value('IsPreSelected', len(item.css('span.selected')) > 0)
            # variableClassItemLoader.add_value('DisplayOrder', False)
            # variableClassItemLoader.add_value('DisplayImageSquaresPicture', False)
            # variableClassItemLoader.add_value('PictureUrlInStorage', '')
            # loadItem = variableClassItemLoader.load_item()

        return result

    def getSizeVariables(self, response):
        list = response.css('#variation-selection-options li')
        list2 = response.css('#size-selector-options li')
        print('list2',list2)
        result = []
        for item in (list if len(list) > 0 else list2):
            # text = item.get()
            # selector = Selector(text=text)
            # attributeVariable = VariableClass()
            # variableClassItemLoader = VariableClassItemLoader(item=attributeVariable, response=text, selector=selector)
            # variableClassItemLoader.add_value('DataCode', item.css('li::attr("id")').get())
            # variableClassItemLoader.add_css('NewPrice', 'span.variation-option-price::text')
            # variableClassItemLoader.add_value('OldPrice', '')
            #
            # variableClassItemLoader.add_css('Name', '.variation-option-infos-titles span::text')
            # variableClassItemLoader.add_value('ColorSquaresRgb', '')
            # variableClassItemLoader.add_value('DisplayColorSquaresRgb', False)
            # variableClassItemLoader.add_value('PriceAdjustment', 0)
            # variableClassItemLoader.add_value('PriceAdjustmentUsePercentage', False)
            #
            # variableClassItemLoader.add_value('IsPreSelected', len(item.css('span.is-selected')) > 0)
            # variableClassItemLoader.add_value('DisplayOrder', False)
            # variableClassItemLoader.add_value('DisplayImageSquaresPicture', False)
            # variableClassItemLoader.add_value('PictureUrlInStorage', '')
            # loadItem = variableClassItemLoader.load_item()
            loadItem = self.setSizeOrColorWithDetailInfo(item)
            result.append(loadItem)
        return result

    def getProductAttributes(self, response):
        result = []
        # 美妆类
        sizeLinklist = response.css('#variation-selection-options li')
        # 鞋靴类
        sizeLinklist2 = response.css('#size-selector-options li')
        print(sizeLinklist2)
        colorSelectorList = response.css('div.generic-variations span.swatch.variation')
        if (len(sizeLinklist) > 0 or len(sizeLinklist2) > 0) and len(colorSelectorList) == 0:
            sizeAttri = self.getSizeAttribute(response)
            result.append(sizeAttri)

        # colorlist = response.css('div.generic-variations')
        if len(colorSelectorList) > 0:
            colorAttri = self.getColorAttribute(response)
            result.append(colorAttri)

        return result

    def setSizeOrColorWithDetailInfo(self, item, picUrl=''):
        text = item.get()
        selector = Selector(text=text)
        attributeVariable = VariableClass()
        variableClassItemLoader = VariableClassItemLoader(item=attributeVariable, response=text, selector=selector)
        variableClassItemLoader.add_value('DataCode', item.css('li::attr("id")').get())
        variableClassItemLoader.add_css('NewPrice', 'span.variation-option-price::text')
        variableClassItemLoader.add_value('NewPrice', self.oriResponse.css('div.product-actions__price span.price-line::text').get())
        variableClassItemLoader.add_value('OldPrice', '')

        variableClassItemLoader.add_css('Name', '.variation-option-infos-titles span::text')
        variableClassItemLoader.add_css('Name', '.size-title::text')

        variableClassItemLoader.add_value('ColorSquaresRgb', '')
        variableClassItemLoader.add_value('ColorSquaresRgb', picUrl)
        variableClassItemLoader.add_value('DisplayColorSquaresRgb', False)
        variableClassItemLoader.add_value('PriceAdjustment', 0)
        variableClassItemLoader.add_value('PriceAdjustmentUsePercentage', False)

        variableClassItemLoader.add_value('IsPreSelected', len(item.css('span.is-selected')) > 0)
        variableClassItemLoader.add_value('DisplayOrder', False)
        variableClassItemLoader.add_value('DisplayImageSquaresPicture', False)
        variableClassItemLoader.add_value('PictureUrlInStorage', '')
        loadItem = variableClassItemLoader.load_item()
        return loadItem