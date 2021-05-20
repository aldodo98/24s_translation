BOT_NAME = 'Powersante'

SPIDER_MODULES = ['Powersante.spiders']
NEWSPIDER_MODULE = 'Powersante.spiders'

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

# REDIS_URL = 'redis://:redisHaiwaPAssw0rd@137.116.216.95:63790'
# UAT
REDIS_URL = 'redis://:HaiwaPAssw0rdUat@20.56.0.56:63790'

ITEM_PIPELINES = {
    'Powersante.pipelines.RedisPipeline': 300,
    # 'Powersante.pipelines.PowersantePipeline': 300
}

DOWNLOADER_MIDDLEWARES = {
    'Powersante.middlewares.PowersanteDownloaderMiddleware': 543,
    'Powersante.mymiddlewares.RandomUserAgentMiddleware': 500,
    'scrapy_crawlera.CrawleraMiddleware': 400
}

CRAWLERA_ENABLED = True
CRAWLERA_APIKEY = '6eb0e6e9d6944b75a262c441a77f928d'


# Obey robots.txt rules
ROBOTSTXT_OBEY = False

# Configure maximum concurrent requests performed by Scrapy (default: 16)
CONCURRENT_REQUESTS = 1
