# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class ProductInfo(scrapy.Item):
    ProductUrl = scrapy.Field()
    Id = scrapy.Field()
    CategoryTreeId = scrapy.Field()
    ProductName = scrapy.Field()
    Price = scrapy.Field()

    SpiderScriptPath = scrapy.Field()
    Seconds = scrapy.Field()
    Enabled = scrapy.Field()

    LastStartUtc = scrapy.Field()
    LastEndUtc = scrapy.Field()
    LastSuccessUtc = scrapy.Field()
    Status = scrapy.Field()
    ProductId = scrapy.Field()


class CategoryTree(scrapy.Item):
    Id = scrapy.Field()
    ManufacturerId = scrapy.Field()
    CategoryId = scrapy.Field()

    CategoryLevel1 = scrapy.Field()
    CategoryLevel2 = scrapy.Field()
    CategoryLevel3 = scrapy.Field()
    CategoryLevel4 = scrapy.Field()
    CategoryLevel5 = scrapy.Field()

    Level_Url = scrapy.Field()
    CreateDateTime = scrapy.Field()
    UpdateDateTime = scrapy.Field()