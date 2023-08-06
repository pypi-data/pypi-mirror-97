# -!- coding: utf-8 -!-
import re, os, sys, requests, json, math, time, copy, random
import pandas as pd
import numpy as np
from copy import deepcopy
from collections import Counter
from functools import reduce
from collections import Counter
from random import sample


class 供应链api():
    domain='http://112.74.78.240:31001'
    账号, 密码 = '', ''
    
    def __init__(self, 账号=None, 密码=None):
        if 账号: self.账号 = 账号
        if 密码: self.密码 = 密码
        self.更新token()
        self.获取一级单项列表()
        self.获取二级单项列表()
        self.获取系统单项列表()
        self.生成标签字典()
        # 先获取品牌列表, 再获取机构列表
        self.获取品牌列表()
        self.获取机构列表()
        print('\n实例化完成')
    
    def 更新token(self):
        url = f'{self.domain}/service-scm/login'
        headers = {'Content-Type': 'application/json'}
        data = json.dumps({"account": self.账号, "password": self.密码})
        r = requests.post(url, data=data, headers=headers)
        self.token = r.json()['data']['token']
    
    # 图片库
    图片库 = {
        '中年人': ('ZhongNian1.jpg', 'ZhongNian10.jpg', 'ZhongNian2.jpg', 'ZhongNian3.jpg', 'ZhongNian4.jpg', 'ZhongNian5.jpg', 'ZhongNian6.jpg', 'ZhongNian7.jpg', 'ZhongNian8.jpg', 'ZhongNian9.jpg', 'ZhongNianRen.jpg', 'ZhongNianRen2.jpg', 'ZhongNianRen3.jpg', 'ZhongNianRen4.jpg', 'ZhongNianRen5.jpg'),
        '入职': ('RuZhi.jpg', 'RuZhi10.jpg', 'RuZhi11.jpg', 'RuZhi12.jpg', 'RuZhi13.jpg', 'RuZhi14.jpg', 'RuZhi15.jpg', 'RuZhi2.jpg', 'RuZhi3.jpg', 'RuZhi4.jpg', 'RuZhi5.jpg', 'RuZhi6.jpg', 'RuZhi7.jpg', 'RuZhi8.jpg', 'RuZhi9.jpg'),
        '公务员': ('GongWuYuan.jpg', 'GongWuYuan10.jpg', 'GongWuYuan11.jpg', 'GongWuYuan12.jpg', 'GongWuYuan13.jpg', 'GongWuYuan14.jpg', 'GongWuYuan15.jpg', 'GongWuYuan16.jpg', 'GongWuYuan3.jpg', 'GongWuYuan4.jpg', 'GongWuYuan5.jpg', 'GongWuYuan6.jpg', 'GongWuYuan7.jpg', 'GongWuYuan8.jpg', 'GongWuYuan9.jpg'),
        '女性': ('NvXing.jpg', 'NvXing10.jpg', 'NvXing11.jpg', 'NvXing12.jpg', 'NvXing13.jpg', 'NvXing14.jpg', 'NvXing15.jpg', 'NvXing2.jpg', 'NvXing3.jpg', 'NvXing4.jpg', 'NvXing5.jpg', 'NvXing6.jpg', 'NvXing7.jpg', 'NvXing8.jpg', 'NvXing9.jpg'),
        '孕前': ('YunQian.jpg', 'YunQian10.jpg', 'YunQian11.jpg', 'YunQian12.jpg', 'YunQian13.jpg', 'YunQian14.jpg', 'YunQian15.jpg', 'YunQian16.jpg', 'YunQian2.jpg', 'YunQian3.jpg', 'YunQian4.jpg', 'YunQian5.jpg', 'YunQian6.jpg', 'YunQian7.jpg', 'YunQian8.jpg', 'YunQian9.jpg'),
        '男女通用': ('tongyong1.jpg', 'tongyong2.jpg', 'tongyong3.jpg', 'tongyong4.jpg', 'tongyong5.jpg'),
        '男性': ('NanXing.jpg', 'NanXing10.jpg', 'NanXing11.jpg', 'NanXing12.jpg', 'NanXing13.jpg', 'NanXing2.jpg', 'NanXing3.jpg', 'NanXing4.jpg', 'NanXing5.jpg', 'NanXing6.jpg', 'NanXing7.jpg', 'NanXing8.jpg', 'NanXing9.jpg'),
        '老年人': ('LaoNianRen.jpg', 'LaoNianRen10.jpg', 'LaoNianRen11.jpg', 'LaoNianRen12.jpg', 'LaoNianRen13.jpg', 'LaoNianRen14.jpg', 'LaoNianRen15.jpg', 'LaoNianRen2.jpg', 'LaoNianRen3.jpg', 'LaoNianRen4.jpg', 'LaoNianRen5.jpg', 'LaoNianRen6.jpg', 'LaoNianRen7.jpg', 'LaoNianRen8.jpg', 'LaoNianRen9.jpg'),
        '青少年': ('QingShaoNian.jpg', 'QingShaoNian10.jpg', 'QingShaoNian11.jpg', 'QingShaoNian12.jpg', 'QingShaoNian13.jpg', 'QingShaoNian14.jpg', 'QingShaoNian15.jpg', 'QingShaoNian2.jpg', 'QingShaoNian3.jpg', 'QingShaoNian4.jpg', 'QingShaoNian5.jpg', 'QingShaoNian6.jpg', 'QingShaoNian7.jpg', 'QingShaoNian8.jpg', 'QingShaoNian9.jpg'),
        '青年': ('QingNian.jpg', 'QingNian10.jpg', 'QingNian11.jpg', 'QingNian12.jpg', 'QingNian13.jpg', 'QingNian14.jpg', 'QingNian15.jpg', 'QingNian3.jpg', 'QingNian4 2.jpg', 'QingNian4.jpg', 'QingNian5.jpg', 'QingNian6.jpg', 'QingNian7.jpg', 'QingNian8.jpg', 'QingNian9.jpg')
    }
    
    def picname_get_url(self, picname):
        return f"http://fm.tijian8.com/fms/package/PACKAGE_IMAGE_INVENTORY/{picname}"
    
    def pictype_get_url(self, 类型, 数量=1):
        return [self.picname_get_url(picname=x) for x in sample(self.图片库[类型], 数量)]
    
    # 字段转小写
    大小写字典 = {chr(i): f"_{chr(i+32)}" for i in range(65, 91)}  # {'A': '_a', 'B': '_b', ... 'Z': '_z'}
    要转换的名称 = {}  # 查表法, key:newkey 对应关系
    不转换的名称 = set()  # 查表法, 不需要转换的key
    def 字段转小写(self, item):
        if type(item) is dict:
            for key in list(item.keys()):
                if key not in self.不转换的名称:
                    if key in self.要转换的名称:
                        item[self.要转换的名称[key]] = item.pop(key)
                    else:
                        new_key = re.sub('^_', '', ''.join([self.大小写字典.get(x, x) for x in key]))
                        if new_key == key:
                            self.不转换的名称 |= {key}
                        else:
                            self.要转换的名称[key] = new_key
                            item[new_key] = item.pop(key)
            for value in item.values():
                self.字段转小写(value)
        elif type(item) is list:
            for x in item:
                self.字段转小写(x)
        return item
    
    # 转中文
    中文字典 = {
        'tag_id': '标签id', 'group_name': '组名称', 'tag_code': '标签代号', 'tag_name': '标签名称', 'group_id': '组id',
        'district_name': '地区名称', 'province_name': '省份名称', 'org_picture': '机构图片', 'org_address': '机构地址',
        'org_id': '机构id', 'org_item_id': '机构单项id', 'org_item_name': '机构单项名称', 'org_item_desc': '机构单项描述',
        'mutual_item_id': '统一单项id', 'mutual_item_name': '统一单项名称', 'mutual_item_desc': '统一单项描述',
        'city_name': '城市名称', 'org_status': '机构状态', 'org_name': '机构名称', 'org_phone': '机构电话',
        'basic': '基础', 'parent_id': '父级id', 'description': '描述', 'genders': '性别', 'tag_group': '标签组',
        'package_id': '套餐id', 'package_name': '套餐名称', 'package_price': '套餐价格', 'package_status': '套餐状态',
        'big_picture': '大图', 'small_picture': '小图', 'sales_volume': '销售量', 'tag_item': '标签项目',
        'create_time': '创建时间', 'update_time': '更新时间', 'tag_gender': '标签性别', 'brand_name': '品牌名称',
        'brand_description': '品牌描述', 'brand_province_id': '品牌省份id', 'brand_province_name': '品牌省份名称',
        'brand_city_id': '品牌城市id', 'brand_city_name': '品牌城市名称', 'brand_district_id': '品牌地区id',
        'brand_district_name': '品牌地区名称', 'brand_address': '品牌地址', 'brand_status': '品牌状态',
        'brand_type': '品牌类型', 'brand_id': '品牌id', 'status':'状态', 'system_item_id': '系统单项id',
        'item_group_id': '单项组id', 'system_item_name': '系统单项名称', 'system_item_alias': '系统单项别名',
        'system_item_desc': '系统单项描述', 'system_item_price': '系统单项价格', 'system_item_discount': '系统单项折扣',
        'system_item_code': '系统单项code', 'gender':'性别', 'item_group_name':'单项组名称', 'images': '图片s',
        'system_items': '系统单项s', 'brand_items': '品牌单项s', 'org_items': '机构单项s', 'scm_package':'供应链套餐',
        'package_alias': '套餐别名', 'package_desc': '套餐描述', 'package_original_price': '套餐原价',
        'package_selling_price': '套餐售价', 'package_discount': '套餐折扣', 'package_gender': '套餐性别',
        'sale_num': '销售量', 'package_code':'套餐code', 'item_desc':'单项描述', 'item_name':'单项名称',
        'item_id':'单项id', 'item_price':'单项价格', 'package_item_id':'套餐单项id', 'type_key': '类型key',
        'dict_type_id': '类型id', 'type_id':'类型id', 'type_key':'类型key', 'org_search_url': '机构搜索url',
        'org_province_id': '机构省份id', 'org_district_name': '机构地区名称', 'org_lgt': '机构经度',
        'org_cooperate_mode': '机构合作模式', 'org_code': '机构code', 'channel_type': '渠道类型',
        'channel_alias': '渠道别名', 'channel_name': '渠道名称', 'org_city_name': '机构城市名称',
        'org_city_id': '机构城市id', 'org_settlement_discount': '机构结算折扣', 'business_hour': '营业时间',
        'org_district_id': '机构地区id', 'org_alias': '机构别名', 'org_description': '机构描述', 'org_lat': '机构纬度',
        'org_type': '机构类型', 'org_province_name': '机构省份名称', 'org_channel_id': '机构渠道id',
        'ah_sync_status': '阿里同步状态', 'bh_sync_status': '百度同步状态', 'th_sync_status': '腾讯同步状态',
        'org_publish': '机构公告', 'org_sketch': '机构简介', 'org_level': '机构等级',
        'org_settlement_advice_discount': '机构建议结算折扣', 'channel_sign_type': '渠道签约类型',
        'org_cash_delivery_support': '机构支持到付', 'package_image_id': '套餐图片id',
        'package_image_path': '套餐图片路径', 'package_image_type': '套餐图片类型'
    }
    def 转中文(self, item, 中文字典=None):
        中文字典 = 中文字典 or self.中文字典
        if type(item) is dict:
            keys = list(item)
            newkeys = [中文字典.get(key, key) for key in keys]
            zip_keys_newkeys = zip(keys, newkeys)
            if len(newkeys) == len(set(newkeys)):
                for key, newkey in zip_keys_newkeys:
                    if key != newkey: item[newkey] = item.pop(key)
            else:
                print('newkeys 冲突')
                for x in [k for k, v in dict(Counter(newkeys)).items() if v > 1]:
                    print(f"{x}: {[a for a, b in zip_keys_newkeys if b == x]}")
                raise Exception('newkeys 冲突')
            for value in item.values():
                if type(value) in [list, dict]:
                    self.转中文(value, 中文字典)
        elif type(item) is list:
            for x in item:
                self.转中文(x, 中文字典)
        return item
    
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
            if r['message'] == 'TOKEN生成失败':
                self.更新token()
            else:
                return r
        return r
    
    def post(self, api, data=None, 转中文=True):
        r = self.字段转小写(self.请求服务器(方法='post', api=api, data=data))
        return self.转中文(r) if 转中文 else r

    def get(self, api, params=None, 转中文=True):
        r = self.字段转小写(self.请求服务器(方法='get', api=api, params=params))
        return self.转中文(r) if 转中文 else r
    
    def put(self, api, data=None, 转中文=True):
        r = self.字段转小写(self.请求服务器(方法='put', api=api, data=data))
        return self.转中文(r) if 转中文 else r
    
    def 打印字段(self, data):
        print('\n'.join(f"{x} = ''," for x in set(re.findall(", '([^,]+)': ", str(data)))))
    
    def 获取全部(self, api, params={}):
        params['per'] = 1
        params['per'] = self.get(api, params=params)['total']
        return self.get(api, params=params)['data']
    
    def 构建双通道字典(self, item, 反向=False):
        if 反向: item = {v: k for k, v in item.items()}
        item.update({v: v for v in item.values()})
        print(item)
    
    成功的msg = {
        'OK', '提交的类型名称已存在,请修改后重新提交', '成功', '统一单项名称已存在', 'SUCCESS', 'success',
        '单项类型名称已存在', '系统单项名称已存在'
    }
    
    ''' 已验证的 '''
    
    ''' 已验证 '''
    def 获取一级单项列表(self):
        print('正在获取一级单项列表')
        api = 'system/groups'
        data = self.获取全部(api, params=dict(groupLevel=1))
        self.一级单项字典 = item = {}
        for x in data: item[x['单项组id']] = item[x['单项组名称']] = x
        return data
    
    ''' 已验证 '''
    def 获取二级单项列表(self):
        print('正在获取二级单项列表')
        api = 'system/groups'
        data = self.获取全部(api, params=dict(groupLevel=2))
        self.二级单项字典 = item = {}
        for x in data: item[x['单项组id']] = item[x['单项组名称']] = x
        return data
    
    ''' 已验证 '''
    def 获取系统单项列表(self):
        print('正在获取系统单项列表')
        data = self.获取全部(api='system/system-items')
        self.系统单项字典 = item = {}
        for x in data: item[x['系统单项id']] = item[x['系统单项名称']] = x
        return data
    
    ''' 已验证 '''
    def 新增二级单项(self, 一级单项id, 单项名称, 更新字典=True):
        # 无法和任何一级单项重名, 无法和任何二级单项重名, 可以和统一单项重名
        api = 'system/item-group'
        data = dict(itemGroupName=单项名称, parentId=self.一级单项字典[一级单项id]['单项组id'], sort=101)
        r = self.post(api, data=data)
        msg = r.get('message') or str(r)
        if msg in self.成功的msg:
            if 更新字典: self.获取二级单项列表()
            return True
        else:
            return msg

    ''' 已验证 '''
    def 新增系统单项(self, 二级单项id, 单项名称, 更新字典=True):
        # 可以和二级单项重名, 无法和任何三级单项重名
        api = 'system/system-item'
        data = dict(gender=1, status=0, sort=637, systemItemCode='1',
            itemGroupId = self.二级单项字典[二级单项id]['单项组id'], # 二级单项id
            systemItemName = 单项名称)
        r = self.post(api, data=data)
        msg = r.get('message') or str(r)
        if msg in self.成功的msg:
            if 更新字典: self.获取系统单项列表()
            return True
        else:
            return msg
    
    ''' 已验证 '''
    def 生成标签字典(self):
        print('正在生成标签字典')
        类型s = self.get('system/dict-data/union')['data']
        self.转中文(类型s, {'dict_data_union_v_o_l_v2': '二级标签', 'type_value': '类型名称',
                       'dict_data_id': '标签id','data_key': '标签key', 'data_value': '标签名称'})
        for 类型 in 类型s:
            item = {}
            类型key, 类型名称 = 类型['类型key'], 类型['类型名称']
            for 标签 in 类型['二级标签']:
                标签['类型key'], 标签['类型名称'] = 类型key, 类型名称
                item[标签['标签id']] = item[标签['标签名称']] = 标签
            类型['二级标签'] = item
        self.标签字典 = item = {}
        for 类型 in 类型s: item[类型['类型id']] = item[类型['类型名称']] = 类型
        return item
    
    ''' 已验证 '''
    def 获取品牌列表(self):
        print('正在获取品牌列表')
        data = self.获取全部('system/brands')
        self.品牌字典 = item = {}
        for x in data:
            x['旗下机构'] = {}
            item[x['品牌id']] = item[x['品牌名称']] = x
        return data
    
    ''' 已验证 '''
    def 获取机构列表(self):
        print('正在获取机构列表')
        data = self.获取全部('org/organization/list')
        data = self.转中文(data, {'org_busline': '机构交通线路', 'org_customize_support': '机构支持自定义套餐',
                               'org_notice': '机构预约须知'})
        self.机构字典 = item = {}
        for x in data:
            品牌id, 机构id, 机构名称 = x['品牌id'], x['机构id'], x['机构名称']
            item[机构id] = item[机构名称] = x
            if 品牌id in self.品牌字典:
                品牌旗下机构 = self.品牌字典[品牌id]['旗下机构']
                品牌旗下机构[机构id] = 品牌旗下机构[机构名称] = x
        return data
    
    ''' 已验证 '''
    def 获取套餐详情(self, 套餐id):
        data = self.get('package', params=dict(packageId=套餐id))['data']
        self.转中文(data, {
            'organizations':'挂靠机构', 'attributes':'标签','item_b_o':'单项', 'package_presettle_price':'套餐预估结算价',
            'item_group_lv1_id':'一级单项id','item_group_lv2_id':'二级单项id', 'type_value':'类型名称',
            'data_id':'标签id', 'data_key':'标签key', 'data_value':'标签名称', '套餐性别': '性别和婚否'
        })
        return data
    
    ''' api列表 '''

    def 判断是否请求成功(self, r):
        msg = r.get('message') or str(r)
        return True if msg in self.成功的msg else msg
    

    
    def 判断数据完整性(self, s):
        for i, x in enumerate(s.fillna('')):
            if type(x) is str:
                if not x.replace(' ', ''):
                    print(f"[{s.name}] 第 {i + 2} 行为空值")
                    raise Exception(f"[{s.name}] 第 {i + 2} 行为空值")
        return True
    
    def 从excel提取系统单项(self, path):
        # 确定字段
        字段s = dict(一级 = '一级', 二级 = '二级', 三级 = '三级')
        zd = pd.Series(字段s)
        # 读取excel
        df = pd.read_excel(path)
        for c in (zd.一级, zd.二级, zd.三级): self.判断数据完整性(df[c])
        # 判断统一单项是否重复
        单项s = df[zd.三级]
        if len(单项s) != len(set(单项s)):
            print('以下三级单项重复:')
            print([k for k, v in dict(Counter(单项s)).items() if v > 1])
            raise Exception('三级单项重复')
        # 读取单项
        需创建的二级单项 = []
        需创建的三级单项 = []
        for h in df.to_dict('records'):
            一级, 二级, 三级 = h[zd.一级], h[zd.二级], h[zd.三级]
            if 一级 not in self.一级单项字典: raise Exception(f"一级单项 [{一级}] 不存在")
            if 二级 not in self.二级单项字典:
                需创建的二级单项.append((一级, 二级))
            if 三级 not in self.系统单项字典:
                需创建的三级单项.append((二级, 三级))
        if 需创建的二级单项:
            print('\n将创建以下 二级单项:')
            for x in 需创建的二级单项: print(list(x))
        if 需创建的三级单项:
            print('\n将创建以下 三级单项:')
            for x in 需创建的三级单项: print(list(x))
        return 需创建的二级单项, 需创建的三级单项

    def 机构id_get_套餐列表(self, 机构id, 去除test=False):
        机构id = self.机构字典[机构id]['机构id']
        data = dict(orgId=机构id, per=1)
        r = self.get('packages', params=data)
        data['per'] = r['total']
        r = self.get('packages', params=data)['data']
        if 去除test:
            r = [x for x in r if not [y for y in ('test', '测试') if y in x['套餐名称'].lower()]]
        return r

    def 修改套餐(self, 套餐id, 套餐详情=None, **kvs):
        # kvs: 标签s, 图片s, 单项s, 机构ids, 折扣, 性别和婚否, 套餐名称, 原价, 售价, 预估结算价, 上架
        详情 = 套餐详情 or self.获取套餐详情(套餐id=套餐id)
        套餐 = 详情['供应链套餐']
        单项来源字典 = {'系统库': 1, '品牌库': 2, '机构库': 3, 1: 1, 2: 2, 3: 3}
        性别和婚否字典 = {'男': 1, '女': 2, '已婚女': 3, '未婚女': 4, '通用': 5, 1: 1, 2: 2, 3: 3, 4: 4, 5: 5}
        上架字典 = {0:0, 1:1, True:1, False:0, '是':1, '否':0}

        图片s = kvs.get('图片s')
        if 图片s: 图片s = [dict(packageImagePath=url, packageImageType=type_) for url, type_ in 图片s]
        else: 图片s = [dict(packageImagePath=x['套餐图片路径'], packageImageType=x['套餐图片类型']) for x in 详情['图片s']]

        单项s = kvs.get('单项s')
        if 单项s: 单项s = [dict(itemId=单项id, source=单项来源字典[来源]) for 单项id, 来源 in 单项s]
        else:
            if (详情['单项']['品牌单项s'] or 详情['单项']['机构单项s']):
                raise Exception('修改套餐 方法需要增加对 品牌单项 和 机构单项 的支持')
            else:
                单项s = [dict(itemId=x['单项id'], source=x['source']) for x in 详情['单项']['系统单项s']]
        newdata = dict(
            packageId = 套餐id,
            attributes = [dict(dictDataKey=s['标签key'], dictDataValue=s['标签名称'], dictTypeId=s['类型id']) for s in kvs.get('标签s', 详情['标签'])],
            images = 图片s,
            items = 单项s,
            orgIds = kvs.get('机构ids', [x['机构id'] for x in 详情['挂靠机构']]),
            packageName = kvs.get('套餐名称', 详情['供应链套餐']['套餐名称']),
            packageAlias = kvs.get('套餐名称', 套餐['套餐别名'] or 套餐['套餐名称']),
            packageDiscount = kvs.get('折扣', 套餐['套餐折扣']),
            packageGender = 性别和婚否字典[kvs.get('性别和婚否', 套餐['性别和婚否'])],
            packageOriginalPrice = kvs.get('原价', 套餐['套餐原价']),
            packageSellingPrice = kvs.get('售价', 套餐['套餐售价']),
            packagePresettlePrice = kvs.get('预估结算价', 套餐['套餐预估结算价']),
            saleNum = 套餐['销售量'] or 0,
            status = 上架字典[kvs.get('上架', 套餐['状态'])],
        )
        r = self.put('package', data=newdata)
        msg = r.get('message') or str(r)
        print(msg)
        return True if msg in self.成功的msg else msg
    
    def 新增套餐(self, 标签s, 图片s, 单项s, 机构ids, 折扣, 性别和婚否, 套餐名称, 原价, 售价, 预估结算价, 上架):
        单项来源字典 = {'系统库': 1, '品牌库': 2, '机构库': 3, 1: 1, 2: 2, 3: 3}
        性别和婚否字典 = {'男': 1, '女': 2, '已婚女': 3, '未婚女': 4, '通用': 5, 1: 1, 2: 2, 3: 3, 4: 4, 5: 5}
        上架字典 = {0:0, 1:1, True:1, False:0, '是':1, '否':0}
        data = dict(
            attributes = [dict(dictDataKey=s['标签key'], dictDataValue=s['标签名称'], dictTypeId=s['类型id']) for s in 标签s],
            images = [dict(packageImagePath=url, packageImageType=type_) for url, type_ in 图片s],
            items = [dict(itemId=单项id, source=单项来源字典[来源]) for 单项id, 来源 in 单项s],
            orgIds = 机构ids,
            packageAlias = 套餐名称,
            packageDiscount = 折扣,  # 0-10实数
            packageGender = 性别和婚否字典[性别和婚否],
            packageName = 套餐名称,
            packageOriginalPrice = 原价,  # 单位: 分
            packageSellingPrice = 售价,  # 单位: 分
            packagePresettlePrice = 预估结算价,  # 单位: 分
            saleNum = 0,
            status = 上架字典[上架]
        )
        r = self.post('package', data=data)
        msg = r.get('message') or str(r)
        print(msg)
        return True if msg in self.成功的msg else msg
    
    def 提取唯一值(self, s):
        name = s.name
        s = set(s)
        if len(s) != 1: raise Exception(f"{name} - 值不唯一: {s}")
        return list(s)[0]
    
    def text_get_类型标签(self, text, 规则=None):
        text = text.lower()
        规则 = 规则 or {
            '婚前孕前体检': ['婚', '孕', '优生', '超'],
            '入职体检': ['入职', '招工', '员工'],
            '父母体检': ['父母', '夕阳', '老', '爸妈', '感恩', '银发', '天伦'],
            '白领体检': ['白领', '职场', '商务', '精英', '都市'],
            '儿童体检': ['儿童', '少年', '宝宝', '婴儿'],
            '证件体检': ['证件', '执照'],
            '专项体检': ['专项', '糖尿', '瘦', '胖', '心', '脑', '肿瘤', '免疫', '基因', '镜', '血', '亚健康'],
            '深度体检': ['深度', '贵宾', 'vip'],
            '女性体检': ['女', '妈', '母', '奶奶'],
            '男性体检': ['男', '爸', '父', '爷爷'],
            '特惠体检': ['特惠', '经济', '优惠', '特价']
        }
        return set(k for k, v in 规则.items() for x in v if x in text)
    
    def text_get_单项标签(self, text, 规则=None):
        text = text.lower()
        规则 = 规则 or {
            '外科': ['外科'],
            '肝功能': ['肝功'],
            '糖尿病': ['糖尿'],
            '眼科': ['眼'],
            '基因检测': ['基因'],
            '肿瘤筛查': ['肿瘤和癌'],
            '胃镜': ['胃镜'],
            '肠镜': ['肠镜'],
            '心肌功能': ['心肌'],
            '肾功能': ['肾功'],
            '甲状腺功能': ['甲功']
        }
        return set(k for k, v in 规则.items() for x in v if x in text)
    
    def text_get_性别和婚否(self, text):
        if ('男' in text) and ('女' in text): return '通用'
        elif '男' in text: return '男'
        elif '女' in text:
            if '已婚' in text: return '已婚女'
            elif '未婚' in text: return '未婚女'
            else: return '女'
        else: raise Exception(f"性别和婚否只支持[通用, 男, 女, 未婚女, 已婚女], 不支持[{text}]")
    
    def 从excel提取套餐(self, path, 上架, 智能匹配标签,
        机构名称,唯一识别,套餐名称,单项,原价,预估结算价,套餐折扣,图片,性别和婚否):

        # 构建容易取值的字典, 用 zd.机构名称 取代 zd['机构名称']
        zd = pd.Series(dict(
            机构名称=机构名称, 唯一识别=唯一识别, 套餐名称=套餐名称, 单项=单项, 原价=原价,
            预估结算价=预估结算价, 套餐折扣=套餐折扣, 图片=图片, 性别和婚否=性别和婚否
        ))

        # 读取excel
        df = pd.read_excel(path)
        for x in (zd): self.判断数据完整性(df[x])
        for x in 智能匹配标签:
            for y in x['匹配excel字段']: self.判断数据完整性(df[y])

        # 输入单项名称, 返回单项
        def get_dx(name):
            dx = self.系统单项字典.get(name)
            if dx: return dx['系统单项id']
            print(f"单项不存在: [{name}]")
            raise Exception(f"单项不存在: [{name}]")
        
        # 输入标签名称, 返回标签
        def get_tag(分类名称, 标签名称):
            分类 = self.标签字典.get(分类名称)
            if not 分类:
                print(f"标签类型[{分类名称}]不存在")
                raise Exception(f"标签类型[{分类名称}]不存在")
            标签 = 分类['二级标签'].get(标签名称)
            if not 标签:
                print(f"标签类型[{分类名称}]下不存在[{标签名称}]")
                raise Exception(f"标签类型[{分类名称}]下不存在[{标签名称}]")
            return 标签

        分隔符 = '__分隔符__'
        旧分隔符s = ('|', '[SEP]', '[SEG]')

        # 生成套餐
        机构名称 = self.提取唯一值(s=df[zd.机构名称])
        机构id = self.机构字典[机构名称]['机构id']
        上架 = {0:0, 1:1, True:1, False:0, '是':1, '否':0}[上架]
        套餐s = {}

        for 唯一识别, df in df.groupby(zd.唯一识别):

            # 匹配各类标签
            所有标签 = []
            for 标签块 in 智能匹配标签:
                标签分类 = 标签块['网页后台标签分类']
                text = '_'.join(set(y for x in 标签块['匹配excel字段'] for y in set(df[x])))
                text = text.lower()
                tags = set(k for k, v in 标签块['匹配规则'].items() for x in v if x.lower() in text)
                tags = [get_tag(标签分类, x) for x in tags]
                if (not tags) and (标签块['是否必填'] != '否'):
                    raise Exception(f"{唯一识别} - [{标签分类}]下 - 未匹配到任何标签")
                所有标签 += tags

            图片url = self.pictype_get_url(类型=self.提取唯一值(s=df[zd.图片]), 数量=1)[0]
            # 折扣
            折扣 = self.提取唯一值(s=df[zd.套餐折扣])
            if not 0 <= 折扣 <= 10: raise Exception("套餐折扣范围: 0-10")
            # 原价 和 售价
            原价 = self.提取唯一值(s=df[zd.原价]) * 100
            售价 = 原价 * 折扣 / 10
            # 单项
            单项s = 分隔符.join(set(df[zd.单项]))
            for x in 旧分隔符s: 单项s = 单项s.replace(x, 分隔符)
            单项s = re.sub('^ +', '', 单项s)  # 去除开头空格
            单项s = re.sub(' +$', '', 单项s)  # 去除末尾空格
            单项s = set(re.split(f' *{分隔符} *', 单项s))
            单项s = [(单项id, '系统库') for 单项id in set(get_dx(x) for x in 单项s)]
            # data
            套餐s[唯一识别] = dict(
                机构ids = [机构id],
                套餐名称 = self.提取唯一值(s=df[zd.套餐名称]),
                上架 = 上架,
                原价 = 原价,
                售价 = 售价,
                预估结算价 = self.提取唯一值(s=df[zd.预估结算价]) * 100,
                图片s = [(图片url, type_) for type_ in (1, 2, 3, 4)],
                折扣 = 折扣,
                性别和婚否 = self.text_get_性别和婚否(text=self.提取唯一值(s=df[zd.性别和婚否])),
                单项s = 单项s,
                标签s = 所有标签
            )
        return 套餐s
