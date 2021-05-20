# Scrapy settings for Celine project
#
# For simplicity, this file contains only settings considered important or
# commonly used. You can find more settings consulting the documentation:
#
#     https://docs.scrapy.org/en/latest/topics/settings.html
#     https://docs.scrapy.org/en/latest/topics/downloader-middleware.html
#     https://docs.scrapy.org/en/latest/topics/spider-middleware.html

BOT_NAME = 'ClaudiePierlot'

SPIDER_MODULES = ['ClaudiePierlot.spiders']
NEWSPIDER_MODULE = 'ClaudiePierlot.spiders'

DOWNLOAD_DELAY = 1

MYSQL_DB_NAME = 'dbo'
MYSQL_HOST = 'localhost'
MYSQL_USER = 'root'
MYSQL_PASSWORD = 'root'

ITEM_PIPELINES = {
   'ClaudiePierlot.pipelines.RedisPipeline': 300,
}

DOWNLOADER_MIDDLEWARES = {
   'scrapy_crawlera.CrawleraMiddleware': 400
}

CRAWLERA_ENABLED = True
CRAWLERA_APIKEY = '6eb0e6e9d6944b75a262c441a77f928d'

# Obey robots.txt rules
ROBOTSTXT_OBEY = False
SCHEDULER = "scrapy_redis.scheduler.Scheduler"

# Ensure all spiders share same duplicates filter through redis.
DUPEFILTER_CLASS = "scrapy_redis.dupefilter.RFPDupeFilter"

SCHEDULER_PERSIST = True
FEED_EXPORT_ENCODING = 'utf-8'
# DEV
# REDIS_URL = 'redis://:redisHaiwaPAssw0rd@137.116.216.95:63790'
# UAT
REDIS_URL = 'redis://:HaiwaPAssw0rdUat@20.56.0.56:63790'
# Obey robots.txt rules
ROBOTSTXT_OBEY = True

CONCURRENT_REQUESTS = 1
