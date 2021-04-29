import scrapy
from fake_useragent import UserAgent
import json
import time

from ..items import ScrapyEastmoneyV117001JkylItem14
from ..settings import CATEGORY, SUB_CATEGORY, SIGN, CODES

class EastmoneyV14Spider(scrapy.Spider):
    name = 'eastMoney_v14'
    allowed_domains = ['eastmoney.com']
    ua = UserAgent()
    headers = {"User-Agent": ua.chrome}
    #####  公司财务分析-项目进度  #####

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


        for ProjectProgress in con['ProjectProgress']:
            item['entry_name'] = ProjectProgress['xmmc']
            item['closing_date'] = ProjectProgress['jzrq']
            item['planned_investment'] = ProjectProgress['jhtz']
            item['raised_funds_invested'] = ProjectProgress['ytrmjzj']
            item['construction_period'] = ProjectProgress['jsq']
            item['earning_rate'] = ProjectProgress['syl']
            item['payback_period'] = ProjectProgress['tzhsq']
            yield ScrapyEastmoneyV117001JkylItem14(item)

