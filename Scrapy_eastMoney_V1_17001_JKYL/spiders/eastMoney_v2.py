import scrapy
from fake_useragent import UserAgent
import json
import time

from ..items import ScrapyEastmoneyV117001JkylItem02
from ..settings import CATEGORY, SUB_CATEGORY, SIGN, CODES
class EastmoneyV2Spider(scrapy.Spider):
    name = 'eastMoney_v2'
    allowed_domains = ['eastmoney.com']
    ua = UserAgent()
    headers = {"User-Agent": ua.chrome}
    #####  公司高管爬取  #####

    def start_requests(self):
        for code in CODES:
            if 'SZ' in code or 'SH' in code:
                url = 'http://f10.eastmoney.com/CompanyManagement/CompanyManagementAjax?code=' + code
                meta = {'code': code}
            else:
                url ='http://emweb.securities.eastmoney.com/PC_HKF10/CompanyManager/PageAjax?code=' + code
                meta = {'Market': 'HK', 'code': code}
            yield scrapy.Request(url, headers=self.headers, callback=self.parse, meta=meta)


    def parse(self, response):
        con = json.loads(response.text)
        item = dict()
        item['sign'] = SIGN
        item['update_time'] = time.strftime("%Y-%m-%d %H:%M:%S")
        item['cleaning_status'] = 0
        if response.meta.get("Market", None):
            # 香港上市公司高管人员
            item['code'] = response.meta['code'] + ".HK"
            item['managerlist'] = con
        else:
            # 深沪上市公司高管人员
            if 'SZ' in response.meta['code']:
                item['code'] = response.meta['code'].replace('SZ', '') + '.SZ'
            else:
                item['code'] = response.meta['code'].replace('SH', '') + '.SH'
            item['managerlist'] = con['RptManagerList']
        yield ScrapyEastmoneyV117001JkylItem02(item)
