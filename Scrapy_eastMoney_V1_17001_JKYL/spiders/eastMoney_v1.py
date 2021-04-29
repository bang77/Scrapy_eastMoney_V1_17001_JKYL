import scrapy
from fake_useragent import UserAgent
import json
import time

from ..items import ScrapyEastmoneyV117001JkylItem01
from ..settings import CATEGORY, SUB_CATEGORY, SIGN ,CODES


class EastmoneyV1Spider(scrapy.Spider):
    name = 'eastMoney_v1'
    allowed_domains = ['eastmoney.com']
    ua = UserAgent()
    headers = {"User-Agent": ua.chrome}

    #####  公司概况爬取  #####

    def start_requests(self):
        for code in CODES:
            if 'SZ' in code or 'SH' in code:
                url = 'http://f10.eastmoney.com/CompanySurvey/CompanySurveyAjax?code=' + code
                meta = {}
            else:
                url = 'http://emweb.securities.eastmoney.com/PC_HKF10/CompanyProfile/PageAjax?code=' + code
                meta = {'Market': 'HK', 'code': code}
            yield scrapy.Request(url, headers=self.headers, callback=self.parse, meta=meta)

    def parse(self, response):
        con = json.loads(response.text)
        item = dict()
        item['category'] = CATEGORY
        item['sub_category'] = SUB_CATEGORY
        item['sign'] = SIGN
        item['update_time'] = time.strftime("%Y-%m-%d %H:%M:%S")
        item['cleaning_status'] = 0
        if response.meta.get("Market", None):
            # 股票代码
            item['code'] = response.meta['code'] + '.HK'
            item['securitycode'] = response.meta['code']
            # 上市市场
            item['market'] = 'HK'
            # 股票简称
            item['securityshortname'] = con['zqzl']['zqjc']
            # 上市交易所
            item['affiliated_exchange'] = con['zqzl']['jys']
            # 所属行业
            item['listed_industries'] = con['gszl']['sshy']
            # 基本资料
            item['basic_information'] = con['gszl']
            # 发行相关
            item['issue_related'] = con['zqzl']

        else:
            # 股票代码
            item['code'] = con['SecuCode']
            item['securitycode'] = con['SecurityCode']
            # 上市市场
            item['market'] = con['Market']
            # 股票简称
            item['securityshortname'] = con['SecurityShortName']
            # 上市交易所
            item['affiliated_exchange'] = con['jbzl']['ssjys']
            # 所属行业
            item['listed_industries'] = con['jbzl']['sszjhhy']
            # 基本资料
            item['basic_information'] = con['jbzl']
            # 发行相关
            item['issue_related'] = con['fxxg']
        yield ScrapyEastmoneyV117001JkylItem01(item)
