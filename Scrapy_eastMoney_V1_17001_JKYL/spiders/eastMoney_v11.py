from pprint import pprint

import scrapy
from fake_useragent import UserAgent
import json
import re
import time
from ..download import FileTrans
from ..items import ScrapyEastmoneyV117001JkylItem11

from ..settings import CATEGORY, SUB_CATEGORY, SIGN, CODES


class EastmoneyV11Spider(scrapy.Spider):
    name = 'eastMoney_v11'
    allowed_domains = ['eastmoney.com']
    ua = UserAgent()
    headers = {"User-Agent": ua.chrome}
    ft = FileTrans()

    #####  公司财务分析-财务研报  #####

    def start_requests(self):
        for code in CODES:
            if 'SZ' in code or 'SH' in code:
                parms = [
                    "sr=-1",
                    "page_size=100",
                    "page_index=1",
                    "ann_type=A",
                    "client_source=web",
                    "stock_list=%s"% code.replace('SZ', '').replace('SH', ''),
                    "f_node=1",
                    "s_node=0",
                ]
                url = 'http://np-anotice-stock.eastmoney.com/api/security/ann?' + '&'.join(parms)
                meta = {'code': code, 'page': 1}
                yield scrapy.Request(url, headers=self.headers, callback=self.parse, meta=meta)
            else:
                parms = [
                    "code=" + code,
                    "pageno=1"
                ]
                url = 'http://emweb.securities.eastmoney.com/PC_HKF10/CompanyNews/GetRecordByPageNo?' + "&".join(parms)
                meta = {'Market': 'HK', 'code': code, 'page': 1}
                yield scrapy.Request(url, headers=self.headers, callback=self.hk_parse, meta=meta)
            break
    def parse(self, response):
        # pprint(json.loads(response.text))
        con = json.loads(response.text)
        if con['data']:
            item = dict()
            item['sign'] = SIGN
            item['update_time'] = time.strftime("%Y-%m-%d %H:%M:%S")
            item['cleaning_status'] = 0
            # 深沪上市公司
            if 'SZ' in response.meta['code']:
                item['code'] = response.meta['code'].replace('SZ', '') + '.SZ'
            else:
                item['code'] = response.meta['code'].replace('SH', '') + '.SH'
            for i in con['data']['list']:
                item['report_name'] = i['title']
                item['date'] = time.strftime('%Y-%m-%d', time.strptime(i['notice_date'], '%Y-%m-%d %H:%M:%S'))
                item['source'] = '东方财富网'

                item['original_url'] = 'https://pdf.dfcfw.com/pdf/H2_%s_1.pdf' % i['art_code']
                if self.mongo.find_one({'original_url': item['original_url']}):
                    self.logger.info('******%s 文件重复 ******' % item['report_name'])
                    continue
                new_url = self.ft.download(item['original_url'], item['report_name'])
                if new_url:
                    item['report_url'] = new_url
                    yield ScrapyEastmoneyV117001JkylItem11(item)
                report_url = 'http://data.eastmoney.com/notices/detail/%s/%s.html' % (response.meta['code'].replace('SZ', '').replace('SH', ''), i['art_code'])
                yield scrapy.Request(report_url, headers=self.headers, callback=self.detail_parse, meta={'item': item})
            page_size = con['data']['page_size']
            total_hits = con['data']['total_hits']
            next_page_1 = int(total_hits/page_size)
            total_page = next_page_1+1 if total_hits%page_size else next_page_1
            yield from self.next_page(response, int(total_page))

    def hk_parse(self, response):
        con = json.loads(response.text)
        if con['gsgg']['data']:
            allpage = con['gsgg']['data']['pageTotal']
            data = con['gsgg']['data']['items']

            item = dict()
            item['sign'] = SIGN
            item['update_time'] = time.strftime("%Y-%m-%d %H:%M:%S")
            item['cleaning_status'] = 0
            item['source'] = '东方财富网'
            item['code'] = response.meta['code'] + ".HK"
            for i in data:
                item['report_name'] = i['title']
                item['date'] = time.strftime('%Y-%m-%d', time.localtime(i['publishDate']/1000))
                item['original_url'] = 'https://pdf.dfcfw.com/pdf/H2_%s_1.pdf' % i['infoCode']
                if self.mongo.find_one({'original_url': item['original_url']}):
                    self.logger.info('******%s 文件重复 ******' % item['report_name'])
                    continue
                new_url = self.ft.download(item['original_url'], item['report_name'])
                if new_url:
                    item['report_url'] = new_url
                    yield ScrapyEastmoneyV117001JkylItem11(item)
                # report_url = 'http://data.eastmoney.com/notices/detail/%s/%s.html' % (response.meta['code'], i['infoCode'])
                # yield scrapy.Request(report_url, headers=self.headers, callback=self.detail_parse, meta={'item': item})
            yield from self.next_page(response, int(allpage))

    def detail_parse(self, response):
        item = response.meta['item']
        file_url = response.xpath('//a[@class="pdf-link"]/@href').get()
        if file_url:
            new_url = self.ft.download(response.urljoin(file_url), item['report_name'])
            if new_url:
                item['report_url'] = new_url
                yield ScrapyEastmoneyV117001JkylItem11(item)
        else:
            self.logger.info('******%s 未找到文件链接 ******' % response.url)

    def next_page(self, response, allpage):
        next_page = response.meta.get('page', 1) + 1
        if not response.meta.get('Market', None):
            url = re.sub('page_index=\d+', f'page_index={next_page}', response.url)
            meta = {'code': response.meta['code'], 'page': next_page}
            if next_page <= allpage:
                yield scrapy.Request(url, headers=self.headers, callback=self.parse, meta=meta)
        else:
            url = re.sub('pageno=\d+', f'pageno={next_page}', response.url)
            meta = {'code': response.meta['code'], 'page': next_page, 'Market': 'HK'}
            if next_page <= allpage:
                yield scrapy.Request(url, headers=self.headers, callback=self.hk_parse, meta=meta)