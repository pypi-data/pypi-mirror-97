# -!- coding: utf-8 -!-
import requests, re, json, time
from scrapy import Selector
# 同文件夹模块
from .req_base import req_base


class req_baidu_pc(req_base):

    rn = 10
    headers = {
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
        'Accept-Encoding': 'gzip, deflate, br',
        'Accept-Language': 'zh-CN,zh;q=0.9',
        'Cache-Control': 'max-age=0',
        'Connection': 'close',
        'Upgrade-Insecure-Requests': '1',
        'Host': 'www.baidu.com',
    }
    url_get_title = None

    def __init__(self):
        req_base.__init__(self)

    def 搜索(self, kw, rn=None, **kvs):
        url = f'https://www.baidu.com/s?wd={kw}&rn={rn or self.rn}&sl_lang=cn&rsv_srlang=cn&rsv_rq=cn&ct=0&tfflag=0&gpc=stf%3D'
        return self.get(url=url, **kvs)
    
    def json搜索(self, kw, rn=None, **kvs):
        url = f'https://www.baidu.com/s?ie=utf8&oe=utf8&wd={kw}&tn=json&ch=9&rn={rn or self.rn}'
        return self.get(url=url, **kvs)

    def kw_get_num(self, kw, rn=10):  # 查收录, rn 只需要10即可
        r = self.搜索(kw=kw, rn=rn)
        html = self.r_get_html(r=r)
        return self.html_get_num(html=html)
    
    # 输入html, 返回收录量
    def html_get_num(self, html):
        if re.findall('没有找到该URL。您可以直接访问.+还可.+提交网址.+给我们.+以下是网页中包含.+的结果', html, re.S):
            return 0
        
        for text in ('百度为您找到相关结果数?约(.*)个', '找到相关结果数?约(.*)个'):
            try:
                num = re.findall(text, html)
                return int(''.join(re.findall('\d', num[0])))
            except: pass
        
        try:  # 该网站共有(.+)个网页被百度收录
            num = re.findall('该网站共有(.+)个网页被百度收录', html, re.S)
            return int(''.join(re.findall('\d', num[0])))
        except: pass

        if re.findall('很?抱歉.*没有找到与.+相关的网页', html, re.S):
            return 0
        raise Exception("查收录量失败")

    # 传入html, 传出以排名为key的字典
    def html_get_results(self, html):
        rankings = {}
        tags = Selector(text=html).xpath("//div[contains(@class,'result c-container')]")
        for tag in tags:
            try:
                # 排名作为key
                rankings[int(tag.attrib['id'])] = item = {}
                x = tag.xpath(".//div[re:test(@class,'f13.+se_st_footer')]/a[@target='_blank']")[0]
                # 提取顶部链接
                domain_href = x.xpath("./@href").extract()[0]
                顶部文字 = tag.xpath(".//h3[re:test(@class,'t')]/a[@target='_blank']")[0]
                item['顶部文字'] = 顶部文字.xpath('string(.)').extract()[0]
                item['顶部链接'] = re.sub('\.{3}$', '', re.sub('\xa0$', '', domain_href))
                # 提取底部文字
                try:  # A型html模板的熊掌号
                    item['底部文字'] = x.xpath("./span[@class='nor-src-wrap']")[0].xpath('string(.)').extract()[0]
                except:
                    if x.xpath("b"):
                        item['底部文字'] = x.xpath('string(.)').extract()[0]  # 域名的文本
                    else:
                        item['底部文字'] = x.xpath("./text()").extract()[0]
            except:
                pass
        return rankings
