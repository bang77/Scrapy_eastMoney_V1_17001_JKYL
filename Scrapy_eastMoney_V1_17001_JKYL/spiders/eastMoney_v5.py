import scrapy
from fake_useragent import UserAgent
import json
import time

from ..items import ScrapyEastmoneyV117001JkylItem05
from ..settings import CATEGORY, SUB_CATEGORY, SIGN, CODES


class EastmoneyV5Spider(scrapy.Spider):
    name = 'eastMoney_v5'
    allowed_domains = ['eastmoney.com']
    ua = UserAgent()
    headers = {"User-Agent": ua.chrome}

    #####  公司主营范围与经营评述  （香港上市公司业务回顾与业务展望）#####

    def start_requests(self):
        for code in CODES:
            if 'SZ' in code or 'SH' in code:
                url = 'http://f10.eastmoney.com/BusinessAnalysis/BusinessAnalysisAjax?code=' + code
                meta = {'code': code}
            else:
                url = 'http://emweb.securities.eastmoney.com/PC_HKF10/BusinessExpectation/PageAjax?code=' + code
                meta = {'Market': 'HK', 'code': code}
            yield scrapy.Request(url, headers=self.headers, callback=self.parse, meta=meta)

    def parse(self, response):
        con = json.loads(response.text)
        item = dict()
        item['sign'] = SIGN
        item['update_time'] = time.strftime("%Y-%m-%d %H:%M:%S")
        item['cleaning_status'] = 0
        if response.meta.get('Market', None):
            item['code'] = response.meta['code'] + '.HK'
            for i, term in enumerate(con['ywhg']):
                item['business_retrospect'] = term['des']
                item['business_outlook'] = con['ywzw'][i]['des']
                item['date'] = term['date'].replace('/', '-')
                item['business_scope'] = None
                item['business_review'] = None
                yield ScrapyEastmoneyV117001JkylItem05(item)

        else:
            # 深沪上市公司
            if 'SZ' in response.meta['code']:
                item['code'] = response.meta['code'].replace('SZ', '') + '.SZ'
            else:
                item['code'] = response.meta['code'].replace('SH', '') + '.SH'
            try:
                item['business_scope'] = con['zyfw'][0]['ms']
                item['business_review'] = con['jyps'][0]['ms']
                item['date'] = con['jyps'][0]['rq']
                item['business_retrospect'] = None
                item['business_outlook'] = None
                yield ScrapyEastmoneyV117001JkylItem05(item)
            except:
                self.logger.info('%s 无主营范围与经营评述' % response.meta['code'])
