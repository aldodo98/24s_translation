# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class ScrapytestItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    item = scrapy.Field()
    index = scrapy.Field()
    test = scrapy.Field()
    # pass


class Product(scrapy.Item):
    TaskId = scrapy.Field()
    Name = scrapy.Field()
    ShortDescription = scrapy.Field()
    FullDescription = scrapy.Field()
    Price = scrapy.Field()
    OldPrice = scrapy.Field()
    ImageThumbnailUrl = scrapy.Field()
    ImageUrls = scrapy.Field()
    ProductAttributes = scrapy.Field()
    LastChangeTime = scrapy.Field()
    HashCode = scrapy.Field()
    Success = scrapy.Field()
    Msg = scrapy.Field()
    LastChangeTime = scrapy.Field()

class ProductAttributeClass(scrapy.Item):
    AttributeBasicInfo = scrapy.Field()
    Mapping = scrapy.Field()
    Variables = scrapy.Field()


class AttributeBasicInfoClass(scrapy.Item):
    Name = scrapy.Field()
    Description = scrapy.Field()


class MappingClass(scrapy.Item):
    TextPrompt = scrapy.Field()
    IsRequired = scrapy.Field()
    AttributeControlTypeId = scrapy.Field()
    AttributeControlType = scrapy.Field()
    DisplayOrder = scrapy.Field()
    DefaultValue = scrapy.Field()
    # ConditionAllowed = scrapy.Field()
    # ConditionString = scrapy.Field()
    # ConditionModel = scrapy.Field()


class VariantDisplays(scrapy.Item):
    dataCode = scrapy.Field()
    dataNewPrice = scrapy.Field()
    dataOldPrice = scrapy.Field()

    dataCurrency = scrapy.Field()
    dataNameText = scrapy.Field()
    imagesData = scrapy.Field()


class VariableClass(scrapy.Item):
    DataCode = scrapy.Field()
    NewPrice = scrapy.Field()
    OldPrice = scrapy.Field()

    Name = scrapy.Field()
    ColorSquaresRgb = scrapy.Field()
    DisplayColorSquaresRgb = scrapy.Field()
    PriceAdjustment = scrapy.Field()
    PriceAdjustmentUsePercentage = scrapy.Field()
    IsPreSelected = scrapy.Field()
    DisplayOrder = scrapy.Field()
    DisplayImageSquaresPicture = scrapy.Field()
    PictureUrlInStorage = scrapy.Field()


class ProductAdditionalProcessData(scrapy.Item):
    Product = scrapy.Field()
    ProductAttributeName = scrapy.Field()
    DataCode = scrapy.Field()
    PictureUrlInStorage = scrapy.Field()
    Success = scrapy.Field()
    Msg = scrapy.Field()
