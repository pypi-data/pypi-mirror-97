# -!- coding: utf-8 -!-
import re, os, sys, requests, json, math, time, copy, random
import pandas as pd
from collections import Counter

class 善检网api第2版_套餐():
    # domain = 'http://test-mc.tijian8.com'  # 测试服务器
    domain = 'https://mc.tijian8.com'
    账号, 密码 = '', ''
    
    def __init__(self):
        self.验证变量完整性()
        self.更新token()

    def 验证变量完整性(self):
        if not self.domain: raise Exception("domain 缺失")
        if not self.账号: raise Exception("账号 缺失")
        if not self.密码: raise Exception("密码 缺失")
        self.地址get经纬度(地址='福建省泉州市')

    
    # 占位函数, 需要在子类中改写
    def 地址get经纬度(self, 地址):
        print(f'''
        需覆盖以下方法:
        def 地址get经纬度(self, 地址):
            return dict(经度=0, 纬度=0)
        self.地址get经纬度(地址='福建省泉州市')
        ''')
        raise Exception("def 地址get经纬度(self, 地址):")
    
    图片库 = {'中年人': ['ZhongNian8.jpg', 'ZhongNian9.jpg', 'ZhongNian10.jpg', 'ZhongNianRen.jpg', 'ZhongNian1.jpg', 'ZhongNianRen3.jpg', 'ZhongNianRen2.jpg', 'ZhongNian2.jpg', 'ZhongNian3.jpg', 'ZhongNian7.jpg', 'ZhongNianRen5.jpg', 'ZhongNianRen4.jpg', 'ZhongNian6.jpg', 'ZhongNian4.jpg', 'ZhongNian5.jpg'], '入职': ['RuZhi14.jpg', 'RuZhi8.jpg', 'RuZhi9.jpg', 'RuZhi15.jpg', 'RuZhi11.jpg', 'RuZhi10.jpg', 'RuZhi12.jpg', 'RuZhi13.jpg', 'RuZhi.jpg', 'RuZhi2.jpg', 'RuZhi3.jpg', 'RuZhi4.jpg', 'RuZhi5.jpg', 'RuZhi7.jpg', 'RuZhi6.jpg'], '公务员': ['GongWuYuan7.jpg', 'GongWuYuan14.jpg', 'GongWuYuan15.jpg', 'GongWuYuan6.jpg', 'GongWuYuan4.jpg', 'GongWuYuan.jpg', 'GongWuYuan16.jpg', 'GongWuYuan5.jpg', 'GongWuYuan12.jpg', 'GongWuYuan13.jpg', 'GongWuYuan11.jpg', 'GongWuYuan3.jpg', 'GongWuYuan10.jpg', 'GongWuYuan8.jpg', 'GongWuYuan9.jpg'], '女性': ['NvXing.jpg', 'NvXing9.jpg', 'NvXing8.jpg', 'NvXing3.jpg', 'NvXing2.jpg', 'NvXing6.jpg', 'NvXing7.jpg', 'NvXing5.jpg', 'NvXing4.jpg', 'NvXing12.jpg', 'NvXing13.jpg', 'NvXing11.jpg', 'NvXing10.jpg', 'NvXing14.jpg', 'NvXing15.jpg'], '孕前': ['YunQian.jpg', 'YunQian9.jpg', 'YunQian8.jpg', 'YunQian6.jpg', 'YunQian7.jpg', 'YunQian5.jpg', 'YunQian4.jpg', 'YunQian3.jpg', 'YunQian2.jpg', 'YunQian12.jpg', 'YunQian13.jpg', 'YunQian11.jpg', 'YunQian10.jpg', 'YunQian14.jpg', 'YunQian15.jpg', 'YunQian16.jpg'], '男性': ['NanXing5.jpg', 'NanXing4.jpg', 'NanXing6.jpg', 'NanXing7.jpg', 'NanXing3.jpg', 'NanXing2.jpg', 'NanXing.jpg', 'NanXing10.jpg', 'NanXing11.jpg', 'NanXing13.jpg', 'NanXing12.jpg', 'NanXing9.jpg', 'NanXing8.jpg'], '老年人': ['LaoNianRen9.jpg', 'LaoNianRen8.jpg', 'LaoNianRen12.jpg', 'LaoNianRen13.jpg', 'LaoNianRen11.jpg', 'LaoNianRen10.jpg', 'LaoNianRen14.jpg', 'LaoNianRen15.jpg', 'LaoNianRen.jpg', 'LaoNianRen5.jpg', 'LaoNianRen4.jpg', 'LaoNianRen6.jpg', 'LaoNianRen7.jpg', 'LaoNianRen3.jpg', 'LaoNianRen2.jpg'], '青少年': ['QingShaoNian9.jpg', 'QingShaoNian8.jpg', 'QingShaoNian3.jpg', 'QingShaoNian2.jpg', 'QingShaoNian5.jpg', 'QingShaoNian4.jpg', 'QingShaoNian6.jpg', 'QingShaoNian7.jpg', 'QingShaoNian11.jpg', 'QingShaoNian.jpg', 'QingShaoNian10.jpg', 'QingShaoNian12.jpg', 'QingShaoNian13.jpg', 'QingShaoNian14.jpg', 'QingShaoNian15.jpg'], '青年': ['QingNian4 2.jpg', 'QingNian.jpg', 'QingNian5.jpg', 'QingNian11.jpg', 'QingNian10.jpg', 'QingNian4.jpg', 'QingNian6.jpg', 'QingNian12.jpg', 'QingNian13.jpg', 'QingNian7.jpg', 'QingNian3.jpg', 'QingNian14.jpg', 'QingNian15.jpg', 'QingNian9.jpg', 'QingNian8.jpg']}
    大小写字典 = {'A': '_a', 'B': '_b', 'C': '_c', 'D': '_d', 'E': '_e', 'F': '_f', 'G': '_g', 'H': '_h', 'I': '_i', 'J': '_j', 'K': '_k', 'L': '_l', 'M': '_m', 'N': '_n', 'O': '_o', 'P': '_p', 'Q': '_q', 'R': '_r', 'S': '_s', 'T': '_t', 'U': '_u', 'V': '_v', 'W': '_w', 'X': '_x', 'Y': '_y', 'Z': '_z'}
    要转换的名称 = {}
    不转换的名称 = []
    
    def 字段转小写(self, item):
        if type(item) is dict:
            for key in list(item.keys()):
                if key not in self.不转换的名称:
                    if key in self.要转换的名称:
                        item[self.要转换的名称[key]] = item.pop(key)
                    else:
                        new_key = re.sub('^_', '', ''.join([self.大小写字典.get(x, x) for x in key]))
                        if new_key == key:
                            self.不转换的名称.append(key)
                        else:
                            self.要转换的名称[key] = new_key
                            item[self.要转换的名称[key]] = item.pop(key)
            for value in item.values():
                self.字段转小写(value)
        elif type(item) is list:
            for x in item:
                self.字段转小写(x)
        return item
    
    def 转中文(self, item):
        if type(item) is dict:
            for key in list(item.keys()):
                if key in self.中文字典:
                    item[self.中文字典[key]] = item.pop(key)
            for value in item.values():
                if type(value) in [list, dict]:
                    self.转中文(value)
        elif type(item) is list:
            for x in item:
                self.转中文(x)
        return item
    
    def 更新token(self):
        url = f'{self.domain}/login'
        headers = {'Content-Type': 'application/json'}
        data = json.dumps({"account": self.账号, "password": self.密码})
        r = requests.post(url, data=data, headers=headers)
        self.token = r.json()['data']['token']
        
    def 请求服务器(self, 方法, api, data=None, params=None):
        url = f'{self.domain}/{api}'
        data = json.dumps(data) if data else None
        for n in range(3):
            headers = {'Content-Type': 'application/json', 'Authorization': f"attackFind:{self.token}"}
            if 方法 == 'get':
                r = requests.get(url, data=data, params=params, headers=headers).json()
            elif 方法 == 'post':
                r = requests.post(url, data=data, headers=headers).json()
            elif 方法 == 'put':
                r = requests.put(url, data=data, params=params, headers=headers).json()
            if r['status'] < 1000:
                break
            else:
                self.更新token()
        return r

    
    def post(self, api, data=None, 转中文=True):
        if 转中文:
            return self.转中文(self.字段转小写(self.请求服务器(方法='post', api=api, data=data)))
        return self.字段转小写(self.请求服务器(方法='post', api=api, data=data))

    def get(self, api, params=None, 转中文=True):
        if 转中文:
            return self.转中文(self.字段转小写(self.请求服务器(方法='get', api=api, params=params)))
        return self.字段转小写(self.请求服务器(方法='get', api=api, params=params))
    
    def put(self, api, data=None, 转中文=True):
        if 转中文:
            return self.转中文(self.字段转小写(self.请求服务器(方法='put', api=api, data=data)))
        return self.字段转小写(self.请求服务器(方法='put', api=api, data=data))
