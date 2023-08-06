# 第三方库
import time, json, pymysql, traceback
import pandas as pd
import numpy as np
from math import ceil
from copy import deepcopy
# 自发布的pip库
from .pmysql import pmysql



class 过滤器():

    def __init__(self, name=None, 条件=None, orm=None, 查询字段='*'):
        self.name = name
        self.条件 = 条件
        self.orm = orm
        self.查询字段 = 查询字段

    def copy(self, 条件, 查询字段=None):
        return 过滤器(name=self.name, 条件=条件, orm=self.orm, 查询字段=查询字段 or self.查询字段)

    def __eq__(self, o):  # ==
        if o is None:
            return self.copy(f"{self.name} is null")
        return self.copy(f"{self.name} = {json.dumps(o, ensure_ascii=False)}")

    def __ne__(self, o):  # !=
        if o is None:
            return self.copy(f"{self.name} is not null")
        return self.copy(f"{self.name} != {json.dumps(o, ensure_ascii=False)}")

    def __lt__(self, o):  # <
        return self.copy(f"{self.name} < {json.dumps(o, ensure_ascii=False)}")

    def __le__(self, o):  # <=
        return self.copy(f"{self.name} <= {json.dumps(o, ensure_ascii=False)}")

    def __gt__(self, o):  # >
        return self.copy(f"{self.name} > {json.dumps(o, ensure_ascii=False)}")

    def __ge__(self, o):  # >=
        return self.copy(f"{self.name} >= {json.dumps(o, ensure_ascii=False)}")

    def __and__(self, o):  # &
        if self.条件: return self.copy(f"({self.条件}) and ({o.条件})")
        return o

    def __or__(self, o):  # |
        if self.条件: return self.copy(f"({self.条件}) or ({o.条件})")
        return o

    def __invert__(self):  # ~
        if self.条件: return self.copy(f"not ({self.条件})")
        return self

    def re_m(self, o=''):
        if o: return self.copy(f"{self.name} regexp {json.dumps(o, ensure_ascii=False)}")
        raise Exception("正则内容不能为空")
    
    def __getitem__(self, key):
        type_ = type(key)
        if type_ is slice:
            start, stop, step = key.start or 0, key.stop or 0, key.step
            if (start < 0) or (stop < 0): raise Exception("不支持负数切片")
            elif start and stop: limit = f" limit {start}, {stop - start}"
            elif start: limit = f" limit {start}, 9999999999999999"
            elif stop: limit = f" limit 0, {stop}"
            else: limit = ""
            sql = f"select {self.查询字段}" + " from {数据表}" + (f" where {self.条件}" if self.条件 else '') + limit
            return self.orm.sql(sql)
        elif type_ is int:  # [3]
            if key < 0: raise Exception("不支持负数切片")
            sql = f"select {self.查询字段}" + " from {数据表}" + (f" where {self.条件}" if self.条件 else '') + f" limit {key}, 1"
            r = self.orm.sql(sql)
            return r[0]
        elif type_ is str:  # 查询单个字段
            return self.copy(self.条件, key)
        elif type_ is dict:  # 字段重命名
            查询字段 = ','.join(f"{k} as {v}" for k, v in key.items())
            return self.copy(self.条件, 查询字段)
        elif type_ is tuple:  # 部分字段重命名
            查询字段 = []
            for x in key:
                if type(x) is str: 查询字段.append(x)
                else:
                    for k, v in x.items(): 查询字段.append(f"{k} as {v}")
            查询字段 = ','.join(查询字段)
            return self.copy(self.条件, 查询字段)
        elif self.条件:  # [过滤器]
            return self.copy(f"({self.条件}) and ({key.条件})")
        return key  # [过滤器]

    def __setitem__(self, key, value):
        type_ = type(key)
        if type_ is slice:
            raise Exception("不支持切片修改, 仅支持条件修改")
        elif type_ is int:  # [3]
            raise Exception("不支持切片修改, 仅支持条件修改")
        zds = self.orm.s__zds if (self.查询字段 == '*') else self.查询字段.split(',')
        if type_ is str:
            zds = [key]
            条件 = f" where {self.条件}" if self.条件 else ''
        elif type_ is tuple:
            zds = list(key)
            条件 = f" where {self.条件}" if self.条件 else ''
        elif self.条件:
            条件 = f" where ({self.条件}) and ({key.条件})"
        else:
            条件 = f" where {key.条件}"
        pk = self.orm.s__pk
        if (pk not in value) and (pk in zds): zds.remove(pk)
        value = {k: value.get(k) for k in zds}
        value = ','.join([f"{k}={json.dumps(v, ensure_ascii=False)}" for k, v in value.items()])
        sql = "update {数据表}" + f" set {value}" + 条件
        return self.orm.sql(sql)

    def get_sql(self):
        return self.条件

    def delete(self):
        sql = "delete from {数据表}" + f" where {self.条件}"
        return self.orm.sql(sql=sql)

    def str_in(self, o=[]):
        条件null = 条件in = None
        o = set(o)
        if None in o:
            o.remove(None)
            条件null = f"{self.name} is null"
        for x in o:
            if type(x) is not str:
                raise Exception("str_in列表只接收str或None")
        if o: 条件in = f"{self.name} in ({','.join(json.dumps(x, ensure_ascii=False) for x in o)})"
        if 条件null and 条件in:
            return self.copy(f"({条件null}) or ({条件in})")
        elif 条件null:
            return self.copy(条件null)
        elif 条件in:
            return self.copy(条件in)
        else:
            raise Exception("str_in列表不能为空")
            
    def str_not_in(self, o=[]):
        条件null = 条件in = None
        o = set(o)
        if None in o:
            o.remove(None)
            条件null = f"{self.name} is not null"
            if o:
                for x in o:
                    if type(x) is not str: raise Exception("str_not_in列表只接收str或None")
                条件in = f"{self.name} not in ({','.join(json.dumps(x, ensure_ascii=False) for x in o)})"
                return self.copy(f"({条件null}) and ({条件in})")
            return self.copy(条件null)
        elif o:
            for x in o:
                if type(x) is not str: raise Exception("str_not_in列表只接收str或None")
            条件null = f"{self.name} is null"
            条件in = f"{self.name} not in ({','.join(json.dumps(x, ensure_ascii=False) for x in o)})"
            return self.copy(f"({条件null}) or ({条件in})")
        raise Exception("str_not_in列表不能为空")

    
    def int_in(self, o=[]):
        条件null = 条件in = None
        o = set(o)
        if None in o:
            o.remove(None)
            条件null = f"{self.name} is null"
        for x in o:
            if type(x) is not int: raise Exception("int_in列表只接收int或None")
        if o: 条件in = f"{self.name} in ({','.join(json.dumps(x, ensure_ascii=False) for x in o)})"
        if 条件null and 条件in:
            return self.copy(f"({条件null}) or ({条件in})")
        elif 条件null:
            return self.copy(条件null)
        elif 条件in:
            return self.copy(条件in)
        else:
            raise Exception("int_in列表不能为空")
    
    def int_not_in(self, o=[]):
        条件null = 条件in = None
        o = set(o)
        if None in o:
            o.remove(None)
            条件null = f"{self.name} is not null"
            if o:
                for x in o:
                    if type(x) is not int: raise Exception("int_not_in列表只接收int或None")
                条件in = f"{self.name} not in ({','.join(json.dumps(x, ensure_ascii=False) for x in o)})"
                return self.copy(f"({条件null}) and ({条件in})")
            return self.copy(条件null)
        elif o:
            for x in o:
                if type(x) is not int: raise Exception("int_not_in列表只接收int或None")
            条件null = f"{self.name} is null"
            条件in = f"{self.name} not in ({','.join(json.dumps(x, ensure_ascii=False) for x in o)})"
            return self.copy(f"({条件null}) or ({条件in})")
        raise Exception("int_not_in列表不能为空")


class orm_mysql(pmysql):

    '''

<<使用教程>>


一, 连接数据库


地址 = {
    '账号': {'host': '', 'user': '', 'passwd': '', 'port': 3306},
    '数据库': '数据库名称',
    '数据表': '数据表名称',
}
orm = orm_mysql(地址=地址, mysql账号=None, 持久连接=True)
持久连接=True时, 每次增删改查的速度比 持久连接=False 快0.5秒, 但用完后需要手动调用 self.close()
持久连接=False时, 每次执行增删改查, 都会创建一个临时的mysql连接, 用完后立即自动关闭, 所以需要多0.5秒


二, 添加数据


kw = {'title':xxx, 'content':xxx}

orm.append(kw)  # 添加一条数据

orm.数据分组尺寸 = 5000  # 默认为1000, 数值越大上传越快, 但mysql本身不支持无限大的分组尺寸
orm += [kw1, kw2, kw3]  # 批量添加数据


三, 过滤器[ ]


1.通过过滤器[ ]查询

查询所有数据: orm[:]

查询 id>=10 的数据: orm[orm.id >= 10][:]

查询 id==10 的数据: orm[orm.id == 10][:]

查询 title=='t' 的数据: orm[orm.title == 't'][:]

用正则表达式查询: orm[orm.title.re_m('.*')][:]

查询id在(1,3,5)里面的数据: orm[orm.id.int_in([1,3,5])][:]

查询title在('t1','t2')里面的数据: orm[orm.title.str_in(['t1','t2'])][:]

查询id不在(1,3,5)里面的数据: orm[orm.id.int_not_in([1,3,5])][:]

查询title不在('t1','t2')里面的数据: orm[orm.title.str_not_in(['t1','t2'])][:]

并联查询:
orm[(orm.id > 5) & (orm.title.re_m('.*'))][:]  # and
orm[(orm.id > 5) | (orm.title.re_m('.*'))][:]  # or
orm[~ (orm.id > 5)]  # 将条件取反
orm[() & (~ (() | (() & ()) | ()))][:]  # 可无限嵌套

串联查询
orm[orm.id > 5][orm.title == 't'][][][]...[:]  # 可无限嵌套

并联和串联混合查询
orm[并联语句][并联语句][并联语句][并联语句]...[:]

# 只查询某几列
orm[一系列过滤器]['title'][:]  # 只查询title字段
orm[一系列过滤器]['title', 'id'][:]  # 只查询title和id字段
orm[一系列过滤器]['title', {'id':'pk'}][:]  # 只查询title和id字段, 并且把id重命名为pk

# 切片
查询全部: orm[一系列过滤器][:]
查询前100条: orm[一系列过滤器][:100]
查询第101条开始的: orm[一系列过滤器][100:]
查询第100条: orm[一系列过滤器][100]


2.通过过滤器[ ]删除数据

orm[一系列过滤器].delete()
orm[orm.id >= 10].delete()


3.通过过滤器[ ]修改数据

kw = dict(title=xx, content=xx, 相似度=xx, ....)
orm[一系列过滤器] = kw  # 对所有字段赋值
orm[一系列过滤器]['title'] = kw  # 仅对title字段赋值
orm[一系列过滤器]['title','content'] = kw  # 仅对title和content字段赋值


四, loc 和 ilic


# 按标签切片
kws = orm.loc[5:]  # 等价于 kws = orm[orm.id >= 5][:]
kws = orm.loc[:5]  # 等价于 kws = orm[orm.id <= 4][:]
kws = orm.loc[:]   # 等价于 kws = orm[:]
kw = orm.loc[5]    # 等价于 kw = orm[orm.id == 5][0]
orm.loc[5] = kw    # 等价于 orm[orm.id == 5] = kw

# 按位置切片
kws = orm.iloc[5:]  # 等价于 kws = orm[5:]
kws = orm.iloc[:5]  # 等价于 kws = orm[:5]
kws = orm.iloc[:]   # 等价于 kws = orm[:]
kw = orm.iloc[5]    # 等价于 kw = orm[5]

'''
    
    添加失败立即报错 = True
    数据分组尺寸 = 1000

    def __init__(self, 地址=None, mysql账号={}, 持久连接=True):
        self.添加失败的数据 = []
        if mysql账号: self.mysql账号 = mysql账号  # 1
        self.s__构建地址(地址)  # 2
        self.持久连接 = 持久连接  # 3
        if 持久连接: self.创建持久连接()  # 3
        self.获取字段列表()  # 4
        self.loc = self.type_loc(self)  # 5
        self.iloc = self.type_iloc(self)  # 5
        for name in self.s__zds:  # 5
            exec(f"self.{name} = 过滤器(name='{name}', orm=self)")
        else:
            self.s__过滤器 = eval(f"self.{name}")

    def s__构建地址(self, o):
        if type(o) is str:
            self.地址 = self.mysql账号[o]
        else:
            def get账号(o):
                r = {}
                for k, v in o.items():
                    if type(v) is dict:
                        r.update(get账号(v))
                    else:
                        r[k] = v
                return r
            地址 = get账号(o)
            地址['账号'] = {'host': 地址.pop('host'), 'user': 地址.pop('user'), 'passwd': 地址.pop('passwd'), 'port': 地址.pop('port')}
            self.地址 = 地址

    def __getitem__(self, key):
        return self.s__过滤器.__getitem__(key)

    def __setitem__(self, key, value):
        return self.s__过滤器.__setitem__(key, value)

    def 创建持久连接(self): self.conn, self.cursor = self.创建连接(地址=self.地址)

    def close(self): return self.conn.close()

    def sql(self, sql=None, **kw):
        数据类型 = kw.get('数据类型', 'list').lower()
        地址 = self.地址
        if self.持久连接:
            conn, cursor = self.conn, self.cursor
            conn.ping(reconnect=True)
            # 加一步判断: 断开的话, 自动重连
        else:
            conn, cursor = self.创建连接(地址=地址)
        if sql:
            sql = sql.replace('{数据表}', 地址['数据表'])
            cursor.execute(sql)
            datas = list(cursor.fetchall())
            conn.commit()
            if not self.持久连接: conn.close()
            if 数据类型 in ('pandas', 'df'): return pd.DataFrame(datas)
            return datas
        return conn, cursor, 地址['数据表']

    def append(self, kw):  # 同list: orm.append({'title': '2020-02-25'})
        return self.添加数据(datas=kw)
    
    def __iadd__(self, kws):  # 同list: orm += [{'title': '2020-02-25-0'}, {'title': '2020-02-25-1'}]
        r = self.添加数据(datas=kws)
        print(r)
        return self

    def 获取字段列表(self):
        sql = "select column_name as name,column_key as pk from information_schema.columns where table_name = '{数据表}'"
        kws = self.sql(sql=sql)
        self.s__zds = 全部字段 = []
        self.s__pzds = 普通字段 = []
        self.s__pk = ''
        实例变量 = set(self.__dict__) | {'s__过滤器', 'loc', 'iloc'}
        for x in kws:
            name = x['name']
            if name in 实例变量:
                raise Exception(f"数据表字段 '{name}' 名称与orm内置变量冲突, 无法使用orm")
            全部字段.append(name)
            if x['pk']:
                self.s__pk = name
            else:
                普通字段.append(name)

    class type_loc():
        def __init__(self, f):
            self.s__pk = f.s__pk
            self.sql = f.sql
            self.修改数据 = f.修改数据

        def __getitem__(self, key):  # 同pandas的loc orm.loc[5], orm.loc[5:], orm.loc[:5]
            if type(key) is slice:
                start, stop, step = key.start, key.stop, key.step
                if start and stop:
                    sql = "select * from {数据表}" + f" where ({self.s__pk} >= {start}) and ({self.s__pk} < {stop})"
                elif start:
                    sql = "select * from {数据表}" + f" where {self.s__pk} >= {start}"
                elif stop:
                    sql = "select * from {数据表}" + f" where {self.s__pk} < {stop}"
                else:
                    sql = "select * from {数据表}"
                return self.sql(sql=sql)
            else:
                key = json.dumps(key, ensure_ascii=False)
                sql = "select * from {数据表}" + f" where {self.s__pk} = {key}"
                r = self.sql(sql=sql)
                return r[0]
        
        def __setitem__(self, key, value):  # 同pandas的loc orm.loc[5] = dict(title='dad')
            if type(key) is slice:
                print('暂不支持切片赋值, 只支持索引赋值')
                return []
            else:
                value = deepcopy(value)
                value[self.s__pk] = key
                return self.修改数据(代号=None, datas=[value], pro_key=self.s__pk)
    
    class type_iloc():
        def __init__(self, f):
            self.s__pk = f.s__pk
            self.sql = f.sql

        def __getitem__(self, key):  # 同pandas的iloc orm.iloc[5], orm.iloc[5:], orm.iloc[:5]
            if type(key) is slice:
                start, stop, step = key.start or 0, key.stop or 0, key.step
                if (start < 0) or (stop < 0): raise Exception("不支持负数切片")
                if start and stop:
                    sql = "select * from {数据表}" + f" limit {start}, {stop-start}"
                elif start:
                    sql = "select * from {数据表}" + f" limit {start}, 9999999999999999"
                elif stop:
                    sql = "select * from {数据表}" + f" limit 0, {stop}"
                else:
                    sql = "select * from {数据表}"
                return self.sql(sql=sql)
            else:
                if key < 0: raise Exception("不支持负数切片")
                key = json.dumps(key, ensure_ascii=False)
                sql = "select * from {数据表}" + f" limit {key}, 1"
                r = self.sql(sql=sql)
                return r[0]


    def 添加数据(self, datas, 极致=True):
        conn, cursor, 数据表 = self.sql()
        if type(datas) is dict:
            try:
                字段s = set(datas)
                sql = f"insert into {数据表}({', '.join(字段s)}) VALUES ({', '.join(('%s',)*len(字段s))})"
                cursor.execute(sql, tuple(datas.values()))
                conn.commit()
            except Exception as err:
                print(f"{err} - {datas}")
                self.添加失败的数据.append(deepcopy(datas))
                if not self.持久连接:
                    try: conn.close()
                    except: pass
                if self.添加失败立即报错:
                    raise Exception("存在添加失败的数据, 通过 orm.添加失败的数据 查看")
                return False
            if not self.持久连接:
                try: conn.close()
                except: pass
            return True
        else:
            size = self.数据分组尺寸
            fails = []
            df = pd.DataFrame(datas)
            字段s = set(df.columns)
            datas = json.loads(df.to_json(orient='records'))
            df = None
            # 初始化数据库连接
            sql = f"insert into {数据表}({', '.join(字段s)}) VALUES ({', '.join(('%s',)*len(字段s))})"
            # 批量上传
            datas = [datas[size*(i-1): size*i] for i in range(1, ceil(len(datas)/size)+1)]
            group_number = len(datas)
            for i, idatas in enumerate(datas):
                print(f'\r正在批量上传第 {i+1}/{group_number} 组, 每组 {size} 条', end='    ')
                values = tuple([tuple(x.values()) for x in idatas])
                try:
                    cursor.executemany(sql, values)
                    conn.commit()
                except Exception as err:
                    conn.rollback()  # 回滚
                    for x in idatas: fails.append(x)
                    print(f'本组插入失败, 已回滚 - {err}')
            # 逐条上传
            if 极致 and fails:
                print('\n已开启极致模式, 开始对批量上传失败的进行逐条上传')
                fails, datas, total = [], fails, len(fails)
                for count, data in enumerate(datas):
                    print(f'\r正在逐条上传第 {count+1}/{total} 条', end='    ')
                    try: cursor.execute(sql, tuple(data.values()))
                    except Exception as err:
                        fails.append(data)
                        print(f"{err} - {data}    ")
                    if (count+1) % size == 0: conn.commit()
                conn.commit()
            # 关闭数据库连接
            try:
                if not self.持久连接: conn.close()
            except: pass
            print(f'\n\n上传完成, 上传失败共 {len(fails)} 条')
            if fails:
                添加失败 = self.添加失败的数据
                for x in fails: 添加失败.append(deepcopy(x))
                if self.添加失败立即报错:
                    raise Exception("存在添加失败的数据, 通过 orm.添加失败的数据 查看")
                return False
            return True
