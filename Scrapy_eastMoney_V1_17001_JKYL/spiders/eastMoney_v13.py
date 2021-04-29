import scrapy
from fake_useragent import UserAgent
import json
import time

from ..items import ScrapyEastmoneyV117001JkylItem13
from ..settings import CATEGORY, SUB_CATEGORY, SIGN, CODES

class EastmoneyV13Spider(scrapy.Spider):
    name = 'eastMoney_v13'
    allowed_domains = ['eastmoney.com']
    ua = UserAgent()
    headers = {"User-Agent": ua.chrome}
    #####  公司财务分析-募集资金来源  #####

    def start_requests(self):
        for code in CODES:
            if 'SZ' in code or 'SH' in code:
                url = 'http://f10.eastmoney.com/CapitalOperation/CapitalOperationAjax?code=%s&orderBy=1&isAsc=false' % code
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



        for CapitalFrom in con['CapitalFrom']:
            item['issue_category'] = CapitalFrom['fxlb']
            item['date_of_issue'] = CapitalFrom['fxqsr']
            item['announcement_date'] = CapitalFrom['ggrq']
            item['raise_funds'] = CapitalFrom['sjmjzjje']
            item['types_of_securities'] = CapitalFrom['zqlb']
            item['security_name'] = CapitalFrom['zqmc']
            yield ScrapyEastmoneyV117001JkylItem13(item)

