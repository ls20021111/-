
from msedge.selenium_tools import EdgeOptions
from msedge.selenium_tools import Edge
from lxml import etree
import re
import requests

class YingHua():
    def __init__(self,url,driver):
        self.url=url
        self.driver=driver

    def lxml_url(self):  #获取m3u8地址
        edge_options = EdgeOptions()
        edge_options.add_experimental_option('excludeSwitches', ['enable-logging'])

        edge_options.use_chromium = True
        edge_options.add_argument('--disable-blink-features=AutomationControlled')
        # 设置无头浏览
        edge_options.add_argument('headless')
        # 注意此处使用的是msedge.selenium_tools中的Edge而不是 selenium.webdriver中的Edge了哦
        edge_options.set_capability("ms:loggingOptions", {'driver': 'OFF', 'browser': 'OFF'})
        self.browser = Edge(executable_path=self.driver, options=edge_options)
        self.browser.get(self.url)
        respond=etree.HTML(self.browser.page_source)
        src=respond.xpath('//*[@id="yh_playfram"]/@src')
        self.name=respond.xpath('/html/body/div[2]/div[2]/a[3]/text()')
        self.browser.close()
        if src!=[]:
            inde_m3u8=str(re.findall('(https.*m3u8)',src[0])[0]).replace('%3A',':').replace('%2F','/')
            inde_m3u8_=requests.get(inde_m3u8).text
            m3u8_url=re.findall('\\n(.*?m3u8)',inde_m3u8_)[0]
            inde_m3u8=inde_m3u8.replace('index.m3u8',m3u8_url)

            return inde_m3u8
        else:
            self.browser.close()

    def xia_zai_m3u8(self):  #解析m3u8里面的地址
        m3u8_url=self.lxml_url()
        url_ts=requests.get(m3u8_url).text.replace('\n','')
        url_ts_list=re.findall(',(.*?ts)',url_ts)
        m3u8_ts_list=[]   #所有ts地址
        for i in url_ts_list:
            m3u8_ts_list.append(m3u8_url.replace('mixed.m3u8',i))
        return m3u8_ts_list

