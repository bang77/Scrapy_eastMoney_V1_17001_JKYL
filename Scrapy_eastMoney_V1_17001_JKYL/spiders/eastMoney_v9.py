import scrapy
from fake_useragent import UserAgent
import json
import time
import re

from ..items import ScrapyEastmoneyV117001JkylItem09
from ..settings import CATEGORY, SUB_CATEGORY, SIGN, CODES


class EastmoneyV9Spider(scrapy.Spider):
    name = 'eastMoney_v9'
    allowed_domains = ['eastmoney.com']
    ua = UserAgent()
    headers = {"User-Agent": ua.chrome}

    #####  公司财务分析-现金流量表  #####

    def start_requests(self):
        for code in CODES:
            if 'SZ' in code or 'SH' in code:
                yield from self.ss_start(code)
            else:
                yield from self.hk_start(code)

    def ss_start(self, code):
        # type=0(按报告期)  type=1(按年度)  type=2(按季度)
        for i in range(0, 3):
            if i <= 1:
                parms = [
                    "companyType=4",
                    "reportDateType=%s" % i,
                    "reportType=1",
                    "endDate=",
                    "code=%s" % code
                ]
            else:
                parms = [
                    "companyType=4",
                    "reportDateType=0",
                    "reportType=%s" % i,
                    "endDate=",
                    "code=%s" % code
                ]
            meta = {'code': code, 'type': i}
            url = "http://f10.eastmoney.com/NewFinanceAnalysis/xjllbAjax?" + "&".join(parms)
            yield scrapy.Request(url, headers=self.headers, callback=self.ss_parse, meta=meta)

    def hk_start(self, code):
        # type=0(按报告期)  type=1(按年度)
        for type_ in [0, 6]:
            parms = [
                "code=%s" % code,
                "startdate=",
                "rtype=%s" % type_
            ]
            if type_ == 6:
                type_ = 2
            meta = {'code': code, 'type': type_}
            url = 'http://emweb.securities.eastmoney.com/PC_HKF10/NewFinancialAnalysis/GetXJLLB?' + "&".join(parms)
            yield scrapy.Request(url, headers=self.headers, callback=self.hk_parse, meta=meta)

    def ss_parse(self, response):
        text = response.text.replace('\\', '')
        con = json.loads(text[1:-1])
        if con:
            item = dict()
            item['sign'] = SIGN
            item['update_time'] = time.strftime("%Y-%m-%d %H:%M:%S")
            item['cleaning_status'] = 0
            # 深沪上市公司
            if 'SZ' in response.meta['code']:
                item['code'] = response.meta['code'].replace('SZ', '') + '.SZ'
            else:
                item['code'] = response.meta['code'].replace('SH', '') + '.SH'
            item['type'] = response.meta['type']
            for i, term in enumerate(con):
                item['date'] = time.strftime('%Y-%m-%d', time.strptime(term['REPORTDATE'], "%Y/%m/%d %H:%M:%S"))
                item['cashflowstatement'] = term
                yield ScrapyEastmoneyV117001JkylItem09(item)
                if i == len(con) - 1:
                    enddate = term['REPORTDATE']
                    yield from self.ss_next(enddate, response.meta['code'], response.meta['type'], response.url)

    def hk_parse(self, response):
        con = json.loads(response.text)
        if con['data']:
            fields = con['data'][0]
            item = dict()
            item['sign'] = SIGN
            item['update_time'] = time.strftime("%Y-%m-%d %H:%M:%S")
            item['cleaning_status'] = 0
            # 香港上市公司
            item['code'] = response.meta['code'] + '.HK'
            item['type'] = response.meta['type']
            for i, terms in enumerate(con['data']):
                # print(terms)
                if i == 0:
                    continue
                item['date'] = time.strftime('%Y-%m-%d', time.strptime(terms[0], "%y-%m-%d"))
                cashflowstatement = {}
                for field, term in zip(fields, terms):
                    cashflowstatement.update({field: term})
                cashflowstatement['截止日期'] = item['date']
                # print(cashflowstatement)
                item['cashflowstatement'] = cashflowstatement
                yield ScrapyEastmoneyV117001JkylItem09(item)
                if i == 1:
                    startdate = item['date']
                    # print(startdate)
                    yield from self.hk_next(startdate, response.meta['code'], response.meta['type'], response.url)

    def ss_next(self, last_date, code, type_, url):
        date = time.strptime(last_date, "%Y/%m/%d %H:%M:%S")
        date = time.strftime("%Y-%m-%d", date)
        if re.findall('endDate=\d+-\d+-\d+', url):
            url = re.sub('endDate=\d+-\d+-\d+', f'endDate={date}', url)
        else:
            url = re.sub('endDate=', f'endDate={date}', url)
        meta = {'code': code, 'type': type_}
        yield scrapy.Request(url, headers=self.headers, callback=self.ss_parse, meta=meta)

    def hk_next(self, last_date, code, type_, url):
        date = time.strptime(last_date, "%Y-%m-%d")
        date = time.strftime("%Y-%m-%d", date)
        if re.findall('startdate=\d+-\d+-\d+', url):
            url = re.sub('startdate=\d+-\d+-\d+', f'startdate={date}', url)
        else:
            url = re.sub('startdate=', f'startdate={date}', url)
        meta = {'code': code, 'type': type_}
        yield scrapy.Request(url, headers=self.headers, callback=self.hk_parse, meta=meta)
