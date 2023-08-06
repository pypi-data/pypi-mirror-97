# 第三方库
import pickle, re, requests, time
import pandas as pd
import numpy as np
from copy import deepcopy


class 设置相似文章():
    文章库 = {}
    推荐数量 = 5  # 每篇文章需要推荐的数量
    相似度缓存路径 = ''
    获取所有文章接口 = ''
    设置相似文章接口 = ""
    
    def __init__(self):
        self.检测数据完整性()  # 0
        self.创建文章库()  # 1
        self.载入相似度缓存()  # 1
        self.矫正相似度缓存字段()  # 2
    
    def 相似度分析(self, t1, t2):
        # return 0.856
        return '占位函数'
    
    def 检测数据完整性(self):
        # 判断相似度缓存路径
        if not self.相似度缓存路径: raise Exception("子类中需覆盖重写 相似度缓存路径, 且每个域名应设置不同的路径")
        if not self.获取所有文章接口: raise Exception("子类中需覆盖重写 获取所有文章接口")
        if not self.设置相似文章接口: raise Exception("子类中需覆盖重写 设置相似文章接口")
        if self.相似度分析(t1='aaaaa', t2='bbbbb') == '占位函数':
            raise Exception("子类中需覆盖重写 相似度分析 方法, 传入(t1, t2), return 浮点数")
    
    # 对 推荐文章为空 的文章进行推荐
    def 增量推荐文章(self):
        for 分类, 文章s in self.分类文章库.items():
            pks = [pk for pk, kw in 文章s.items() if not kw['相似文章pks']]
            if pks: self.pks_set_相似文章pks(分类, pks)
        print("增量推荐文章 完成")
    
    # 对 所有文章 进行推荐
    def 全部文章推荐文章(self):
        i, total = 0, len(self.分类文章库)
        for 分类, 文章s in self.分类文章库.items():
            i += 1
            print(f"\r                                            文章分类:{i}/{total}    ", end='')
            pks = list(文章s.keys())
            self.pks_set_相似文章pks(分类, pks)
        print("\n全部文章推荐文章 完成")
    
    # self.文章库 = {pk1:{kw1}, pk2:{kw2}, ...}
    # kw1 = [{pk:pk,标题:标题,相似文章pks:[1,2,3, ...]}]
    def 创建文章库(self):
        texts = requests.get(self.获取所有文章接口).json()
        文章库, 分类文章库 = {}, {}
        for pk, title, pks, sort in texts:
            pks = pks.replace(' ', '') if pks else []
            pks = list(map(int, pks.split('-'))) if pks else []
            sort = str(sort)
            kw = dict(pk=pk, title=title, 相似文章pks=pks, sort=sort)
            文章库[pk] = kw
            分类文章库.setdefault(sort, {})[pk] = kw
        self.文章库 = 文章库
        self.分类文章库 = 分类文章库
    
    # return 用来计算相似度的文本
    # 目前以title计算相似度, 后期可改为以正文计算相似度
    def pk_get_计算文本(self, pk):  return self.文章库[pk]['title']

    def 载入相似度缓存(self):
        try:
            with open(self.相似度缓存路径, 'rb') as fa:
                self.相似度缓存 = pickle.load(fa)
        except:
            self.相似度缓存 = {}

    # 由于文章增删变化, 需要修改缓存的列数
    def 矫正相似度缓存字段(self):
        # pks: {pk1, pk2, ...}
        for 分类, kws in self.分类文章库.items():
            df = self.相似度缓存.get(分类)
            if not (type(df) is pd.core.frame.DataFrame):
                self.相似度缓存[分类] = df = pd.DataFrame(dict(pk=[])).set_index('pk')
                df.index = df.index.astype(np.int64)
            pks = set(kws)
            旧的缓存字段 = set(df.columns)
            已失效pk = 旧的缓存字段 - pks
            新增的pk = pks - 旧的缓存字段
            已失效index = set(df.index) - pks
            if 已失效pk: df.drop(已失效pk, axis=1, inplace=True)
            if 已失效index: df.drop(已失效index, axis=0, inplace=True)
            for pk in 新增的pk: df[pk] = -1.0
        print('已矫正相似度缓存字段')
    
    def 保存相似度缓存(self):
        with open(self.相似度缓存路径, 'wb') as fa:
            pickle.dump(self.相似度缓存, fa)
        self.待保存计数 = 0

    # return {pk1:相似度1, pk2:相似度2, ...}
    待保存计数 = 0
    def pk_计算_相似的pks(self, 分类, pk, 推荐数量):
        df = self.相似度缓存[分类]
        if pk not in df.index: df.loc[pk] = -1.0
        相似度s = df.loc[pk]
        需计算的pk = 相似度s[相似度s < 0].index.to_list()
        if 需计算的pk:
            text = self.pk_get_计算文本(pk=pk)
            相似度s = deepcopy(相似度s)
            total = 相似度s.shape[0]
            for count,k in enumerate(需计算的pk):
                for i in range(10):
                    t2 = self.pk_get_计算文本(pk=k)
                    v = self.相似度分析(t1=text, t2=t2)
                    if (type(v) is float) or (type(v) is int):
                        相似度s[k] = v
                        break
                else:
                    相似度s[k] = v = 0
                print(f"\r{count}/{total}[{v}]        ", end='')
                self.待保存计数 += 1
                if self.待保存计数 >= 100: self.保存相似度缓存()
            df.loc[pk] = 相似度s = 相似度s.sort_values(ascending=False)
        return dict(相似度s[相似度s < 1][:推荐数量])
    
    # 对传入的pks设置推荐文章, 并提交到服务器
    def pks_set_相似文章pks(self, 分类, pks):
        if pks:
            文章库 = self.文章库
            total = len(pks)
            for i, pk in enumerate(pks):
                print(f"\r                         分类下的文章:{i}/{total}    ", end='')
                rpks = self.pk_计算_相似的pks(分类=分类, pk=pk, 推荐数量=self.推荐数量)
                文章库[pk]['相似文章pks'] = rpks = list(rpks.keys())
                rpks = '-'.join(map(str, rpks)) if rpks else ''
                url = self.设置相似文章接口.format(pk=pk, rpks=rpks)
                rt = requests.get(url).text  # ['设置成功', ]
            self.保存相似度缓存()
