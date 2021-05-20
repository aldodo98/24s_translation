# Scrapy settings for Dior project
#
# For simplicity, this file contains only settings considered important or
# commonly used. You can find more settings consulting the documentation:
#
#     https://docs.scrapy.org/en/latest/topics/settings.html
#     https://docs.scrapy.org/en/latest/topics/downloader-middleware.html
#     https://docs.scrapy.org/en/latest/topics/spider-middleware.html

BOT_NAME = 'Dior'

SPIDER_MODULES = ['Dior.spiders']
NEWSPIDER_MODULE = 'Dior.spiders'

DOWNLOAD_DELAY = 0.1

MYSQL_DB_NAME = 'dbo'
MYSQL_HOST = 'localhost'
MYSQL_USER = 'root'
MYSQL_PASSWORD = 'root'
# Crawl responsibly by identifying yourself (and your website) on the user-agent
#USER_AGENT = 'Dior (+http://www.yourdomain.com)'
# Enables scheduling storing requests queue in redis.
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

ITEM_PIPELINES = {
   'Dior.pipelines.RedisPipeline': 300,
}

# Configure maximum concurrent requests performed by Scrapy (default: 16)
CONCURRENT_REQUESTS = 1

# Enable or disable downloader middlewares
# See https://docs.scrapy.org/en/latest/topics/downloader-middleware.html
DOWNLOADER_MIDDLEWARES = {
   'Dior.middlewares.DiorDownloaderMiddleware': 543,
   'scrapy_crawlera.CrawleraMiddleware': 400
}

CRAWLERA_ENABLED = True
CRAWLERA_APIKEY = '6eb0e6e9d6944b75a262c441a77f928d'

