# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter


class ScrapyEastmoneyV117001JkylPipeline:
    def __init__(self):
        import pymongo
        from scrapy.utils.project import get_project_settings
        self.config = get_project_settings()

        # self.client = pymongo.MongoClient(self.config.get('MONGODB_HOST'))
        # self.mongo_db = self.client[self.config.get('MONGODB_DBNAME')]

        # 地址
        self.host = self.config['MONGODB_HOST']
        # 端口
        self.port = self.config['MONGODB_PORT']
        # 数据库名
        self.dbname = self.config['MONGODB_DBNAME']
        # 创建数据库连接
        self.client = pymongo.MongoClient(host=self.host, port=self.port)
        # # 指定数据库
        self.db = self.client[self.dbname]

    def open_spider(self, spider):
        # 指定集合
        collection_name = self.select_mongo_collection(spider)
        # 连接集合
        self.mongo = self.db[collection_name]
        if spider.name == 'eastMoney_v11':
            spider.mongo = self.mongo

    def process_item(self, item, spider):
        item = dict(item)
        if spider.name == 'eastMoney_v1':
            res = self.mongo.find_one({'code': item['code']})
            if res:
                sub_category = res['sub_category']
                category = res['category']
                if item['category'] not in category.split(','):
                    item['category'] = category + ',' + item['category']

                    if item['sub_category'] not in sub_category.split(','):
                        item['sub_category'] = sub_category + ',' + item['sub_category']
                        self.mongo.update_one({'code': res['code']}, {'$set': item})
                        spider.logger.info('**** 更新一条 item ****')
                elif item['sub_category'] not in sub_category.split(','):
                    item['sub_category'] = sub_category + ',' + item['sub_category']
                    self.mongo.update_one({'code': res['code']}, {'$set': item})
                    spider.logger.info('**** 更新一条 item ****')
                elif res['basic_information'] != item['basic_information'] or res['issue_related'] != item[
                    'issue_related']:
                    self.mongo.update_one({'code': res['code']}, {'$set': item})
                    spider.logger.info('**** 更新一条 item ****')
            else:
                self.mongo.insert_one(item)
                spider.logger.info('**** 插入一条 item ****')
        elif spider.name == 'eastMoney_v2':
            res = self.mongo.find_one({'code': item['code']})
            if res:
                if res['managerlist'] != item['managerlist']:
                    self.mongo.update_one({'code': res['code']}, {'$set': item})
                    spider.logger.info('**** 更新一条 item ****')
            else:
                self.mongo.insert_one(item)
                spider.logger.info('**** 插入一条 item ****')
        elif spider.name == 'eastMoney_v3':
            res = self.mongo.find_one({'code': item['code']})
            if res:
                if res['capital_structure'] != item['capital_structure']:
                    self.mongo.update_one({'code': res['code']}, {'$set': item})
                    spider.logger.info('**** 更新一条 item ****')
            else:
                self.mongo.insert_one(item)
                spider.logger.info('**** 插入一条 item ****')
        elif spider.name == 'eastMoney_v4':
            res = self.mongo.find_one(
                {'code': item['code'], 'date': item['date']})
            if res:
                if res['capital_change'] != item['capital_change']:
                    self.mongo.update_one({'code': res['code'], 'date': res['date']}, {'$set': item})
                    spider.logger.info('**** 更新一条 item ****')
            else:
                self.mongo.insert_one(item)
                spider.logger.info('**** 插入一条 item ****')
        elif spider.name == 'eastMoney_v5':
            res = self.mongo.find_one(
                {'code': item['code'], 'date': item['date']})
            if res:
                if res['business_scope'] != item['business_scope'] or res['business_review'] != item[
                    'business_review'] or res['business_retrospect'] != item['business_retrospect'] \
                        or res['business_outlook'] != item['business_outlook']:
                    self.mongo.update_one({'code': res['code'], 'date': res['date']}, {'$set': item})
                    spider.logger.info('**** 更新一条 item ****')
            else:
                self.mongo.insert_one(item)
                spider.logger.info('**** 插入一条 item ****')
        elif spider.name == 'eastMoney_v6':
            res = self.mongo.find_one({'code': item['code'], 'date': item['date']})
            if res:
                if res['product'] != item['product'] or res['industry'] != item['industry'] or res['region'] != item[
                    'region']:
                    self.mongo.update_one({'code': res['code'], 'date': res['date']}, {'$set': item})
                    spider.logger.info('**** 更新一条 item ****')
            else:
                self.mongo.insert_one(item)
                spider.logger.info('**** 插入一条 item ****')
        elif spider.name == 'eastMoney_v7':
            res = self.mongo.find_one({'code': item['code'], 'date': item['date'], 'type': item['type']})
            if res:
                self.mongo.update_one({'code': res['code']}, {'$set': item})
                spider.logger.info('**** 更新一条 item ****')
            else:
                self.mongo.insert_one(item)
                spider.logger.info('**** 插入一条 item ****')
        elif spider.name == 'eastMoney_v8' or spider.name == 'eastMoney_v9' or spider.name == 'eastMoney_v10':
            res = self.mongo.find_one({'code': item['code'], 'date': item['date'], 'type': item['type']})
            if res:
                self.mongo.update_one({'code': res['code']}, {'$set': item})
                spider.logger.info('**** 更新一条 item ****')
            else:
                self.mongo.insert_one(item)
                spider.logger.info('**** 插入一条 item ****')

        elif spider.name == 'eastMoney_v11':
            res = self.mongo.find_one(
                {'code': item['code'], 'report_name': item['report_name']})
            if res:
                spider.logger.info('**** 重复一条 item ****')
            else:
                self.mongo.insert_one(item)
                spider.logger.info('**** 插入一条 item ****')
        elif spider.name == 'eastMoney_v12':
            res = self.mongo.find_one({'code': item['code'], 'announcement_date': item['announcement_date']})
            if res:
                self.mongo.update_one({'code': res['code']}, {'$set': item})
                spider.logger.info('**** 更新一条 item ****')
            else:
                self.mongo.insert_one(item)
                spider.logger.info('**** 插入一条 item ****')
        elif spider.name == 'eastMoney_v13':
            res = self.mongo.find_one(
                {'code': item['code'], 'issue_category': item['issue_category'], 'security_name': item['security_name'],
                 'announcement_date': item['announcement_date']})
            if res:
                self.mongo.update_one({'code': res['code']}, {'$set': item})
                spider.logger.info('**** 更新一条 item ****')
            else:
                self.mongo.insert_one(item)
                spider.logger.info('**** 插入一条 item ****')
        elif spider.name == 'eastMoney_v14':
            res = self.mongo.find_one(
                {'code': item['code'], 'entry_name': item['entry_name'], 'closing_date': item['closing_date']})
            if res:
                self.mongo.update_one({'code': res['code']}, {'$set': item})
                spider.logger.info('**** 更新一条 item ****')
            else:
                self.mongo.insert_one(item)
                spider.logger.info('**** 插入一条 item ****')

        # 关闭数据库
    def close_spider(self, spider):
        self.client.close()

        # 指定集合
    def select_mongo_collection(self, spider):
        # 公司概况
        if spider.name == 'eastMoney_v1':
            return self.config.get('listedcompany_information')
        elif spider.name == 'eastMoney_v2':
            return self.config.get('listedcompany_managers')
        elif spider.name == 'eastMoney_v3':
            return self.config.get('capital_structure')
        elif spider.name == 'eastMoney_v4':
            return self.config.get('capital_change')
        elif spider.name == 'eastMoney_v5':
            return self.config.get('operation_business')
        elif spider.name == 'eastMoney_v6':
            return self.config.get('main_business_structure')
        elif spider.name == 'eastMoney_v7':
            return self.config.get('balance_sheet')
        elif spider.name == 'eastMoney_v8':
            return self.config.get('income_statement')
        elif spider.name == 'eastMoney_v9':
            return self.config.get('cashflow_statement')
        elif spider.name == 'eastMoney_v10':
            return self.config.get('dupont_analysis')
        elif spider.name == 'eastMoney_v11':
            return self.config.get('financial_research_report')
        elif spider.name == 'eastMoney_v12':
            return self.config.get('dividend_impact')
        elif spider.name == 'eastMoney_v13':
            return self.config.get('source_offunds_raised')
        elif spider.name == 'eastMoney_v14':
            return self.config.get('project_progress')


