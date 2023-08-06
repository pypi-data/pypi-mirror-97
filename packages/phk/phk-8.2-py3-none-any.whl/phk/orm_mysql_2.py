# -!- coding: utf-8 -!-
import time, json, pymysql
import pandas as pd
from math import ceil


class 过滤器():

    def __init__(self, name=None, 条件=None, orm=None, 查询字段='*'):
        self.name = name
        self.条件 = 条件
        self.orm = orm
        self.c = orm.c
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
        if self.条件 == o.条件: return self.copy(self.条件)
        return self.copy(f"({self.条件}) and ({o.条件})")

    def __or__(self, o):  # |
        if self.条件 == o.条件: return self.copy(self.条件)
        return self.copy(f"({self.条件}) or ({o.条件})")

    def __invert__(self):  # ~
        return self.copy(f"not ({self.条件})")

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
            return self.orm.sql(sql)[0]
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
        else:  # orm[过滤器]
            if self.条件:
                return self.copy(f"({self.条件}) and ({key.条件})", 查询字段=self.查询字段)
            return self.copy(key.条件, 查询字段=self.查询字段)

    def __setitem__(self, key, value):
        type_ = type(key)
        if type_ is slice: raise Exception("不支持切片修改, 仅支持条件修改")
        elif type_ is int: raise Exception("不支持索引修改, 仅支持条件修改")
        elif type_ is str:
            zds = {key}
            条件 = f" where {self.条件}" if self.条件 else ''
        elif type_ is tuple:
            zds = set(key)
            条件 = f" where {self.条件}" if self.条件 else ''
        else:
            if self.查询字段 == '*':
                zds = set(self.orm.columns)
                pk = self.orm.pk
                if (pk not in value) and (pk in zds): zds.remove(pk)
            else:
                zds = set(self.查询字段.split(','))
            if self.条件:
                条件 = f" where ({self.条件}) and ({key.条件})"
            else:
                条件 = f" where {key.条件}"
        value = {k: value.get(k) for k in zds}
        value = ','.join([f"{k}={json.dumps(v, ensure_ascii=False)}" for k, v in value.items()])
        sql = "update {数据表}" + f" set {value}" + 条件
        return self.orm.sql(sql)

    def delete(self):
        sql = "delete from {数据表}" + f" where {self.条件}"
        return self.orm.sql(sql=sql)

    def isin(self, o=[]):
        if not o: return self.copy(f"({self.name} is null) and ({self.name} is not null)")
        o = set(o)
        条件null = None
        if None in o:
            条件null = f"{self.name} is null"
            o.remove(None)
            if not o: return self.copy(条件null)
        types = set(type(x) for x in o)
        if (types == {str}) or (types == {int}):
            条件in = f"{self.name} in ({','.join(json.dumps(x, ensure_ascii=False) for x in o)})"
            if 条件null: return self.copy(f"({条件null}) or ({条件in})")
            return self.copy(条件in)
        raise Exception("isin列表只接收[None, int] 或 [None, str]")

    def notin(self, o=[]):
        o = set(o)
        if not o: return self.copy(f"({self.name} is null) or ({self.name} is not null)")
        elif None in o:
            o.remove(None)
            条件null = f"{self.name} is not null"
            if o:
                types = set(type(x) for x in o)
                if (types != {str}) and (types != {int}): raise Exception("notin列表只接收[None, int] 或 [None, str]")
                条件in = f"{self.name} not in ({','.join(json.dumps(x, ensure_ascii=False) for x in o)})"
                return self.copy(f"({条件null}) and ({条件in})")
            return self.copy(条件null)
        else:
            types = set(type(x) for x in o)
            if (types != {str}) and (types != {int}): raise Exception("notin列表只接收[None, int] 或 [None, str]")
            条件in = f"{self.name} not in ({','.join(json.dumps(x, ensure_ascii=False) for x in o)})"
            条件null = f"{self.name} is null"
            return self.copy(f"({条件null}) or ({条件in})")

class cc():
    pass

class orm_mysql():

    '''

<<使用教程>>


一, 连接数据库


账号 = {'host': '', 'user': '', 'passwd': '', 'port': xxxx, 'db':'', 'sheet':''}
orm = orm_mysql(账号=账号, 持久连接=True)
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

查询 id>=10 的数据: orm[orm.c.id >= 10][:]

查询 id==10 的数据: orm[orm.c.id == 10][:]

查询 title=='t' 的数据: orm[orm.c.title == 't'][:]

用正则表达式查询: orm[orm.c.title.re_m('.*')][:]

查询id在(1,3,5)里面的数据: orm[orm.c.id.isin([1,3,5])][:]

查询title在('t1','t2')里面的数据: orm[orm.c.title.isin(['t1','t2'])][:]

查询id不在(1,3,5)里面的数据: orm[orm.c.id.notin([1,3,5])][:]

查询title不在('t1','t2')里面的数据: orm[orm.c.title.notin(['t1','t2'])][:]

并联查询:
orm[(orm.c.id > 5) & (orm.c.title.re_m('.*'))][:]  # and
orm[(orm.c.id > 5) | (orm.c.title.re_m('.*'))][:]  # or
orm[~ (orm.c.id > 5)]  # 将条件取反
orm[() & (~ (() | (() & ()) | ()))][:]  # 可无限嵌套

串联查询
orm[orm.c.id > 5][orm.c.title == 't'][][][]...[:]  # 可无限嵌套

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
orm[orm.c.id >= 10].delete()


3.通过过滤器[ ]修改数据

kw = dict(title=xx, content=xx, 相似度=xx, ....)
orm[一系列过滤器] = kw  # 对所有字段赋值
orm[一系列过滤器]['title'] = kw  # 仅对title字段赋值
orm[一系列过滤器]['title','content'] = kw  # 仅对title和content字段赋值
'''

    数据分组尺寸 = 1000
    添加失败立即报错 = True
    极致上传 = False

    def __init__(self, 账号, 持久连接=True):
        self.添加失败的数据 = []  # 1
        self.提取账号(账号)  # 1
        self.持久连接 = 持久连接  # 1
        if 持久连接: self.conn, self.cursor = self.创建连接()  # 2
        self.获取字段列表()  # 3  self.columns, self.pk

        # 4 创建过滤器
        self.c = c = cc()
        for name in self.columns: exec(f"c.{name} = 过滤器(name='{name}', orm=self)")
        self.过滤器 = eval(f"c.{self.columns[-1]}")

    def 创建连接(self):
        for i in range(5):
            try:
                conn = pymysql.connect(**self.账号)
                cursor = conn.cursor(cursor=pymysql.cursors.DictCursor)
                return conn, cursor
            except Exception as err:
                e = err
                time.sleep(1)
        raise e

    def 提取账号(self, o):
        def get账号(o):
            r = {}
            for k, v in o.items():
                if type(v) is dict: r.update(get账号(v))
                else: r[k] = v
            return r
        o = get账号(o)
        self.账号 = dict(host=o['host'], user=o['user'], passwd=o['passwd'], port=o['port'], db=o['db'])
        self.name = o['sheet']

    def __getitem__(self, key): return self.过滤器.__getitem__(key)

    def __setitem__(self, key, value): return self.过滤器.__setitem__(key, value)

    def close(self): return self.conn.close()

    def sql(self, sql=None, **kvs):
        数据类型 = kvs.get('数据类型', 'list').lower()
        if self.持久连接:
            conn, cursor = self.conn, self.cursor
            conn.ping(reconnect=True)
        else:
            conn, cursor = self.创建连接()
        if sql:
            sql = sql.replace('{数据表}', self.name)
            cursor.execute(sql)
            datas = list(cursor.fetchall())
            conn.commit()
            if not self.持久连接: conn.close()
            if 数据类型 in ('pandas', 'df'): return pd.DataFrame(datas)
            return datas
        return conn, cursor, self.name

    def append(self, kw): return self.添加数据(datas=kw)
    
    def __iadd__(self, kws):  # 同list: orm += [{'title': '2020-02-25-0'}, {'title': '2020-02-25-1'}]
        r = self.添加数据(datas=kws)
        print(r)
        return self

    def 获取字段列表(self):
        sql = "select column_name as name,column_key as ispk from information_schema.columns where table_name = '{数据表}'"
        self.columns = columns = []
        self.pk = ''
        for x in self.sql(sql=sql):
            columns.append(x['name'])
            if x['ispk']: self.pk = x['name']

    def 添加数据(self, datas):
        conn, cursor, 数据表 = self.sql()
        if type(datas) is dict:
            try:
                字段s = datas.keys()
                sql = f"insert into {数据表}({', '.join(字段s)}) VALUES ({', '.join(('%s',)*len(字段s))})"
                cursor.execute(sql, tuple(datas.values()))
                conn.commit()
            except Exception as err:
                print(f"{err} - {datas}"[:20])
                self.添加失败的数据.append((datas, err))
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
            字段s = set(y for x in datas for y in x.keys())
            datas = [tuple([kw.get(k) for k in 字段s]) for kw in datas]
            # 初始化数据库连接
            sql = f"insert into {数据表}({', '.join(字段s)}) VALUES ({', '.join(('%s',)*len(字段s))})"
            # 批量上传
            datas = [datas[size*(i-1): size*i] for i in range(1, ceil(len(datas)/size)+1)]
            group_number = len(datas)
            for i, idatas in enumerate(datas):
                print(f'\r正在批量上传第 {i+1}/{group_number} 组, 每组 {size} 条', end='    ')
                try:
                    cursor.executemany(sql, tuple(idatas))
                    conn.commit()
                except Exception as err:
                    conn.rollback()  # 回滚
                    for x in idatas: fails.append((x, err))
                    print(f'本组插入失败, 已回滚 - {err}')
            # 逐条上传
            if self.极致上传 and fails:
                print('\n已开启极致上传模式, 开始对批量上传失败的进行逐条上传')
                fails, datas, total = [], [a for a, b in fails], len(fails)
                for count, data in enumerate(datas):
                    print(f'\r正在逐条上传第 {count+1}/{total} 条', end='    ')
                    try: cursor.execute(sql, data)
                    except Exception as err:
                        fails.append((data, err))
                        print(f"{err} - {data}"[:20])
                    if (count+1) % size == 0: conn.commit()
                conn.commit()
            # 关闭数据库连接
            try:
                if not self.持久连接: conn.close()
            except: pass
            print(f'\n\n上传完成, 上传失败共 {len(fails)} 条')
            if fails:
                添加失败 = self.添加失败的数据
                for kw, err in fails: 添加失败.append((dict(zip(字段s, kw)), err))
                if self.添加失败立即报错: raise Exception("存在添加失败的数据, 通过 orm.添加失败的数据 查看")
                return False
            return True
