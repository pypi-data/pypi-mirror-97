import time, re
import pandas as pd
from aip import AipNlp  # pip install baidu-aip
from math import ceil
from copy import deepcopy


class baidu_aip(AipNlp):
    app_id = ''
    app_key = ''
    secret_key = ''
    
    def __init__(self, app_id=None, app_key=None, secret_key=None):
        if app_id: self.app_id = app_id
        if app_key: self.app_key = app_key
        if secret_key: self.secret_key = secret_key
        AipNlp.__init__(self, self.app_id, self.app_key, self.secret_key)
    
    词性字典 = {'n': '普通名词', 'f': '方位名词', 's': '处所名词', 't': '时间名词', 'nr': '人名', 'ns': '地名', 'nt': '机构团体名', 'nw': '作品名', 'nz': '其他专名', 'v': '普通动词', 'vd': '动副词', 'vn': '名动词', 'a': '形容词', 'ad': '副形词', 'an': '名形词', 'd': '副词', 'm': '数量词', 'q': '量词', 'r': '代词', 'p': '介词', 'c': '连词', 'u': '助词', 'xc': '其他虚词', 'w': '标点符号', 'PER': '人名', 'LOC': '地名', 'ORG': '机构名', 'TIME': '时间'}
    
    def 数据分组(self, data, size):
        return [data[size*(i-1): size*i] for i in range(1, ceil(len(data)/size)+1)]
    
    def lexerpro(self, text):
        rs = []
        texts = self.数据分组(data=text, size=3000)
        # 根据api文档: 长度不超过65536字节. 但实际测试发现: 65536只是瞎写的一个数值, 实际数值大约在15000字节
        for text in texts:
            tr = self.lexer(text)
            if 'items' in tr:
                for x in tr['items']: rs.append(x)
                # 不采用 rs + tr['items'], 因为前者时间复杂度为 len(tr['items']), 而后者为 len(rs) + len(tr['items'])
            else:
                err = tr.get('error_msg') or '未知错误'
                print(f"[{err}]")
                if err in ('input text too long', 'Service temporarily unavailable'):
                    long = len(text) // 2
                    for x in self.lexerpro(text=text[:long]): rs.append(x)
                    for x in self.lexerpro(text=text[long:]): rs.append(x)
                else:  # ['unsupported corpus for lexer', '未知错误']
                    print(f"[{text}]")
        return rs
    
    def 词性分析(self, text):
        rs = self.lexerpro(text=text)
        rs = [(x['item'], x['ne'] or x['pos']) for x in rs]
        rs = [dict(kw=kw, 词性=self.词性字典.get(词性, 词性)) for kw, 词性 in rs]
        return pd.DataFrame(rs)
    
    上次请求 = 0
    请求间隔 = {}
    def 限制并发(func):
        name = str(func)
        name = re.findall('function (.+) at', name) or re.findall('method (.+) of', name) or [name]
        任务名称 = name[0]
        print(任务名称)
        def newfunc(self, *v, **kv):
            dt = self.上次请求 + self.请求间隔.setdefault(任务名称, 0) - time.time()
            if dt >= 0: time.sleep(dt)
            r = func(self, *deepcopy(v), **deepcopy(kv))
            self.上次请求 = time.time()
            if r.get('error_msg') == 'Open api qps request limit reached':
                print(f'请求过快, 正在自动重试, 并自动将请求间隔增大0.1秒 - {任务名称}')
                间隔 = self.请求间隔[任务名称] + 0.1
                self.请求间隔[任务名称] = 间隔 if 间隔 <= 5 else 0
                # 设置5秒的安全界限, 以防止多线程干扰, 以及同账号多地同时调用的干扰, 这些干扰将使请求间隔无限增大, 所以超出5秒自动重置为0
                return newfunc(self, *v, **kv)
            return r
        return newfunc
    
    
    newsSummary = 限制并发(func=AipNlp.newsSummary)
    def newsSummarypro(self, text, 摘要最大长度=None, 标题=None):
        rs = []
        texts = self.数据分组(data=text, size=3000)  # 根据说明文档, 最多可输入3000字
        if len(texts) > 1: print(f'文本长度过长, 已自动分割成 {len(texts)} 份')
        for text in texts:
            tr = self.newsSummary(text, 摘要最大长度)
            if 'summary' in tr: rs.append(tr['summary'])
            else:
                err = tr.get('error_msg') or '未知错误'
                print(f"[{err}]")
                if err == 'input text too long':
                    long = len(text) // 2
                    for x in self.newsSummarypro(text=text[:long], 摘要最大长度=摘要最大长度, 标题=标题): rs.append(x)
                    for x in self.newsSummarypro(text=text[long:], 摘要最大长度=摘要最大长度, 标题=标题): rs.append(x)
                else:  # ['unsupported corpus for lexer', '未知错误']
                    print(f"[{text}]")
        return rs
    
    def 新闻摘要(self, text, 摘要最大长度=None):
        if 摘要最大长度 and 摘要最大长度 < 2: 摘要最大长度 = None  # 经测试, 有效的最低值为 2
        while True:
            text = ''.join(self.newsSummarypro(text=text, 摘要最大长度=摘要最大长度))
            if (not 摘要最大长度) or (len(text) <= 摘要最大长度):
                return text
    
    simnet = 限制并发(func=AipNlp.simnet)
    def 短文本相似度(self, t1, t2):
        if t1 == t2:
            return 1.0
        r = self.simnet(t1, t2)
        return r.get('score', r)

    dnnlm = 限制并发(func=AipNlp.dnnlm)
