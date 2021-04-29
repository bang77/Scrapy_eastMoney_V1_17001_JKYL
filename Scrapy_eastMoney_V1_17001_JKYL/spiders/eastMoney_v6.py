import scrapy
from fake_useragent import UserAgent
import json
import time

from ..items import ScrapyEastmoneyV117001JkylItem06
from ..settings import CATEGORY, SUB_CATEGORY, SIGN, CODES

class EastmoneyV6Spider(scrapy.Spider):
    name = 'eastMoney_v6'
    allowed_domains = ['eastmoney.com']
    ua = UserAgent()
    headers = {"User-Agent": ua.chrome}
    #####  公司主营构成分析  （香港上市公司没有此类）  #####

    def start_requests(self):
        for code in CODES:
            if 'SZ' in code or 'SH' in code:
                url = 'http://f10.eastmoney.com/BusinessAnalysis/BusinessAnalysisAjax?code=' + code
                meta = {'code': code}
                yield scrapy.Request(url, headers=self.headers, callback=self.parse, meta=meta)


    def parse(self, response):
        con = json.loads(response.text)
        item = dict()
        item['sign'] = SIGN
        item['update_time'] = time.strftime("%Y-%m-%d %H:%M:%S")
        item['cleaning_status'] = 0
        # 深沪上市公司
        if 'SZ' in response.meta['code']:
            item['code'] = response.meta['code'].replace('SZ', '') + '.SZ'
        else:
            item['code'] = response.meta['code'].replace('SH', '') + '.SH'
        data = con['zygcfx']
        if data:
            for i in data:
                item['date'] = i['rq']
                item['product'] = i['cp']
                item['industry'] = i['hy']
                item['region'] = i['qy']
                yield ScrapyEastmoneyV117001JkylItem06(item)
        else:
            self.logger.info('%s 无主营构成分析' % response.meta['code'])
