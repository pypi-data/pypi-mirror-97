# -!- coding: utf-8 -!-
import re, os, time, random
from math import ceil
from random import shuffle
from multiprocessing.dummy import Pool as ThreadPool
# 同文件夹模块
from .tool import tool


class 装饰器():
    tool = tool

    def 失败重试(最高次数=5, 重试间隔=0, 失败返回=Exception("-"), 装饰对象是实例方法=False):
        def 装饰器(func):
            最高次数_, 重试间隔_, 失败返回_ = 最高次数, 重试间隔, 失败返回
            name = str(func)
            name = re.findall('function (.+) at', name) or re.findall('method (.+) of', name) or [name]
            name = name[0]
            def newfunc(*vs, **kvs):
                最高次数 = kvs.pop('最高次数', 最高次数_)
                重试间隔 = max(0, kvs.pop('重试间隔', 重试间隔_))
                失败返回 = kvs.pop('失败返回', 失败返回_)
                for i in range(1, 最高次数 + 1):
                    try:
                        r = func(*vs, **kvs)
                        状态 = True
                        break
                    except Exception as err:
                        状态 = False
                        e = err
                        if i == 1: print(f"执行函数 {name} 第{i}/{最高次数}次失败, {重试间隔}秒后将进行重试    ", end='')
                        else: print(f"\r执行函数 {name} 第{i}/{最高次数}次失败, {重试间隔}秒后将进行重试    ", end='')
                        if i < 最高次数: time.sleep(重试间隔)
                if 状态:
                    if i > 1: print()
                    return r
                else: print(f"\n{e}")
                if type(失败返回) is Exception: raise e
                elif re.findall('method|function', str(type(失败返回))):
                    if 装饰对象是实例方法: vs = vs[1:]
                    return 失败返回(err=e, vs=vs, kvs=kvs)
                else: return 失败返回
            return newfunc
        return 装饰器

    @classmethod
    def 计时(cls, func):
        任务名称 = cls.tool.提取任务名称(func)
        def newfunc(*v, **kv):
            开始时间 = time.time()
            r = func(*v, **kv)
            print(f"{任务名称} - 运行了{round(time.time() - 开始时间, 2)}秒")
            return r
        return newfunc

    @classmethod
    def 多线程(cls, 更新代理=None, 更新ua=None, 判断是否执行成功=None):

        def 装饰器(func):

            寄存器 = dict(
                更新代理 = 更新代理 or False,
                判断是否执行成功 = 判断是否执行成功 or (lambda o: True),
                更新ua = 更新ua or (lambda : None)
            )
            
            def newfunc(*vs, datas={}, 线程数=20, 返值分组尺寸=None,
                最高次数=10, 重试间隔=0,
                更新代理=None, 代理有效时长=0, 更新ua=None, 判断是否执行成功=None, **kvs):

                # 自动修正返值分组尺寸
                if 返值分组尺寸: 返值分组尺寸 = min(返值分组尺寸, len(datas))

                # 确定 更新代理 的方法
                # False 表示不需要更新代理, 将关闭此功能
                # 如果不是False, 且未传入, 则使用预定义的方法
                if 更新代理 is not False:
                    更新代理 = 更新代理 or 寄存器['更新代理']

                # 确定 更新ua 的方法
                if 更新ua is False:  # False 表示不需要更新ua, 将关闭此功能
                    更新ua = lambda : None
                elif not 更新ua:  # 如果不是False, 且未传入, 则使用预定义的方法
                    更新ua = 寄存器['更新ua']
                
                # 确定 判断是否执行成功 的方法
                if 判断是否执行成功 is False:  # False 表示不需要判断, 直接返回成功
                    判断是否执行成功 = lambda o: True
                elif not 判断是否执行成功:  # 如果不是False, 且未传入, 则使用预定义的方法
                    判断是否执行成功 = 寄存器['判断是否执行成功']
                
                # 转化格式为: [{'key': 0, 'data': data0}, {'key': 1, 'data': data1}]
                if type(datas) is list:  # [{}, {}, ...]
                    datas = [dict(key=key, data=data) for key, data in zip(range(len(datas)), datas)]
                elif type(datas) is dict:  # {key1:{}, key2:{}, ...}
                    datas = [dict(key=key, data=data) for key, data in datas.items()]
                else:
                    raise Exception("datas格式须为: [{}, {}, ...]")

                def f2(kw):
                    try:
                        kw['return'] = func(*vs, **kvs, **kw['data'])
                        # **kw['data'] 放在 **kvs 后面, 估计可以用特别值覆盖通用值
                        kw['msg'] = 判断是否执行成功(kw)
                    except Exception as err:
                        kw['msg'] = err
                    return kw
            
                # 初始化数据
                成功 = []
                失败 = datas
                datas = None  # 释放内存
                random.shuffle(失败)
                if 更新代理:
                    更新代理()
                    cutime = time.time()
                    代理未失效 = True
                print()

                # 开始多线程查询
                for i次数 in range(1, 最高次数+1):
                    if not 失败:  # 如果查询完了, 就提前结束
                        break
                    else:
                        尚未查询 = cls.tool.数据分组(失败, 线程数)
                        失败 = []
                        total = len(尚未查询)
                        for count, kws in enumerate(尚未查询):
                            print(f'\r第{i次数}/{最高次数}次, 第{count + 1}/{total}组 {cls.tool.当前时间()}', end='    ')
                            更新ua()
                            if 更新代理:
                                if 代理未失效 is False:
                                    print('\r认为代理已失效, 正在自动更新代理', end='    ')
                                    更新代理()
                                    cutime = time.time()
                                elif 代理有效时长 and (time.time() - cutime >= 代理有效时长):
                                    print(f'\r代理已使用超过理论有效时长 {代理有效时长} 秒, 正在自动更新代理', end='    ')
                                    更新代理()
                                    cutime = time.time()
                            # 多线程请求
                            if 线程数 > 1:
                                pool = ThreadPool(线程数 + 2)
                                results = pool.map(f2, kws)
                                pool.close()
                                pool.join()
                            else:  # 单线程不需要使用pool
                                results = [f2(kws[0])]
                            # 处理请求结果
                            if 更新代理:
                                代理未失效 = False
                                for kw in results:
                                    if kw['msg'] is True:
                                        代理未失效 = True
                                        成功.append(kw)
                                    else:
                                        失败.append(kw)
                            else:
                                for kw in results:
                                    成功.append(kw) if kw['msg'] is True else 失败.append(kw)
                            if type(返值分组尺寸) is int:
                                len_成功 = len(成功)
                                if len_成功 >= 返值分组尺寸:
                                    print(f'\r本次执行成功共 {len_成功} 条', end='    ')
                                    yield 成功
                                    成功 = []
                            time.sleep(重试间隔)
                if 成功 or (type(返值分组尺寸) is not int):
                    print(f'\r本次执行成功共 {len(成功)} 条', end='    ')
                    yield 成功
                print('\r执行结束', end='    ')
                yield '执行结束'
                print(f'\r执行失败共 {len(失败)} 条', end='    ')
                yield 失败

            return newfunc
        
        return 装饰器

# 开始测试
# 开始测试