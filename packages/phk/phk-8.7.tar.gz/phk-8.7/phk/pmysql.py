# -!- coding: utf-8 -!-
import time, json, pymysql, traceback
import pandas as pd
import numpy as np
from math import ceil

class pmysql():
    mysql账号 = {}
    持久连接 = False
    数据分组尺寸 = 1000
    
    def __init__(self, mysql账号={}):  # {代号: {账号, 数据库, 数据表}}
        if mysql账号: self.mysql账号 = mysql账号
        self.快速读写地址 = self.mysql账号.get('快速读写', {})
    
    def 读(self, id): return self.快速读写(id=id, model='读')
    def 写(self, id, content): return self.快速读写(id=id, model='写', content=content)
    def 快速读写(self, id, model, content=None):
        nowtime = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
        for n in range(3):
            try:
                conn = pymysql.connect(**self.快速读写地址['账号'], db=self.快速读写地址['数据库'])
                cursor = conn.cursor(cursor=pymysql.cursors.DictCursor)
                if model == '读':
                    sql = f"select content from {self.快速读写地址['数据表']} where id = {id}"
                elif model == '写':
                    content = json.dumps(content, ensure_ascii=False)
                    sql = f"update {self.快速读写地址['数据表']} set content='{content}', 更新时间='{nowtime}' where id = {id}"
                cursor.execute(sql)
                data = cursor.fetchall()
                data = json.loads(data[0]['content'] or "null") if data else None
                # data[0]['content'] 一定是字符串, 空字符串也即null
                conn.commit()
                if not self.持久连接: conn.close()
                return data
            except:
                try:
                    if not self.持久连接: conn.close()
                except: pass
                time.sleep(1)
    
    def 创建连接(self, 地址):
        for i in range(5):
            try:
                conn = pymysql.connect(**地址['账号'], db=地址['数据库'])
                cursor = conn.cursor(cursor=pymysql.cursors.DictCursor)
                return conn, cursor
            except Exception as err:
                e = err
                time.sleep(1)
        raise e
    
    def 操作数据表(self, 代号, sql=None, **kw):
        数据类型 = kw.get('数据类型', 'list').lower()
        地址 = self.mysql账号[代号] if type(代号) is str else 代号
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
    
    def get字段(self, 代号):
        sql字段 = self.操作数据表(代号=代号, sql="select column_name as name from information_schema.columns where table_name = '{数据表}'")
        return [x['name'] for x in sql字段]
    
    def 数据清洗(self, 代号, datas, **kw):
        kvs = kw.get('kvs') or {}
        忽略字段 = kw.get('忽略字段') or set()
        df = datas if (type(datas) is pd.core.frame.DataFrame) else pd.DataFrame(datas)
        for k, v in kvs.items(): df[k] = v
        字段s = set(df.columns) - set(忽略字段) & set(self.get字段(代号=代号))
        df = pd.DataFrame(df, columns=字段s)
        datas = json.loads(df.to_json(orient='records'))
        return dict(datas=datas, 字段s=字段s)
    
    def 添加数据(self, 代号, datas, 极致=True, 忽略字段=set(), **kw):
        调试 = kw.get('调试', True)
        size = kw.get('size') or self.数据分组尺寸
        kvs = kw.get('kvs')
        打印状态 = kw.get('打印状态', True)
        fails = []
        if (type(datas) is pd.core.frame.DataFrame) or datas:
            datas = self.数据清洗(代号=代号, datas=datas, 忽略字段=忽略字段, kvs=kvs)
            datas, 字段s = [datas[x] for x in ('datas', '字段s')]
            # 初始化数据库连接
            conn, cursor, 数据表 = self.操作数据表(代号=代号) 
            sql = f"insert into {数据表}({', '.join(字段s)}) VALUES ({', '.join(('%s',)*len(字段s))})"
            # 批量上传
            datas = [datas[size*(i-1): size*i] for i in range(1, ceil(len(datas)/size)+1)]
            group_number = len(datas)
            for i, idatas in enumerate(datas):
                if 打印状态: print(f'\r正在批量上传第 {i+1}/{group_number} 组, 每组 {size} 条', end='')
                values = tuple([tuple(x.values()) for x in idatas])
                try:
                    cursor.executemany(sql, values)
                    conn.commit()
                except:
                    conn.rollback()
                    fails += idatas
                    if 打印状态: print('本组插入失败, 已回滚')
            # 逐条上传
            if 极致 and fails:
                if 打印状态: print('\n已开启极致模式, 开始逐条上传')
                fails, datas, total = [], fails, len(fails)
                for count, data in enumerate(datas):
                    if 打印状态: print(f'\r正在逐条上传第 {count+1}/{total} 条', end='')
                    try: cursor.execute(sql, tuple(data.values()))
                    except:
                        if 调试: traceback.print_exc()
                        fails.append(data)
                    if (count+1) % size == 0: conn.commit()
                conn.commit()
            # 关闭数据库连接
            try:
                if not self.持久连接: conn.close()
            except: pass
        if 打印状态: print(f'\n\n上传完成, 上传失败共 {len(fails)} 条')
        return fails
    
    def 修改数据(self, 代号, datas, pro_key, **kw):
        调试 = kw.get('调试', False)
        忽略字段 = kw.get('忽略字段', set())
        size = kw.get('size', 1000)
        打印状态 = kw.get('打印状态', True)
        fails = []
        if datas:
            字段s = set(self.get字段(代号=代号)) - set(忽略字段) - {pro_key}
            datas = [(c+1, x[pro_key], {k:v for k,v in x.items() if k in 字段s}) for c,x in enumerate(datas)]
            total = len(datas)
            conn, cursor, 数据表 = self.操作数据表(代号=代号)
            for count, pro_v, data in datas:
                if 打印状态: print(f'\r正在逐条修改第 {count}/{total} 条', end='')
                updates = ','.join([f"{k}={json.dumps(v, ensure_ascii=False)}" for k, v in data.items()])
                pro_v = json.dumps(pro_v, ensure_ascii=False)
                try:
                    sql = f"update {数据表} set {updates} where {pro_key} = {pro_v}"
                    cursor.execute(sql)
                except:
                    fails.append(data)
                    if 调试: traceback.print_exc()
                if count % size == 0: conn.commit()
            conn.commit()
            try:
                if not self.持久连接: conn.close()
            except: pass
        if 打印状态: print(f'\n\n修改完成, 修改失败共 {len(fails)} 条')
        return fails
    
    # def 数据表迁移(self, 原表, 新表, where条件, 迁移字段='*', 去除主键='id', 模式='复制', 字段映射=None):
    #     sql = f"select {迁移字段} from 数据表 where {where条件}" if where条件 else f"select {迁移字段} from 数据表"
    #     sql = sql.replace(' from 数据表', ' from {数据表}')
    #     datas = self.操作数据表(代号=原表, sql=sql)
    #     if datas:
    #         if 去除主键 in datas[0]:
    #             for data in datas:
    #                 data.pop(去除主键)
    #         if 字段映射:
    #             for data in datas:
    #                 for oldkey, newkey in 字段映射.items():
    #                     data[newkey] = data.pop(oldkey)
    #         fails = self.添加数据(代号=新表, datas=datas, 极致=True)
    #         if 模式 in ['剪切', '剪贴', 'cut']:
    #             sql = f"delete from 数据表 where {where条件}" if where条件 else f"delete from 数据表"
    #             sql = sql.replace(' from 数据表', ' from {数据表}')
    #             self.操作数据表(代号=原表, sql=sql)
    #         return fails

    def 创建数据库(self, 代号, 数据库):
        地址 = self.mysql账号[代号] if type(代号) is str else 代号
        for i in range(5):
            try:
                conn = pymysql.connect(**地址['账号'])
                cursor = conn.cursor(cursor=pymysql.cursors.DictCursor)
            except:
                time.sleep(1)
        cursor.execute(f"create database {数据库}")
        conn.commit()
        if not self.持久连接: conn.close()
        return True
    
    # def 创建数据表(self, 代号, 数据表, 字段s):
    #     地址 = self.mysql账号[代号] if type(代号) is str else 代号
    #     for i in range(5):
    #         try:
    #             conn = pymysql.connect(**地址['账号'], db=地址['数据库'])
    #             cursor = conn.cursor(cursor=pymysql.cursors.DictCursor)
    #         except:
    #             time.sleep(1)
    #     sql = f"create table {数据表} ({字段s}) engine=innodb charset=utf8mb4"
    #     cursor.execute(sql)
    #     conn.commit()
    #     if not self.持久连接: conn.close()
    #     return True
    
    # def 如何创建数据表(self):
    #     print('''
    #     create table 拟定的数据表名称 (
    #     id int(100) primary key auto_increment not null,
    #     添加日期 datetime,
    #     说明 varchar(1000)
    #     ) engine=innodb charset=utf8mb4
    #     ''')
