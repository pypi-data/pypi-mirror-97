# -!- coding: utf-8 -!-
import re, os, requests, time, random
from html.parser import HTMLParser
from random import randint
from scrapy import Selector
from copy import deepcopy
# 同文件夹模块
from .deco import 装饰器



def get_win10ua():
    year = int(time.strftime("%Y", time.localtime()))  # 2021
    '''内核'''
    chrome = lambda : f"Chrome/{int(10+69/7*(year-2013))}.0.{randint(1001, 9999)}.{randint(101, 999)}"
    qq = lambda : "Core/1.70.3741.400 QQBrowser/{a}.{b}.{c}.{d}".format(a=int(8+2/7*(year-2013)), b=randint(1, 9), c=randint(1001, 9999), d=randint(101, 999))
    # firefox = lambda : f"{float(int(34+38/7*(year-2013)))}"
    # safari = lambda : 'Version/{a}.{b}.{c} Safari/{d}.{e}.{f}'.format(a=max(5, int(5+8/5*(year-2015))), b=randint(0, 9), c=randint(0, 9), d=max(533, int(533+72/5*(year-2015))), e=randint(11, 99), f=randint(11, 99))
    '''浏览器'''
    # 火狐 = lambda : f"Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:{firefox()}) Gecko/20100101 Firefox/{firefox()}"
    谷歌 = lambda : f"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) {chrome()} Safari/537.36"
    qq浏览器 = lambda : f"Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) {chrome()} Safari/537.36 {qq()}"
    so = lambda : f"Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) {chrome()} Safari/537.36"
    '''随机获取'''
    浏览器s = (谷歌, qq浏览器, so)
    随机base = lambda : random.choice(浏览器s)()
    class get_win10ua():
        谷歌, qq浏览器, so = 浏览器s
        随机 = 随机base
    return get_win10ua



# 设计理念: 一个实例代表一只具体的爬虫
class req_base():

    网址智能协议 = 'http'  # 智能补全, 缺少的话就补全
    域名智能前缀 = []  # 智能补全, 缺少的话就补全, 可选范围: [www, m, wap, ....]
    get_win10ua = get_win10ua()
    url = None
    timeout = None
    proxies = None
    params = None
    data = None

    headers = {
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
        'Accept-Encoding': 'gzip, deflate, br',
        'Accept-Language': 'zh-CN,zh;q=0.9',
        'Cache-Control': 'max-age=0',
        'Connection': 'close',
        'Upgrade-Insecure-Requests': '1',
    }

    多线程装饰器 = 装饰器.多线程

    
    def __init__(self):
        self.update_ua()

    # ua
    def get_ua(self): return self.get_win10ua.随机()
    def delete_ua(self): self.headers.pop('User-Agent', '')
    def update_ua(self):
        ua = self.get_ua()
        if ua: self.headers['User-Agent'] = ua
        else: self.headers.pop('User-Agent', '')
    
    # cookie
    def get_cookie(self): return ''
    def delete_cookie(self): self.headers.pop('Cookie', '')
    def update_cookie(self):
        cookie = self.get_cookie()
        if cookie: self.headers['Cookie'] = cookie
        else: self.headers.pop('Cookie', '')
    
    # 代理ip
    def get_proxies(self): return {}
    def delete_proxies(self): self.proxies = {}
    def update_proxies(self): self.proxies = self.get_proxies()

    def url_get_domain(self, url, 含端口=False):
        r = re.findall('[^/]+' if 含端口 else '[^/:]+', re.sub('^https?://| ', '', url))
        return r[0] if r else ''
    
    def url_get_完整url(self, url):
        if not re.findall(f'^[a-zA-Z]+://', url):
            url = f"{self.网址智能协议}://{url}"
        前缀 = self.域名智能前缀
        if 前缀:
            for x in 前缀:
                if re.findall(f'^[a-zA-Z]+://{x}\.', url):
                    break
            else:
                url = url.replace('://', f'://{前缀[0]}.', 1)
        return url

    # 访问网址
    def get(self, url='', headers={}, params=None, timeout=None, proxies=None, **kvs):
        r = requests.get(
            url = self.url_get_完整url(url or self.url),
            headers = headers or self.headers,
            timeout = timeout or self.timeout,
            params = params or self.params,
            proxies = proxies or self.proxies
        )
        return r
    
    # 多线程请求
    代理有效时长 = 0  # 强制换代理间隔, 0表示关闭, 该参数仅对方法 多线程 有用
    def 判断是否执行成功(self, o): return True  # 该方法只对方法 多线程 有用, 返回 True 或 False
    
    
    def 多线程(self, func, datas=[], 线程数=20, 返值分组尺寸=None, 最高次数=10, 重试间隔=0, 启用代理=True, **kvs):
        ''' 解决多线程参数顾虑
        必须参数：
            func
            datas
            启用代理
        可忽略的参数：
            线程数
            反值分组尺寸
            最高次数
            重试间隔
        '''
        # **kvs将解包给func
        return self.多线程装饰器()(func=func)(
            datas=datas, 线程数=线程数, 返值分组尺寸=返值分组尺寸,
            最高次数=最高次数, 重试间隔=重试间隔,
            更新代理 = self.update_proxies if 启用代理 else False,
            代理有效时长=self.代理有效时长,
            更新ua=self.update_ua, 判断是否执行成功=self.判断是否执行成功, **kvs
        )
    
    def html_get_title(self, html):
        return Selector(text=html).xpath('//title/text()').extract()[0]

    def r_get_html(self, r):
        try: html = r.text
        except Exception as err: html = err
        codes = ('utf8', 'gbk', r.encoding)
        for x in codes:
            try: return r.content.decode(x)
            except: pass
        for x in codes:
            try:
                rc = deepcopy(r)
                rc.encoding = x
                return rc.text
            except: pass
        if type(html) is str: return html
        raise html

    def url_get_是否内页(self, url):
        r = re.findall('/.+', re.sub('^https?://| ', '', url))
        return bool(r)

    def html解密(self, html): return HTMLParser().unescape(html)

    def html转xpath(self, html): return Selector(text=html)

    def url_get_title(self, url):
        r = self.get(url=url)
        html = self.r_get_html(r=r)
        return self.html_get_title(html=html)
