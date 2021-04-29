# Scrapy settings for Scrapy_eastMoney_V1_17001_JKYL project
#
# For simplicity, this file contains only settings considered important or
# commonly used. You can find more settings consulting the documentation:
#
#     https://docs.scrapy.org/en/latest/topics/settings.html
#     https://docs.scrapy.org/en/latest/topics/downloader-middleware.html
#     https://docs.scrapy.org/en/latest/topics/spider-middleware.html

BOT_NAME = 'Scrapy_eastMoney_V1_17001_JKYL'

SPIDER_MODULES = ['Scrapy_eastMoney_V1_17001_JKYL.spiders']
NEWSPIDER_MODULE = 'Scrapy_eastMoney_V1_17001_JKYL.spiders'


# Crawl responsibly by identifying yourself (and your website) on the user-agent
#USER_AGENT = 'Scrapy_eastMoney_V1_17001_JKYL (+http://www.yourdomain.com)'

# Obey robots.txt rules
ROBOTSTXT_OBEY = False

# Configure maximum concurrent requests performed by Scrapy (default: 16)
#CONCURRENT_REQUESTS = 32

# Configure a delay for requests for the same website (default: 0)
# See https://docs.scrapy.org/en/latest/topics/settings.html#download-delay
# See also autothrottle settings and docs
DOWNLOAD_DELAY = 2
# The download delay setting will honor only one of:
#CONCURRENT_REQUESTS_PER_DOMAIN = 16
#CONCURRENT_REQUESTS_PER_IP = 16

# Disable cookies (enabled by default)
#COOKIES_ENABLED = False

# Disable Telnet Console (enabled by default)
#TELNETCONSOLE_ENABLED = False

# Override the default request headers:
#DEFAULT_REQUEST_HEADERS = {
#   'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
#   'Accept-Language': 'en',
#}

# Enable or disable spider middlewares
# See https://docs.scrapy.org/en/latest/topics/spider-middleware.html
#SPIDER_MIDDLEWARES = {
#    'Scrapy_eastMoney_V1_17001_JKYL.middlewares.ScrapyEastmoneyV117001JkylSpiderMiddleware': 543,
#}

# Enable or disable downloader middlewares
# See https://docs.scrapy.org/en/latest/topics/downloader-middleware.html
DOWNLOADER_MIDDLEWARES = {
   # 'Scrapy_eastMoney_V1_17001_JKYL.middlewares.ScrapyEastmoneyV117001JkylDownloaderMiddleware': 543,
    'Scrapy_eastMoney_V1_17001_JKYL.middlewares.ProxyMiddleware': 543,

}

# Enable or disable extensions
# See https://docs.scrapy.org/en/latest/topics/extensions.html
#EXTENSIONS = {
#    'scrapy.extensions.telnet.TelnetConsole': None,
#}

# Configure item pipelines
# See https://docs.scrapy.org/en/latest/topics/item-pipeline.html
ITEM_PIPELINES = {
   'Scrapy_eastMoney_V1_17001_JKYL.pipelines.ScrapyEastmoneyV117001JkylPipeline': 300,
}

# Enable and configure the AutoThrottle extension (disabled by default)
# See https://docs.scrapy.org/en/latest/topics/autothrottle.html
#AUTOTHROTTLE_ENABLED = True
# The initial download delay
#AUTOTHROTTLE_START_DELAY = 5
# The maximum download delay to be set in case of high latencies
#AUTOTHROTTLE_MAX_DELAY = 60
# The average number of requests Scrapy should be sending in parallel to
# each remote server
#AUTOTHROTTLE_TARGET_CONCURRENCY = 1.0
# Enable showing throttling stats for every response received:
#AUTOTHROTTLE_DEBUG = False

# Enable and configure HTTP caching (disabled by default)
# See https://docs.scrapy.org/en/latest/topics/downloader-middleware.html#httpcache-middleware-settings
#HTTPCACHE_ENABLED = True
#HTTPCACHE_EXPIRATION_SECS = 0
#HTTPCACHE_DIR = 'httpcache'
#HTTPCACHE_IGNORE_HTTP_CODES = []
#HTTPCACHE_STORAGE = 'scrapy.extensions.httpcache.FilesystemCacheStorage'


RETRY_ENABLED = False
LOG_LEVEL = 'INFO'
APP_ID = 'YLJK,ylqx_ssqyfx,ssqyfx_db'
CLUSTER = 'default'
CONFIG_SERVER_URL = 'http://192.168.3.85:8096/'

# 本地数据库
# MONGODB_HOST="127.0.0.1"
# MONGODB_PORT=27017
# MONGODB_DBNAME="popular_industry"
# MONGODB_SHEETNAME="wbf_yyzz_ssqyfx"


CATEGORY = '医疗保健'
SUB_CATEGORY = '健康养老产业'

SIGN = '21'







# 健康养老
CODES = ['SZ000615', 'SZ002551', 'SZ300015', 'SH600129', 'SZ002233', 'SZ001979', 'SH600329', 'SH600671',
         'SZ002231', 'SZ000616', 'SH603998', 'SZ300096', 'SZ002223', 'SZ002105', 'SZ000961', 'SZ000415',
         'SZ002652', 'SZ002162', 'SZ002008', 'SZ002381', 'SH600735', 'SH601318', 'SH600716', 'SZ000919',
         'SZ002178', 'SH600238', 'SH600689', 'SH600223', 'SH600998', 'SZ300212', 'SZ300244', 'SZ300791',
         'SZ002093', 'SZ300078', 'SZ002614', 'SZ000700', 'SH600518', 'SZ002603', 'SH601003', 'SH600664',
         'SH600718', 'SZ002777', 'SZ000663', 'SH600393', 'SH600530', 'SH600679', 'SH601588', 'SH600745',
         'SZ300166', 'SH605288', 'SZ300024', 'SH600695', 'SH600239', 'SZ000931', 'SZ000722', 'SH600643',
         'SH601007', 'SZ000150', 'SZ002285', 'SZ300247', 'SH601336', 'SZ002579', 'SH600682', 'SH600704']

