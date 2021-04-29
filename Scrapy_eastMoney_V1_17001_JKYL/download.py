# -*- coding: utf-8 -*-
import requests
import logging
from pathlib import Path
from fake_useragent import UserAgent
from scrapy.utils.project import get_project_settings
from urllib3 import encode_multipart_formdata


# from pybase.apollo_setting import get_project_settings


class FileTrans:
    ua = UserAgent()
    header = {"User-Agent": ua.chrome}
    logger = logging.getLogger(__name__)
    setting = get_project_settings()
    proxy_url = setting.get('PROXY_URL')
    uploadurl = setting.get("file_upload")  # 请求的接口地址
    # uploadurl = 'http://192.168.3.85:8500/file/upload/zhengyufei'

    @classmethod
    def send_file(self, file_name, file_content):
        """
        file_name: xxx.xx 如： 123.jpg
        """
        file = {
            "file": (file_name, file_content),  # 引号的file是接口的字段，后面的是文件的名称、文件的内容
            # "key": "value",  # 如果接口中有其他字段也可以加上
        }
        encode_data = encode_multipart_formdata(file)
        file_data = encode_data[0]
        headers_from_data = {
            "Content-Type": encode_data[1]
        }
        response = requests.post(url=self.uploadurl, headers=headers_from_data, data=file_data).json()
        if response:
            if response.get('success', False) is True:
                return response['data']['url']
            elif response.get('msg', False):
                self.logger.info('传输文件错误：%s' % str(response['msg']))
                return None
            else:
                self.logger.info('传输文件错误：%s' % str(response))
                return None
        else:
            self.logger.info('传输文件错误：无返回结果')
            return None

    def download(self, url, file_name):
        if not url:
            return None
        response = self.request_file(url)
        if response:
            file_url = self.send_file(file_name+".pdf", response.content)
            return file_url
        else:
            return None

    def request_file(self, url):
        count = 5
        while count:
            proxy = self._get_proxy()
            try:
                if proxy:
                    res = requests.get(url, headers=self.header, proxies=proxy, timeout=20)
                else:
                    res = requests.get(url, headers=self.header, timeout=20)
                if res.status_code == 200:
                    self.logger.info("下载文件：%s" % url)
                    return res
                else:
                    self.logger.info("文件下载状态异常,code：%s ,链接:%s" % (res.status_code, url))
                    return None
            except:
                count -= 1
                continue
        return None

    def _get_proxy(self):
        p = requests.get(self.proxy_url).json()
        proxy_ = p.get('proxy', None)
        if proxy_:
            proxy = {'http': 'http://%s' % proxy_, 'https': 'https://%s' % proxy_}
            return proxy
        else:
            return None
