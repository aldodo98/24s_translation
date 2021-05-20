# Scrapy settings for Powersante project
#
# For simplicity, this file contains only settings considered important or
# commonly used. You can find more settings consulting the documentation:
#
#     https://docs.scrapy.org/en/latest/topics/settings.html
#     https://docs.scrapy.org/en/latest/topics/downloader-middleware.html
#     https://docs.scrapy.org/en/latest/topics/spider-middleware.html

BOT_NAME = 'Marionnaud'

SPIDER_MODULES = ['Marionnaud.spiders']
NEWSPIDER_MODULE = 'Marionnaud.spiders'

DOWNLOAD_DELAY = 1

MYSQL_DB_NAME = 'dbo'
MYSQL_HOST = 'localhost'
MYSQL_USER = 'root'
MYSQL_PASSWORD = 'root'

# Enables scheduling storing requests queue in redis.
SCHEDULER = "scrapy_redis.scheduler.Scheduler"

# Ensure all spiders share same duplicates filter through redis.
DUPEFILTER_CLASS = "scrapy_redis.dupefilter.RFPDupeFilter"

SCHEDULER_PERSIST = True
FEED_EXPORT_ENCODING = 'utf-8'

# UAT
REDIS_URL = 'redis://:HaiwaPAssw0rdUat@20.56.0.56:63790'

ITEM_PIPELINES = {
    'Marionnaud.pipelines.RedisPipeline': 300,
    # 'Marionnaud.pipelines.MarionnaudPipeline': 300
}

DOWNLOADER_MIDDLEWARES = {
   'Marionnaud.mymiddlewares.RandomUserAgentMiddleware': 500,
    'scrapy_crawlera.CrawleraMiddleware': 400
}

CRAWLERA_ENABLED = True
CRAWLERA_APIKEY = '6eb0e6e9d6944b75a262c441a77f928d'

ROBOTSTXT_OBEY = False
CONCURRENT_REQUESTS = 1

