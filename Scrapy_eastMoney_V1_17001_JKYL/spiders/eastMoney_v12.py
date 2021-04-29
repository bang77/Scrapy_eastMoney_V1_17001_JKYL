import scrapy
from fake_useragent import UserAgent
import json
import time

from ..items import ScrapyEastmoneyV117001JkylItem12
from ..settings import CATEGORY, SUB_CATEGORY, SIGN, CODES

class EastmoneyV12Spider(scrapy.Spider):
    name = 'eastMoney_v12'
    allowed_domains = ['eastmoney.com']
    ua = UserAgent()
    headers = {"User-Agent": ua.chrome}
    #####  公司财务分析-分红影响  #####

    def start_requests(self):
        for code in CODES:
            if 'SZ' in code or 'SH' in code:
                url = 'http://f10.eastmoney.com/BonusFinancing/BonusFinancingAjax?code=' + code
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


        for fhyx in con['fhyx']:
            item['announcement_date']=fhyx['ggrq']
            item['dividend_scheme'] = fhyx['fhfa']
            item['record_date'] = fhyx['gqdjr']
            item['ex_dividend_date'] = fhyx['cqcxr']
            item['payment_date'] = fhyx['pxr']
            item['programme_progress'] = fhyx['fajd']
            yield ScrapyEastmoneyV117001JkylItem12(item)

