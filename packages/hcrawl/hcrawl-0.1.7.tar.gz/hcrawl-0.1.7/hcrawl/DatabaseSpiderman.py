#!/usr/bin/env python 
# coding=utf-8
# @Time : 2020/7/13 0013 10:11 
# @Author : HL 
# @Site :  
# @File : DatabaseSpiderman.py 
# @Software: PyCharm
import difflib
import hashlib
import os
import re
import string
import time
import zipfile
from time import sleep

import pymysql
import requests
import xlrd
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver import Chrome, DesiredCapabilities

requests.packages.urllib3.disable_warnings()


class database():
    host_1 = '192.168.0.170'
    user_1 = 'skoda_community'
    password_1 = 'skoda_community'
    database_1 = 'skoda_community_ad'

    # host = 'localhost'
    # user = 'root'
    # password = 'root1226'
    host = '192.168.0.210'
    user = 'search_user'
    password = 'search_user'
    database = 'gmcms2_dev_statistic'
    # database = 'gmcms2_test'
    # host = 'rm-uf6te34unl5694f23.mysql.rds.aliyuncs.com'
    # user = 'contentdbuser'
    # password = '3D7RVMn3WR3n'
    # database = 'gmcms_2'
    port = 3306
    charset = 'utf8mb4'
    cursor = ''
    connet = ''
    CRAWL_TIME = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time()))
    ipidea_api = "http://tiqu.linksocket.com:81/abroad?num={}&type=2&lb=1&sb=0&flow=1&regions=china&port=1&n=1"

    def __init__(self, default_db=0, api=ipidea_api):
        # 连接数据库
        self.ded = default_db
        if default_db:
            self.connet = pymysql.connect(host=self.host_1, user=self.user_1, password=self.password_1,
                                          database=self.database_1,
                                          port=self.port, charset=self.charset)
            self.cursor = self.connet.cursor()
        else:
            self.connet = pymysql.connect(host=self.host, user=self.user, password=self.password,
                                          database=self.database,
                                          port=self.port, charset=self.charset)
            self.cursor = self.connet.cursor()
        self.header = {
            'cookie': 'CNZZDATA1598548=cnzz_eid%3D1204699512-1598319345-http%253A%252F%252Fwww.cnena.com%252F%26ntime%3D1599530632; Hm_lvt_d0e33fc3fbfc66c95d9fdcc4c93a8288=1602730848,1604557864; __cfduid=df806d3b82b36b9279f6a819fbb6c6ef01612749813; srcurl=687474703a2f2f7777772e636e656e612e636f6d2f73686f77726f6f6d2f62656e63616e64792d68746d2d6669642d362d69642d33373637382e68746d6c; __51cke__=; USR=xvay6cmy%090%091615171397%09http%3A%2F%2Fwww.cnena.com%2Fshowroom%2Fbencandy.php%3FRurl%3Dfid-6-id-37678.html; __tins__2844959=%7B%22sid%22%3A%201615171062858%2C%20%22vd%22%3A%202%2C%20%22expires%22%3A%201615173198061%7D; __51laig__=2; security_session_verify=18616d097122eef5d7e23a3f881c7d0a; security_session_mid_verify=0b0cdb554e89f2850f9bdf92eb0b761c',
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/81.0.4044.92 Safari/537.36'}
        self.api = api
        self.iplst = self.getIps(self.api)
        # # 代理服务器
        # self.proxyHost = "http-dyn.abuyun.com"
        # self.proxyPort = "9020"
        #
        # # 代理隧道验证信息
        # self.proxyUser = "H9XK0330X97147TD"
        # self.proxyPass = "3280B770F047D45B"

    # 插入
    def insertSql(self, sql):
        try:
            self.cursor.execute(sql)
            self.connet.commit()
        except Exception as e:
            print(e.args)
            if self.ded:
                self.connet = pymysql.connect(host=self.host_1, user=self.user_1, password=self.password_1,
                                              database=self.database_1,
                                              port=self.port, charset=self.charset)
                self.cursor = self.connet.cursor()
            else:
                self.connet = pymysql.connect(host=self.host, user=self.user, password=self.password,
                                              database=self.database,
                                              port=self.port, charset=self.charset)
                self.cursor = self.connet.cursor()
            try:
                self.cursor.execute(sql)
                self.connet.commit()
            except Exception as e1:
                print(e1.args)
                return False
        return True

    # 查询
    def selectBySql(self, sql):
        try:
            self.cursor.execute(sql)
            result = self.cursor.fetchall()
            return result
        except Exception as e:
            print(e.args)
            if self.ded:
                self.connet = pymysql.connect(host=self.host_1, user=self.user_1, password=self.password_1,
                                              database=self.database_1,
                                              port=self.port, charset=self.charset)
                self.cursor = self.connet.cursor()
            else:
                self.connet = pymysql.connect(host=self.host, user=self.user, password=self.password,
                                              database=self.database,
                                              port=self.port, charset=self.charset)
                self.cursor = self.connet.cursor()
            self.cursor.execute(sql)
            result = self.cursor.fetchall()
            return result

    # 验证是否存在
    def is_exist_sql(self, sql):
        try:
            self.cursor.execute(sql)
            if self.cursor.fetchone() is None:
                return False
            return True
        except Exception as e:
            print(e.args)
            if self.ded:
                self.connet = pymysql.connect(host=self.host_1, user=self.user_1, password=self.password_1,
                                              database=self.database_1,
                                              port=self.port, charset=self.charset)
                self.cursor = self.connet.cursor()
            else:
                self.connet = pymysql.connect(host=self.host, user=self.user, password=self.password,
                                              database=self.database,
                                              port=self.port, charset=self.charset)
                self.cursor = self.connet.cursor()
            self.cursor.execute(sql)
            if self.cursor.fetchone() is None:
                return False
            return True

    # 更新
    def updateTables(self, sql):
        try:
            self.cursor.execute(sql)
            self.connet.commit()
        except Exception as e:
            print(e.args)
            if self.ded:
                self.connet = pymysql.connect(host=self.host_1, user=self.user_1, password=self.password_1,
                                              database=self.database_1,
                                              port=self.port, charset=self.charset)
                self.cursor = self.connet.cursor()
            else:
                self.connet = pymysql.connect(host=self.host, user=self.user, password=self.password,
                                              database=self.database,
                                              port=self.port, charset=self.charset)
                self.cursor = self.connet.cursor()
            self.cursor.execute(sql)
            self.connet.commit()

    # 根据字典，表名生成插入sql
    def sqlByDict(self, tablename, dics, **kwargs):
        conditon = ''
        values = ''
        for k, v in dict.items(dics):
            conditon = conditon + ',' + pymysql.escape_string(str(k))
            values = values + ',"' + pymysql.escape_string(str(v)) + '"'
        for k, v in dict.items(kwargs):
            conditon = conditon + ',' + pymysql.escape_string(str(k))
            values = values + ',"{}"'.format(pymysql.escape_string(str(v)))

        sql = "INSERT INTO `{}`({}) VALUES ({})".format(tablename, conditon[1:], values[1:])
        return sql

    # 读取Excel表格
    def readExcel(self, excel_path, sheetname):
        wb = xlrd.open_workbook(excel_path)
        sheet = wb.sheet_by_name(sheetname)
        return sheet

    # 获取页面源码
    def getHtml(self, href, encoding='utf-8', header={}):
        if header:
            res = requests.get(href, headers=header, verify=False)
            while res.status_code != 200:
                print('{} ========================= {}'.format(href, res.status_code))
                sleep(1.5)
                res = requests.get(href, headers=header, verify=False)
            res.encoding = encoding
        else:
            res = requests.get(href, headers=self.header, verify=False)
            while res.status_code != 200:
                print('{} ========================= {}'.format(href, res.status_code))
                sleep(1.5)
                res = requests.get(href, headers=self.header, verify=False)
            res.encoding = encoding
        return res.text

    # 获取链接Response
    def getResp(self, href, encoding='utf-8', header={}):
        if header:
            res = requests.get(href, headers=header, verify=False)
            while res.status_code != 200:
                print('{} ========================= {}'.format(href, res.status_code))
                sleep(1.5)
                res = requests.get(href, headers=header, verify=False)
            res.encoding = encoding
        else:
            res = requests.get(href, headers=self.header, verify=False)
            while res.status_code != 200:
                print('{} ========================= {}'.format(href, res.status_code))
                sleep(1.5)
                res = requests.get(href, headers=self.header, verify=False)
            res.encoding = encoding
        return res

    # 获取链接Response
    def getRespAby(self, href, encoding='utf-8', header={}):
        proxyMeta = "http://{}".format(self.iplst[0])
        proxies = {
            "http": proxyMeta,
            "https": proxyMeta,
        }
        if header == {}:
            headers = self.header
        else:
            headers = header
        num = 0
        exct = 0
        while True:
            if num > 10:
                return ''
            try:
                res = requests.get(href, headers=headers, proxies=proxies, verify=False, timeout=(10, 5))
                if res.status_code == 404:
                    print("{}  链接错误！！！ CODE：{}".format(href, res.status_code))
                    break
                while res.status_code != 200:
                    if exct > 5:
                        break
                    sleep(1.5)
                    print("{}  请求异常！！！ CODE：{}".format(href, res.status_code))
                    exct += 1
                    res = requests.get(href, headers=headers, proxies=proxies, verify=False, timeout=(10, 5))
                break
            except requests.exceptions.ProxyError as pe:
                while True:
                    print('代理IP失效，重新获取代理IP！！！')
                    print(pe.args)
                    self.iplst = self.getIps(self.api)
                    proxyMeta = "http://{}".format(self.iplst[0])
                    proxies = {
                        "http": proxyMeta,
                        "https": proxyMeta,
                    }
                    try:
                        res = requests.get(href, headers=headers, proxies=proxies, verify=False, timeout=(10, 5))
                        if res.status_code == 404:
                            print("{}  链接错误！！！ CODE：{}".format(href, res.status_code))
                            break
                        while res.status_code != 200:
                            if exct > 5:
                                break
                            sleep(1.5)
                            print("{}  请求异常！！！ CODE：{}".format(href, res.status_code))
                            exct += 1
                            res = requests.get(href, headers=headers, proxies=proxies, verify=False, timeout=(10, 5))
                    except requests.exceptions.ProxyError as pe:
                        pass
                    except Exception as e:
                        print(e.args)
                        print('{} 请求失败！！！'.format(href))
                    break
            except Exception as e:
                print(e.args)
                print('{} 请求失败！！！'.format(href))
                num += 1
        if res.status_code == 200:
            res.encoding = encoding
            return res
        return ""

    # 获取页面源码并返回BeautifulSoup
    def getSoup(self, href, headers={}, encoding='utf-8'):
        html = self.getHtml(href, encoding=encoding, header=headers)
        return BeautifulSoup(html, 'html.parser')

    def getIps(self, url, num=1):
        href = url.format(num)
        res = requests.get(href)
        jjson = res.json()
        data = jjson['data']
        if len(data):
            data_list = []
            for d in data:
                ip = d['ip']
                port = d['port']
                data_list.append(ip + ':' + str(port))
            return data_list
        else:
            print('没有获取到隧道IP！！！')
            print(data)
            print(href)

    # 获取页面源码(加入代理) ipidea代理
    def getHtmlAby(self, href, encoding='utf-8', header={}):
        if header == {}:
            header = self.header

        #     proxyMeta = "http://%(user)s:%(pass)s@%(host)s:%(port)s" % {
        #         "host": self.proxyHost,
        #         "port": self.proxyPort,
        #         "user": self.proxyUser,
        #         "pass": self.proxyPass,
        #     }
        # print(self.iplst[0])
        # proxyMeta = "http://{}".format('113.31.114.1902:11653')
        proxyMeta = "http://{}".format(self.iplst[0])

        proxies = {
            "http": proxyMeta,
            "https": proxyMeta,
        }
        num = 1
        while True:
            if num > 10:
                return ''
            try:
                res = requests.get(href, headers=header, proxies=proxies, verify=False, timeout=(10, 5))
                while res.status_code != 200:
                    sleep(1.5)
                    print("{}  请求异常！！！ CODE：{}".format(href, res.status_code))
                    res = requests.get(href, headers=header, proxies=proxies, verify=False, timeout=(10, 5))
                break
            except requests.exceptions.ProxyError as pe:
                while True:
                    print('代理IP失效，重新获取代理IP！！！')
                    print(pe.args)
                    self.iplst = self.getIps(self.api)
                    proxyMeta = "http://{}".format(self.iplst[0])
                    proxies = {
                        "http": proxyMeta,
                        "https": proxyMeta,
                    }
                    try:
                        res = requests.get(href, headers=header, proxies=proxies, verify=False, timeout=(10, 5))
                        while res.status_code != 200:
                            sleep(1.5)
                            print("{}  请求异常！！！ CODE：{}".format(href, res.status_code))
                            res = requests.get(href, headers=header, proxies=proxies, verify=False, timeout=(10, 5))
                    except requests.exceptions.ProxyError as pe:
                        pass
                    except Exception as e:
                        print(e.args)
                        print('{} 请求失败！！！'.format(href))
                    break
            except Exception as e:
                print(e.args)
                print('{} 请求失败！！！'.format(href))
                num += 1
        res.encoding = encoding
        return res.text

    # 获取页面源码并返回BeautifulSoup(加入代理)
    def getSoupAby(self, href, encoding='utf-8', headers={}):
        html = self.getHtmlAby(href, encoding, header=headers)
        return BeautifulSoup(html, 'html.parser')

    # 获取页面源码（post请求）
    def getHtmlPost(self, href, data, header={}):
        if header == {}:
            header = self.header
        while True:
            try:
                res = requests.post(href, headers=header, data=data, verify=False)
                while res.status_code != 200:
                    sleep(1.5)
                    print("{}  请求异常！！！ CODE：{}".format(href, res.status_code))
                    res = requests.post(href, headers=header, data=data, verify=False)
                break
            except Exception as e:
                print(e.args)
                print('{} 请求失败！！！'.format(href))
        return res.text

    # 获取页面源码（post请求、加入代理）
    def getHtmlAbyPost(self, href, data, header={}):
        if header == {}:
            header = self.header
        # proxyMeta = "http://%(user)s:%(pass)s@%(host)s:%(port)s" % {
        #     "host": self.proxyHost,
        #     "port": self.proxyPort,
        #     "user": self.proxyUser,
        #     "pass": self.proxyPass,
        # }
        proxyMeta = "http://{}".format(self.iplst[0])
        proxies = {
            "http": proxyMeta,
            "https": proxyMeta,
        }
        while True:
            try:
                res = requests.post(href, headers=header, data=data, proxies=proxies, verify=False)
                while res.status_code != 200:
                    sleep(1.5)
                    print("{}  请求异常！！！ CODE：{}".format(href, res.status_code))
                    res = requests.post(href, headers=header, data=data, proxies=proxies, verify=False)
                break
            except requests.exceptions.ProxyError as pe:
                print('代理IP失效，重新获取代理IP！！！')
                print(pe.args)
                self.iplst = self.getIps(self.api)
                proxyMeta = "http://{}".format(self.iplst[0])
                proxies = {
                    "http": proxyMeta,
                    "https": proxyMeta,
                }
            except Exception as e:
                print(e.args)
                print('{} 请求失败！！！'.format(href))
        return res.text

    # 将字符串生成MD5
    def getMD5(self, str):
        m = hashlib.md5()
        m.update(str.encode("utf8"))
        return m.hexdigest()

    # 比较两字符串的相似度
    def string_similar(self, s1, s2):
        try:
            f = difflib.SequenceMatcher(None, s1, s2).quick_ratio()
        except Exception as e:
            print(e.args)
            print(s1)
            print(s2)
            f = 0
        return f

    # 上传图片到Zimg（传入图片链接，和下载图片暂存的本机路径）
    def uploadZimg(self, url, zimgUrl, path):
        if not os.path.exists(path):
            try:
                r = requests.get(url, verify=False)
                r.raise_for_status()
                # 使用with语句可以不用自己手动关闭已经打开的文件流
                with open(path, "wb") as f:  # 开始写文件，wb代表写二进制文件
                    f.write(r.content)
            except Exception as e:
                print("爬取失败:" + str(e))
                return ''
        header = {'Connection': 'Keep-Alive',
                  'Cache-Control': 'no-cache',
                  }

        files = {'files': open(path, 'rb')}
        n = 1
        while True:
            try:
                r = requests.post(zimgUrl, files=files, headers=header)
                if 'Image upload successfully' in r.text:
                    md5 = re.search('<h1>MD5:(.*?)</h1>', r.text).group(1)
                    return md5
                else:
                    print('上传失败！！！')
                    return ''
            except Exception as e:
                print('上传失败：' + str(e))
                if n > 4:
                    return ''
                n += 1
                sleep(1.5)

    # webdriver+selenium 模拟浏览器
    def getDriver(self):
        # proxy_auth_plugin_path = self.create_proxy_auth_extension(
        #     proxy_host=self.proxyHost,
        #     proxy_port=self.proxyPort,
        #     proxy_username=self.proxyUser,
        #     proxy_password=self.proxyPass)

        option = webdriver.ChromeOptions()

        # option.add_argument("--start-maximized")
        # prefs = {'profile.managed_default_content_settings.images': 2}
        # option.add_experimental_option('prefs', prefs)
        option.add_experimental_option('excludeSwitches', ['enable-automation'])
        # option.add_extension(proxy_auth_plugin_path)

        driver = webdriver.Chrome(chrome_options=option, executable_path="D:\\chromedriver.exe")
        return driver

    # webdriver+selenium 模拟手机浏览器
    def getWapDriver(self):
        proxy_auth_plugin_path = self.create_proxy_auth_extension(
            proxy_host=self.proxyHost,
            proxy_port=self.proxyPort,
            proxy_username=self.proxyUser,
            proxy_password=self.proxyPass)

        option = webdriver.ChromeOptions()
        # wap端
        mobileEmulation = {'deviceName': 'iPhone X'}
        option.add_experimental_option('mobileEmulation', mobileEmulation)
        # 最大化
        # option.add_argument("--start-maximized")
        # 不加载图片
        prefs = {'profile.managed_default_content_settings.images': 2}
        option.add_experimental_option('prefs', prefs)
        # 防爬检测
        option.add_experimental_option('excludeSwitches', ['enable-automation'])
        option.add_extension(proxy_auth_plugin_path)

        driver = webdriver.Chrome(chrome_options=option)
        return driver

    def getPhatomjsDriver(self, headers={}):
        if headers == {}:
            headers = self.header
        # 初始化浏览器对象
        # 使用copy() 防止修改原代码定义dict
        cap = DesiredCapabilities.PHANTOMJS.copy()
        for key, value in headers.items():
            cap['phantomjs.page.customHeaders.{}'.format(
                key)] = value

        # 在初始化浏览器对象的时候可以接收一个service_args的参数，使用这个参数设置代理
        driver = webdriver.PhantomJS(desired_capabilities=cap)

        # 设置页面加载和js加载超时时间，超时立即报错，如下设置超时时间为10秒
        driver.set_page_load_timeout(25)
        driver.set_script_timeout(25)

        return driver

    def getPhatomjsProxyDriver(self, headers={}):
        if headers == {}:
            headers = self.header
        # 初始化浏览器对象
        # 使用copy() 防止修改原代码定义dict
        cap = DesiredCapabilities.PHANTOMJS.copy()
        for key, value in headers.items():
            cap['phantomjs.page.customHeaders.{}'.format(
                key)] = value
        proxy = [
            '--proxy=%s:%s' % (self.proxyHost, self.proxyPort),  # 代理服务器的域名
            '--proxy-type=http',  # 代理类型
            '--proxy-auth=%s:%s' % (self.proxyUser, self.proxyPass),  # 代理验证所需的用户名和密码
            '--ignore-ssl-errors=true',  # 忽略https错误
        ]

        # 在初始化浏览器对象的时候可以接收一个service_args的参数，使用这个参数设置代理
        driver = webdriver.PhantomJS(service_args=proxy, desired_capabilities=cap)

        # 设置页面加载和js加载超时时间，超时立即报错，如下设置超时时间为10秒
        driver.set_page_load_timeout(25)
        driver.set_script_timeout(25)

        return driver

    # 加入代理工具方法
    def create_proxy_auth_extension(self, proxy_host, proxy_port,
                                    proxy_username, proxy_password,
                                    scheme='http', plugin_path=None):
        if plugin_path is None:
            plugin_path = 'D:/{}_{}@http-dyn.abuyun.com_9020.zip'.format(proxy_username, proxy_password)

        manifest_json = """
        {
            "version": "1.0.0",
            "manifest_version": 2,
            "name": "Abuyun Proxy",
            "permissions": [
                "proxy",
                "tabs",
                "unlimitedStorage",
                "storage",
                "<all_urls>",
                "webRequest",
                "webRequestBlocking"
            ],
            "background": {
                "scripts": ["background.js"]
            },
            "minimum_chrome_version":"22.0.0"
        }
        """

        background_js = string.Template(
            """
            var config = {
                mode: "fixed_servers",
                rules: {
                    singleProxy: {
                        scheme: "${scheme}",
                        host: "${host}",
                        port: parseInt(${port})
                    },
                    bypassList: ["foobar.com"]
                }
              };

            chrome.proxy.settings.set({value: config, scope: "regular"}, function() {});

            function callbackFn(details) {
                return {
                    authCredentials: {
                        username: "${username}",
                        password: "${password}"
                    }
                };
            }

            chrome.webRequest.onAuthRequired.addListener(
                callbackFn,
                {urls: ["<all_urls>"]},
                ['blocking']
            );
            """
        ).substitute(
            host=proxy_host,
            port=proxy_port,
            username=proxy_username,
            password=proxy_password,
            scheme=scheme,
        )

        with zipfile.ZipFile(plugin_path, 'w') as zp:
            zp.writestr("manifest.json", manifest_json)
            zp.writestr("background.js", background_js)

        return plugin_path

# if __name__ == '__main__':
#     database().getIps()
