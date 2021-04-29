import scrapy
from fake_useragent import UserAgent
import json
import time

from ..items import ScrapyEastmoneyV117001JkylItem10
from ..settings import CATEGORY, SUB_CATEGORY, SIGN, CODES

class EastmoneyV10Spider(scrapy.Spider):
    name = 'eastMoney_v10'
    allowed_domains = ['eastmoney.com']
    ua = UserAgent()
    headers = {"User-Agent": ua.chrome}
    #####  公司财务分析-杜邦分析  #####

    def start_requests(self):
        for code in CODES:
            if 'SZ' in code or 'SH' in code:
                url = 'http://f10.eastmoney.com/NewFinanceAnalysis/DubangAnalysisAjax?code=' + code
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
        for i in con['bgq']:
            item['date'] = i['date']
            item['type'] = 0
            item['dupontanalysis'] = i
            yield ScrapyEastmoneyV117001JkylItem10(item)
        for i in con['nd']:
            item['date'] = i['date']
            item['type'] = 1
            item['dupontanalysis'] = i
            yield ScrapyEastmoneyV117001JkylItem10(item)
