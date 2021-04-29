# Define here the models for your spider middleware
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/spider-middleware.html

from scrapy import signals

# useful for handling different item types with a single interface
from itemadapter import is_item, ItemAdapter
import logging
import time
import requests
from scrapy.exceptions import IgnoreRequest
from scrapy.utils.project import get_project_settings
class ProxyMiddleware(object):

    def __init__(self):
        logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
        self.logger = logging.getLogger(__name__)
        self.setting = get_project_settings()
        self.proxy = None
        # self.ua = UserAgent()

    def get_proxy(self):
        if self.proxy is None:
            count = 0
            while True:
                p = requests.get(self.setting.get('PROXY_URL')).json()
                proxy = p.get('proxy', None)
                if proxy:
                    break
                elif count > 5:
                    # self.proxy = None
                    return None
                else:
                    time.sleep(1)
                    count += 1
            self.proxy = proxy
            return proxy
        else:
            return self.proxy

    def process_request(self, request, spider):
        '''对request对象加上proxy'''
        proxy = self.get_proxy()
        spider.logger.info("*** proxy: %s ***" % proxy)
        if proxy:
            if 'https:' in request.url:
                proxy = 'https://' + proxy
            elif 'http:' in request.url:
                proxy = 'http://' + proxy
            self.logger.info("*** Using Proxy : %s ***" % proxy)
            request.meta['proxy'] = proxy
            # request.headers.setdefault('User-Agent',self.ua.chrome)

        request.meta['download_timeout'] = 15*2  # 超时前等待的时间
        request_count = request.meta.get('retry_times', 0)
        request.dont_filter = True
        if request_count >= 3:
            spider.logger.info("放弃请求：%s" % request.url)
            raise IgnoreRequest
        # 重试超过5次便更改proxy
        # retry_times = request.meta.get('retry_times', 0)
        # if retry_times > 5:
        #     request.dont_filter = True
        #     self.proxy = None

    def process_response(self, request, response, spider):
        '''对返回的response处理'''
        # 如果返回的response状态不是200，重新生成当前request对象
        if response.status == 404:  # 状态码：404
            return response
        elif response.status != 200:  # 状态码：非200
            spider.logger.debug('*** Bad proxy: %s ***' % request.meta['proxy'])
            # 重置proxy
            self.proxy = None
            return request
        else:  # 状态码：200
            if request.meta.get('proxy', None):
                proxy = request.meta['proxy']
                self.proxy = proxy.replace('https://','').replace('http://','')
            return response

    def process_exception(self, request, exception, spider):
        if isinstance(exception, IgnoreRequest):
            return None
        spider.logger.debug(exception)
        # if isinstance(exception, RetryMiddleware.EXCEPTIONS_TO_RETRY):
        #     retry_times = request.meta.get('retry_times') + 1
        #     request.meta['retry_times'] = retry_times
        # 重置proxy
        if request.meta['proxy']:
            proxy = request.meta['proxy'].replace('https://','').replace('http://','')
            if proxy == self.proxy:
                self.proxy = None
        request_count = request.meta.get('request_count', 1)
        # 重复请求次数不能超过3次
        self.logger.info("第%s次重复请求：%s" % (request_count, request.url))
        request.meta['request_count'] = request_count + 1
        return request

class ScrapyEastmoneyV117001JkylSpiderMiddleware:
    # Not all methods need to be defined. If a method is not defined,
    # scrapy acts as if the spider middleware does not modify the
    # passed objects.

    @classmethod
    def from_crawler(cls, crawler):
        # This method is used by Scrapy to create your spiders.
        s = cls()
        crawler.signals.connect(s.spider_opened, signal=signals.spider_opened)
        return s

    def process_spider_input(self, response, spider):
        # Called for each response that goes through the spider
        # middleware and into the spider.

        # Should return None or raise an exception.
        return None

    def process_spider_output(self, response, result, spider):
        # Called with the results returned from the Spider, after
        # it has processed the response.

        # Must return an iterable of Request, or item objects.
        for i in result:
            yield i

    def process_spider_exception(self, response, exception, spider):
        # Called when a spider or process_spider_input() method
        # (from other spider middleware) raises an exception.

        # Should return either None or an iterable of Request or item objects.
        pass

    def process_start_requests(self, start_requests, spider):
        # Called with the start requests of the spider, and works
        # similarly to the process_spider_output() method, except
        # that it doesn’t have a response associated.

        # Must return only requests (not items).
        for r in start_requests:
            yield r

    def spider_opened(self, spider):
        spider.logger.info('Spider opened: %s' % spider.name)


class ScrapyEastmoneyV117001JkylDownloaderMiddleware:
    # Not all methods need to be defined. If a method is not defined,
    # scrapy acts as if the downloader middleware does not modify the
    # passed objects.

    @classmethod
    def from_crawler(cls, crawler):
        # This method is used by Scrapy to create your spiders.
        s = cls()
        crawler.signals.connect(s.spider_opened, signal=signals.spider_opened)
        return s

    def process_request(self, request, spider):
        # Called for each request that goes through the downloader
        # middleware.

        # Must either:
        # - return None: continue processing this request
        # - or return a Response object
        # - or return a Request object
        # - or raise IgnoreRequest: process_exception() methods of
        #   installed downloader middleware will be called
        return None

    def process_response(self, request, response, spider):
        # Called with the response returned from the downloader.

        # Must either;
        # - return a Response object
        # - return a Request object
        # - or raise IgnoreRequest
        return response

    def process_exception(self, request, exception, spider):
        # Called when a download handler or a process_request()
        # (from other downloader middleware) raises an exception.

        # Must either:
        # - return None: continue processing this exception
        # - return a Response object: stops process_exception() chain
        # - return a Request object: stops process_exception() chain
        pass

    def spider_opened(self, spider):
        spider.logger.info('Spider opened: %s' % spider.name)
