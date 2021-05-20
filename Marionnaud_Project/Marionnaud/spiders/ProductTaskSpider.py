import scrapy
import random
from Marionnaud.items import Product
from Marionnaud.itemloader import ProductItemLoader
from scrapy.http.headers import Headers
# from scrapy_redis.spiders import RedisSpider
import json
from Marionnaud.settings import BOT_NAME
from datetime import datetime
# import datetime
from datetime import datetime
from Marionnaud.items import Product, AttributeBasicInfoClass, MappingClass, ProductAttributeClass, VariableClass, ProductAdditionalProcessData
from Marionnaud.itemloader import ProductItemLoader, VariableClassItemLoader
from scrapy.http.headers import Headers
from scrapy_redis.spiders import RedisSpider

# class ProducttaskspiderSpider(scrapy.Spider):
class ProducttaskspiderSpider(RedisSpider):
    name = 'ProductTaskSpider'
    redis_key = BOT_NAME + ':ProductTaskSpider'
    allowed_domains = ['www.marionnaud.fr']
    variantUrl = "https://www.marionnaud.fr/p/variantImageData?code="

    # __init__方法必须按规定写，使用时只需要修改super()里的类名参数即可
    def __init__(self, *args, **kwargs):
        # 修改这里的类名为当前类名
        super(ProducttaskspiderSpider, self).__init__(*args, **kwargs)

    def make_request_from_data(self, data):
        receivedDictData = json.loads(str(data, encoding="utf-8"))
        # print(receivedDictData)
        # here you can use and FormRequest
        formRequest = scrapy.FormRequest(url=receivedDictData['ProductUrl'], dont_filter=True,
                                         meta={'TaskId': receivedDictData['Id']})
        return formRequest

    def parse(self, response):
        try:
            return self.parseP(response=response)
        except Exception as err:
            print(err)

    def parseP(self, response):
        product = Product()
        product['Success'] = response.status == 200
        if response.status == 200:
            productItemloader = ProductItemLoader(
                item=product, response=response)
            productItemloader.add_value('TaskId', response.meta['TaskId'])
            productItemloader.add_value('Name', self.getProductName(response))
            productItemloader.add_value('ShortDescription', '')
            productItemloader.add_value('FullDescription', response.xpath(
                '//div[@class="productInformationSection"]/div[@class="row"][1]').get())
            productItemloader.add_value(
                'Price',
                self.getPrice(response.css('div.finalPrice::text').get(),
                              response.css('div.finalPrice sup::text').get()))
            productItemloader.add_value(
                'OldPrice',
                self.getPrice(response.css('div.markdownPrice.priceformat::text').get(),
                              response.css('div.markdownPrice.priceformat sup::text').get()))

            productItemloader.add_value(
                'ImageThumbnailUrl',
                response.urljoin(response.css('a.productImagePrimaryLink img').attrib['data-src']))

            productItemloader.add_value(
                'ImageUrls', self.convertToFullUrls(
                    response.css('div.productImageGallery #images_galery_mobile img').xpath('@src').getall(), response))

            productItemloader.add_value('LastChangeTime', datetime.utcnow())
            productItemloader.add_value('HashCode', '')
            loadItem = productItemloader.load_item()

            productAttributes = self.getProductAttributes(response)
            loadItem['ProductAttributes'] = productAttributes
            yield loadItem
            # 获取对应的照片，报错
            # if len(productAttributes) > 0:
            #     yield loadItem
            #     # for x in productAttributes:
            #     #     for v in x['Variables']:
            #             # yield scrapy.Request(url=self.variantUrl + v['DataCode'],
            #             #                      callback=self.loadPictureUrlInStorage,
            #             #                      meta={'Product': loadItem,
            #             #                            'ProductAttributeName': x['AttributeBasicInfo']['Name'],
            #             #                            'DataCode': v['DataCode']})
            # else:
            #     yield loadItem

    def loadPictureUrlInStorage(self, response):
        item = ProductAdditionalProcessData()
        item['Product'] = response.meta['Product']
        item['ProductAttributeName'] = response.meta['ProductAttributeName']
        item['DataCode'] = response.meta['DataCode']
        item['PictureUrlInStorage'] = ''
        if response.status == 200:
            textJson = json.loads(response.text)
            if len(textJson) > 0:
                item['PictureUrlInStorage'] = ';'.join(
                    list(map(lambda x: response.urljoin(x['url']), textJson[0]['primaryImages'])))
                item['Success'] = True
                return item
        item['Msg'] = response
        item['Success'] = False
        return item

    def getProductName(self, response):
        productBrandName = response.css('span.productBrandName::text').get()
        productName = response.css('span.productName::text').get()
        productRangeName = response.css('span.productRangeName::text').get()
        result = ''
        if productName is not None:
            result = productName
        if productBrandName is not None:
            result = result + ' / ' + productBrandName
        if productRangeName is not None:
            result = result + ' / ' + productRangeName
        return result

    def convertToFullUrls(self, array, reponse):
        return list(map(lambda x: reponse.urljoin(x), array))

    def getPrice(self, _int, _decimal):
        if _int is None:
            return 0
        desc = _decimal[1:-1]
        price = float(_int + "." + desc)
        return price

    def getCurrency(self, value):
        currency = "Unknow"
        if value and value[0] == "€":
            currency = "EUR"
        return currency

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
        list = response.css('#variantColorSelector select>option')
        result = []
        for item in list:
            attributeVariable = VariableClass()
            variableClassItemLoader = VariableClassItemLoader(item=attributeVariable, response=response)
            variableClassItemLoader.add_value('DataCode', item.css('::attr("data-code")').get())
            variableClassItemLoader.add_value('NewPrice', item.css('::attr("data-igc-markdown-price")').get())
            variableClassItemLoader.add_value('OldPrice', item.css('::attr("data-price")').get())

            variableClassItemLoader.add_value('Name', item.css('::text').get())
            variableClassItemLoader.add_value('ColorSquaresRgb', item.css('::attr("data-color")').get())
            variableClassItemLoader.add_value('DisplayColorSquaresRgb', False)
            variableClassItemLoader.add_value('PriceAdjustment', 0)
            variableClassItemLoader.add_value('PriceAdjustmentUsePercentage', False)

            variableClassItemLoader.add_value('IsPreSelected', len(item.css('span.selected')) > 0)
            variableClassItemLoader.add_value('DisplayOrder', False)
            variableClassItemLoader.add_value('DisplayImageSquaresPicture', False)
            variableClassItemLoader.add_value('PictureUrlInStorage', '')
            loadItem = variableClassItemLoader.load_item()
            result.append(loadItem)
        return result

    def getSizeVariables(self, response):
        list = response.css('#productVariantDisplay a')
        result = []
        for item in list:
            attributeVariable = VariableClass()
            variableClassItemLoader = VariableClassItemLoader(item=attributeVariable, response=response)
            variableClassItemLoader.add_value('DataCode', item.css('::attr("data-code")').get())
            variableClassItemLoader.add_value('NewPrice', item.css('::attr("data-igc-markdown-price")').get())
            variableClassItemLoader.add_value('OldPrice', item.css('::attr("data-price")').get())

            variableClassItemLoader.add_value('Name', item.css('span::text').get())
            variableClassItemLoader.add_value('ColorSquaresRgb', '')
            variableClassItemLoader.add_value('DisplayColorSquaresRgb', False)
            variableClassItemLoader.add_value('PriceAdjustment', 0)
            variableClassItemLoader.add_value('PriceAdjustmentUsePercentage', False)

            variableClassItemLoader.add_value('IsPreSelected', len(item.css('span.selected')) > 0)
            variableClassItemLoader.add_value('DisplayOrder', False)
            variableClassItemLoader.add_value('DisplayImageSquaresPicture', False)
            variableClassItemLoader.add_value('PictureUrlInStorage', '')
            loadItem = variableClassItemLoader.load_item()
            result.append(loadItem)
        return result

    def getProductAttributes(self, response):
        result = []
        sizeLinklist = response.css('#productVariantDisplay a')
        if len(sizeLinklist) > 0:
            sizeAttri = self.getSizeAttribute(response)
            result.append(sizeAttri)

        colorlist = response.css('#variantColorSelector select>option')
        if len(colorlist) > 0:
            colorAttri = self.getColorAttribute(response)
            result.append(colorAttri)

        return result
