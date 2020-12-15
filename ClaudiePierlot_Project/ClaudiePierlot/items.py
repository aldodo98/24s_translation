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
    ProjectName = scrapy.Field()


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
    RootId = scrapy.Field()
    ProjectName = scrapy.Field()

class TreeLevel(scrapy.Item):
    Id = scrapy.Field()
    Level = scrapy.Field()
    Name = scrapy.Field()
    Names = scrapy.Field()
    DomId = scrapy.Field()
    DomParentId = scrapy.Field()
    Urls = scrapy.Field()

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

class ProductAttributeClass(scrapy.Item):
    AttributeBasicInfo = scrapy.Field()
    Mapping = scrapy.Field()
    Variables = scrapy.Field()

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
