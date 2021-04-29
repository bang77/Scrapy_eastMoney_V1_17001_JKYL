import scrapy
from fake_useragent import UserAgent
import json
import time

from ..items import ScrapyEastmoneyV117001JkylItem04
from ..settings import CATEGORY, SUB_CATEGORY, SIGN, CODES


class EastmoneyV4Spider(scrapy.Spider):
    name = 'eastMoney_v4'
    allowed_domains = ['eastmoney.com']
    ua = UserAgent()
    headers = {"User-Agent": ua.chrome}
    #####  公司股本历年变动  #####

    def start_requests(self):
        for code in CODES:
            if 'SZ' in code or 'SH' in code:
                url = 'http://f10.eastmoney.com/CapitalStockStructure/CapitalStockStructureAjax?code=' + code
                meta = {'code': code}
            else:
                url ='http://emweb.securities.eastmoney.com/PC_HKF10/CapitalStructure/PageAjax?code=' + code
                meta = {'Market': 'HK', 'code': code}
            yield scrapy.Request(url, headers=self.headers, callback=self.parse, meta=meta)


    def parse(self, response):
        con = json.loads(response.text)
        item = dict()
        item['sign'] = SIGN
        item['update_time'] = time.strftime("%Y-%m-%d %H:%M:%S")
        item['cleaning_status'] = 0
        if response.meta.get("Market", None):
            # 香港上市公司
            item['code'] = response.meta['code'] + ".HK"
            try:
                data = con['lsgbbh']
                if data:
                    for i in data:
                        item['capital_change'] = i
                        item['date'] = time.strftime('%Y-%m-%d', time.strptime(i['ggrq'], '%Y-%m-%d %H:%M:%S'))
                        yield ScrapyEastmoneyV117001JkylItem04(item)
            except:
                self.logger.info(con)
        else:
            data = con['ShareChangeList']
            # 深沪上市公司
            if 'SZ' in response.meta['code']:
                item['code'] = response.meta['code'].replace('SZ', '') + '.SZ'
            else:
                item['code'] = response.meta['code'].replace('SH', '') + '.SH'
            length = len(data)
            if length > 0:
                sublen = len(data[0]['changeList'])
                for i in range(sublen):
                    da = {}
                    for j in range(length):
                        des = data[j]['des']
                        if '单位' in des:
                            item['date'] = data[j]['changeList'][i]
                            da['unit'] = des.replace('单位:', '')
                            da['sj'] = data[j]['changeList'][i]
                        elif des == '总股本':
                            da['zgb'] = data[j]['changeList'][i].replace(',', '')
                        elif des == '流通受限股份':
                            da['ltsxgf'] = data[j]['changeList'][i].replace(',', '')
                        elif des == '国有法人持股(受限)':
                            da['gyfrcgsx'] = data[j]['changeList'][i].replace(',', '')
                        elif des == "其他内资持股(受限)":
                            da['qtnzcgsx'] = data[j]['changeList'][i].replace(',', '')
                        elif des == "境内自然人持股(受限)":
                            da['jnzrrcgsx'] = data[j]['changeList'][i].replace(',', '')
                        elif des == "已流通股份":
                            da['yltgf'] = data[j]['changeList'][i].replace(',', '')
                        elif des == "已上市流通A股":
                            da['yssltag'] = data[j]['changeList'][i].replace(',', '')
                        elif des == "变动原因":
                            da['bdyy'] = data[j]['changeList'][i].replace(',', '')
                    item['capital_change'] = da
                    yield ScrapyEastmoneyV117001JkylItem04(item)
