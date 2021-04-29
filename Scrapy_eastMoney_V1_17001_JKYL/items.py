# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class ScrapyEastmoneyV117001JkylItem01(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    category = scrapy.Field()
    sub_category = scrapy.Field()
    sign = scrapy.Field()
    update_time = scrapy.Field()
    cleaning_status = scrapy.Field()
    # 股票代码
    code = scrapy.Field()
    securitycode = scrapy.Field()
    secucode = scrapy.Field()
    # 上市市场
    market = scrapy.Field()
    # 股票简称
    securityshortname = scrapy.Field()
    # 上市交易所
    affiliated_exchange = scrapy.Field()
    # 所属行业
    listed_industries = scrapy.Field()
    # 基本资料
    basic_information = scrapy.Field()
    # 发行相关
    issue_related = scrapy.Field()


class ScrapyEastmoneyV117001JkylItem02(scrapy.Item):
    sign = scrapy.Field()
    update_time = scrapy.Field()
    cleaning_status = scrapy.Field()
    # 股票代码
    code = scrapy.Field()
    managerlist = scrapy.Field()


class ScrapyEastmoneyV117001JkylItem03(scrapy.Item):
    sign = scrapy.Field()
    update_time = scrapy.Field()
    cleaning_status = scrapy.Field()
    # 股票代码
    code = scrapy.Field()
    capital_structure = scrapy.Field()


class ScrapyEastmoneyV117001JkylItem04(scrapy.Item):
    sign = scrapy.Field()
    update_time = scrapy.Field()
    cleaning_status = scrapy.Field()
    # 股票代码
    code = scrapy.Field()
    capital_change = scrapy.Field()
    date = scrapy.Field()


class ScrapyEastmoneyV117001JkylItem05(scrapy.Item):
    sign = scrapy.Field()
    update_time = scrapy.Field()
    cleaning_status = scrapy.Field()
    # 股票代码
    code = scrapy.Field()
    business_scope = scrapy.Field()
    business_review = scrapy.Field()
    business_retrospect = scrapy.Field()
    business_outlook = scrapy.Field()
    date = scrapy.Field()


class ScrapyEastmoneyV117001JkylItem06(scrapy.Item):
    sign = scrapy.Field()
    update_time = scrapy.Field()
    cleaning_status = scrapy.Field()
    # 股票代码
    code = scrapy.Field()
    date = scrapy.Field()
    product = scrapy.Field()
    industry = scrapy.Field()
    region = scrapy.Field()


class ScrapyEastmoneyV117001JkylItem07(scrapy.Item):
    sign = scrapy.Field()
    update_time = scrapy.Field()
    cleaning_status = scrapy.Field()
    # 股票代码
    code = scrapy.Field()
    type = scrapy.Field()
    date = scrapy.Field()
    balance = scrapy.Field()


class ScrapyEastmoneyV117001JkylItem08(scrapy.Item):
    sign = scrapy.Field()
    update_time = scrapy.Field()
    cleaning_status = scrapy.Field()
    # 股票代码
    code = scrapy.Field()
    type = scrapy.Field()
    date = scrapy.Field()
    incomestatement = scrapy.Field()


class ScrapyEastmoneyV117001JkylItem09(scrapy.Item):
    sign = scrapy.Field()
    update_time = scrapy.Field()
    cleaning_status = scrapy.Field()
    # 股票代码
    code = scrapy.Field()
    type = scrapy.Field()
    date = scrapy.Field()
    cashflowstatement = scrapy.Field()


class ScrapyEastmoneyV117001JkylItem10(scrapy.Item):
    sign = scrapy.Field()
    update_time = scrapy.Field()
    cleaning_status = scrapy.Field()
    # 股票代码
    code = scrapy.Field()
    type = scrapy.Field()
    date = scrapy.Field()
    dupontanalysis = scrapy.Field()


class ScrapyEastmoneyV117001JkylItem11(scrapy.Item):
    sign = scrapy.Field()
    update_time = scrapy.Field()
    cleaning_status = scrapy.Field()
    # 股票代码
    code = scrapy.Field()
    report_name = scrapy.Field()
    date = scrapy.Field()
    report_url = scrapy.Field()
    source = scrapy.Field()
    original_url = scrapy.Field()


class ScrapyEastmoneyV117001JkylItem12(scrapy.Item):
    sign = scrapy.Field()
    update_time = scrapy.Field()
    cleaning_status = scrapy.Field()
    # 股票代码
    code = scrapy.Field()
    announcement_date = scrapy.Field()
    dividend_scheme = scrapy.Field()
    record_date = scrapy.Field()
    ex_dividend_date = scrapy.Field()
    payment_date = scrapy.Field()
    programme_progress = scrapy.Field()


class ScrapyEastmoneyV117001JkylItem13(scrapy.Item):
    sign = scrapy.Field()
    update_time = scrapy.Field()
    cleaning_status = scrapy.Field()
    # 股票代码
    code = scrapy.Field()

    issue_category = scrapy.Field()
    date_of_issue = scrapy.Field()
    announcement_date = scrapy.Field()
    raise_funds = scrapy.Field()
    types_of_securities = scrapy.Field()
    security_name = scrapy.Field()


class ScrapyEastmoneyV117001JkylItem14(scrapy.Item):
    sign = scrapy.Field()
    update_time = scrapy.Field()
    cleaning_status = scrapy.Field()
    # 股票代码
    code = scrapy.Field()

    planned_investment = scrapy.Field()
    construction_period = scrapy.Field()
    closing_date = scrapy.Field()
    earning_rate = scrapy.Field()
    payback_period = scrapy.Field()
    entry_name = scrapy.Field()
    raised_funds_invested = scrapy.Field()