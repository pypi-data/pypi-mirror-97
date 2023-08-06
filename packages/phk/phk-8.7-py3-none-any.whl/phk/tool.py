# -!- coding: utf-8 -!-
import datetime, re, time, hashlib
from math import ceil
from pathlib import Path



class tool():

    class date():
        
        def __init__(self, date): self.date = self.o_get_date(date=date)
        
        def __str__(self): return str(self.date)
        
        def __add__(self, count): return self.date + datetime.timedelta(days=int(count))
        
        o_get_date = lambda self, date: datetime.date(*map(int, re.findall('\d+', str(date))))
        
        def __sub__(self, date):
            try:
                return self.date - datetime.timedelta(days=int(str(date)))
            except:
                date = self.o_get_date(date=date)
                return 0 if self.date == date else int(str(self.date-date).split(' ')[0])

    def 数据分组(data, size):
        return [data[size*(i-1): size*i] for i in range(1, ceil(len(data)/size)+1)]
    
    def 提取任务名称(func):
        name = str(func)
        name = re.findall('function (.+) at', name) or re.findall('method (.+) of', name) or [name]
        return name[0]
    
    def 生成md5(text, short=False):
        md5 = hashlib.md5(text.encode(encoding='utf-8')).hexdigest()
        return md5[8:-8] if short else md5

    def 当前时间(): return time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
    
    def 当前日期(): return time.strftime("%Y-%m-%d", time.localtime())

    def 提取文件目录(path, 后缀=[]):
        files = [str(x) for x in Path(path).iterdir()]
        if 后缀:
            files = [x for x in files if ('.' in x) and (x.split('.')[-1] in 后缀)]
        return files
    
    def 判断中文(text, model='含中文'):
        if type(text) is not str:  # 不是字符串类型, 返回 False
            return False
        elif not text:  # 空字符串, 返回 False
            return False
        elif model == '含中文':  # 只要含有中文, 就返回 True
            for x in text:
                if u'\u4e00' <= x <= u'\u9fa5':
                    return True
            return False
        elif model == '全中文':  # 只要含有非中文, 就返回 False
            for x in text:
                if not (u'\u4e00' <= x <= u'\u9fa5'):
                    return False
            return True
    
    def 循环取值(data):
        while True:
            for x in data:
                yield x

    def 字典取值(item):
        def g(item, i, total, keys):
            if (i < total) and (type(item) is dict):
                ki = keys[i]
                for k, v in item.items():
                    if k == ki:
                        if i == total - 1: return v, True
                        else:
                            value, r = g(v, i + 1, total, keys)
                            if r: return value, True
                    value, r = g(v, i, total, keys)
                    if r: return value, True
            return None, False
        def briskget(keys, 代替值=Exception("briskget未找到key")):
            keys = re.split(' *> *', keys)
            value, r = g(item, 0, len(keys), keys)
            if r: return value
            if type(代替值) is Exception: raise 代替值
            return 代替值
        return briskget

    @classmethod
    def 配置图转字典(cls, 配置图):
        # 先按行分割, 然后每行按#分割并取第1部分, 再删除末尾的空格
        data = [re.sub(" *$", '', x.split('#')[0]) for x in 配置图.split('\n')]
        # 去除无效元素, 然后 计算单项级别 和 提取出单项值
        data = [(len(re.findall('^ *', x)[0])//4+1, re.findall('[^ ].*', x)[0]) for x in data if x.replace(' ', '')]
        # 转为字典
        data = [(a, 'value' if ':' in b else 'list', b) for a, b in data]
        item = {0:{}}
        for n, type_, text in data:
            if type_ == 'list':
                item[n-1][text] = item[n] = {}
            elif type_ == 'value':
                key, value = re.split(' *: *', text, 1)  # 冒号前后自动忽略空格
                item[n-1][key] = eval(value)
        return item[0], cls.字典取值(item[0])
