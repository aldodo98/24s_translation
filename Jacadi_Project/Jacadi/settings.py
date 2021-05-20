# Scrapy settings for Jacadi project
#
# For simplicity, this file contains only settings considered important or
# commonly used. You can find more settings consulting the documentation:
#
#     https://docs.scrapy.org/en/latest/topics/settings.html
#     https://docs.scrapy.org/en/latest/topics/downloader-middleware.html
#     https://docs.scrapy.org/en/latest/topics/spider-middleware.html

BOT_NAME = 'Jacadi'

SPIDER_MODULES = ['Jacadi.spiders']
NEWSPIDER_MODULE = 'Jacadi.spiders'

DOWNLOAD_DELAY = 3

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
# REDIS_URL = 'redis://:redisHaiwaPAssw0rd@137.116.216.95:63790'
REDIS_URL = 'redis://:HaiwaPAssw0rdUat@20.56.0.56:63790'

DOWNLOADER_MIDDLEWARES = {
   'scrapy_crawlera.CrawleraMiddleware': 400
}

ITEM_PIPELINES = {
   # 'Jacadi.pipelines.JacadiPipeline': 300,
   'Jacadi.pipelines.RedisPipeline': 300
}

# Obey robots.txt rules
ROBOTSTXT_OBEY = False

# Configure maximum concurrent requests performed by Scrapy (default: 16)
CONCURRENT_REQUESTS = 1

CRAWLERA_ENABLED = True
CRAWLERA_APIKEY = '6eb0e6e9d6944b75a262c441a77f928d'