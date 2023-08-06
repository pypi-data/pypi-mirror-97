# -!- coding: utf-8 -!-
import requests, re, json, time
# 同文件夹模块
from .req_base import req_base
from .req_baidu_pc import req_baidu_pc


self_req_base = req_base()  # 私有变量
class seo_baidu_pc(req_baidu_pc):

    去除www匹配排名 = True
    网站内页排名有效 = True
    psino = False
    psino有效值 = (6, 1, 2)
    无排名报错 = False  # 查询没有排名时报错
    无排名返回 = 'rn+1'  # 无排名时的返回值
    打印查询结果 = True

    results最低占比 = False
    if type(results最低占比) is int: results最低占比 = float(results最低占比)
    # 接收False或浮点数, 范围为0-1, len(results) < rn 时报错, False表示关闭此功能

    url_get_title = self_req_base.url_get_title


    def __init__(self):
        req_baidu_pc.__init__(self)

    def get(self, *vs, **kvs):
        r = req_baidu_pc.get(self, *vs, **kvs)
        if self.psino:
            psino = int(r.cookies.get('PSINO') or -1)
            if psino in self.psino有效值:
                if self.打印查询结果: print(f"psino: {psino}")
            else:
                if self.打印查询结果: print(f"psino: {psino}, 不符合要求")
                raise Exception("psino值不符合要求")
        return r

    # json查排名
    def kw_get_json排名(self, kw, domain, rn=None):
        rn = rn or self.rn
        r = self.json搜索(kw=kw, rn=rn)
        ranking = self.rjson_get_ranking(rjson=r, domain=domain)
        if not ranking:
            if self.无排名报错: raise Exception("self.无排名报错")
            elif self.无排名返回 == 'rn+1': return rn + 1
            else: return self.无排名返回
        if self.打印查询结果: print(f'{kw} - {domain} - {ranking}')
        return ranking

    # 传入 关键词 和 域名 和 熊掌号, 获取pc排名
    def kw_get_ranking(self, kw, domain=None, 熊掌号=None, rn=None, **kvs):
        rn = rn or self.rn
        if domain and domain.count('.') >= 3:
            # 分发到json
            r = self.json搜索(kw=kw, rn=rn)
            ranking = self.rjson_get_ranking(rjson=r, domain=domain)
        else:
            # 分发到普通html
            r = self.搜索(kw=kw, rn=rn)
            results = self.html_get_results(html=self.r_get_html(r=r))
            if type(self.results最低占比) is float:
                if len(results) < rn * self.results最低占比:
                    raise Exception("self.results最低占比")
            ranking = self.results_get_ranking(results=results, domain=domain, 熊掌号=熊掌号)
        if not ranking:
            if self.无排名报错: raise Exception("self.无排名报错")
            elif self.无排名返回 == 'rn+1': return rn + 1
            else: return self.无排名返回
        if self.打印查询结果: print(f'{kw} - {domain} - {熊掌号} - {ranking}')
        return ranking

    # 传入json类型的r和domain, 传出排名
    def rjson_get_ranking(self, rjson, domain):
        domain = self.url_get_domain(url=domain)
        if self.去除www匹配排名: domain = re.sub('^www\.', '', domain)
        rjson = rjson.json()["feed"]["entry"][:-1]
        result = [(x['pn'], re.sub(' |https:|http:|\.shtml|\.html', '', x['url'], 0)) for x in rjson]
        result = [(x[0], re.sub('/+', '/', '/' + x[1] + '/', 0)[1:-1]) for x in result]
        domain = re.sub('/+', '/', '/' + re.sub(' |https:|http:', '', domain, 0) + '/', 0)[1:-1]
        for i in result:
            if domain in i[1]: return int(i[0])
        return None


    #  传入 以排名为key的字典 和 domain, 传出排名
    def results_get_ranking(self, results, domain=None, 熊掌号=None):
        if domain:
            domain = self.url_get_domain(url=domain)
            if self.去除www匹配排名: domain = re.sub('^www\.', '', domain)
        for id, item in results.items():
            底部文字 = item.get('底部文字') or ''
            if domain and domain in self.url_get_domain(url=底部文字):
                if self.网站内页排名有效: return id
                elif not re.findall('/(.+)', re.sub('https?://| ', '', 底部文字)):
                    return id  # 不存在内页, 说明是首页
            if 熊掌号 and 熊掌号 in 底部文字: return id
        return None
