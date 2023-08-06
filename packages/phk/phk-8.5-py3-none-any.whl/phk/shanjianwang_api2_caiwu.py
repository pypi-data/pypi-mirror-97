# -!- coding: utf-8 -!-
import re, os, sys, requests, json, math, time, copy, random, traceback
import pandas as pd
from math import ceil
from .data_set import 数据集

全国城市字典 = 数据集.全国城市.获取城市字典()

class 善检网api第2版_财务():
    domain = 'https://mc.tijian8.com'
    账号, 密码 = '', ''
    
    def __init__(self, 账号=None, 密码=None):
        if 账号: self.账号 = 账号
        if 密码: self.密码 = 密码
        self.更新token()
        self.初始化()
    
    def 初始化(self):
        self.字段清单 = [
            ('oid', 'oid', 'oid'),
            ('sql_state', 'sql_state', 'sql_state'),

            ('城市', 'city', 'city'),
            ('城市', 'city', 'cityName'),
            ('csid', 'csid', 'csid'),
            ('医院', 'hospital', 'hospitalName'),
            ('医院', 'hospital', 'bookingMerchant'),
            ('医院简称', 'hospital_jc', None),
            
            ('esid', 'esid', 'esid'),
            ('机构', 'org', 'bookingMEC'),
            ('机构', 'org', 'orgName'),
            ('机构类型', 'org_type', 'orgType'),
            ('机构类型', 'org_type', 'typeName'),

            ('用户名', 'user_account', 'customerAct'),
            ('下单时间', 'order_time', 'orderTime'),
            ('订单来源', 'order_origin', 'orderOrigin'),
            ('订单类型', 'order_type', 'orderType'),

            ('支付状态', 'pay_status', 'payStatus'),
            ('支付状态', 'pay_status', 'orderStatus'),
            ('支付方式', 'pay_type', 'payType'),
            ('认领状态', 'claim_status', 'claimStatus'),
            ('认领客服', 'kefu', 'claimName'),
            ('订单原价', 'origin_price', 'originPrice'),
            ('订单金额', 'order_price', 'orderPrice'),
            ('订单实付款', 'payed_price', 'payedPrice'),
            ('订单合同结算价', 'order_contract_settlement', 'contractSettlementPrice'),
            ('订单结算价', 'order_settlement', 'actSettlementPrice'),
            ('订单结算价', 'order_settlement', 'settlementPrice'),
            ('订单利润', 'order_profit', None),
            ('订单合同结算时间', 'contract_settlement_time', 'contractSettlementTime'),
            ('订单结算完成时间', 'finally_settlement_time', 'finallySettlementTime'),

            ('rid', 'rid', 'rid'),
            ('年龄', 'age', 'bookingAge'),
            ('性别', 'gender', 'bookingGender'),
            ('套餐名称', 'goods_name', 'bookingGoods'),
            ('套餐原价', 'goods_origin_price', 'goodsOriginPrice'),
            ('套餐售价', 'goods_sale_price', 'goodsSalePrice'),
            ('套餐结算价', 'goods_settlement_price', 'goods_settlement_price'),
            ('套餐利润', 'goods_profit', None),
            ('预约状态', 'booking_status', 'bookingStatus'),
            ('预估结算价', 'predict_settlement', 'presettlePrice'),
            ('预估利润', 'predict_profit', None) 
        ]

        self.字段中文清单 = list(set([a for a,b,c in self.字段清单]))

        self.字段字典 = {b: str(dict(zip(['中文', '数据库', 'api'], a))) for a in self.字段清单 for b in a}

        self.代号值字典 = dict(
            订单类型 = {2:'普通订单', 5:'大型检查订单', 6:'简版商城订单', 100:'线下订单'},
            订单来源 = {1:'PC', 2:'WAP', 3:'小程序', 5:'线下'},
            支付状态 = {0:'未付款', 2:'已付款', 3:'待退款', 4:'已退款', 5:'部分退款'},
            认领状态 = {0:'未认领', 1:'已认领'},
            支付方式 = {1:'微信支付', 2:'支付宝WAP', 3:'威付通微信', 4:'威付通支付宝', 5:'威付通银联', 6:'支付宝PC'},
            预约状态 = {0:'审核中', 1:'审核通过', 2:'审核驳回', 3:'体检完成', 4:'取消预约', 5:'大型体检未支付', 6:'已结算',
                   7:'申请结算', 8:'已预付', 9:'申请预付'}
        )
    
    def 转为中文(self, item):
        if type(item) is dict:
            for a, c in [(a,c) for a,b,c in self.字段清单 if c in item]:
                item[a] = item.pop(c)
            for key, item_b in self.代号值字典.items():
                if key in item:
                    value = item[key]
                    if value in item_b:
                        item[key] = item_b[value]
        return item

    def 保留小数(self, item, n):
        for k,v in item.items():
            if type(v) is float:
                item[k] = round(v, n)
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
    
    def 查询订单列表(self, params=None):
        api = "finance/orders"
        p = params.copy()
        p['per'] = 1
        r = self.请求服务器('get', api, params=p)
        kws = []
        p['per'] = min(1000, r['total'])
        pagetotal = ceil(r['total'] / 1000)
        for page in range(1, pagetotal + 1):
            print(f"\r查询订单列表 第 {page}/{pagetotal} 页", end='    ')
            p['page'] = page
            for data in self.请求服务器('get', api, params=p)['data']:
                self.转为中文(data)
                try: data['订单利润'] = data['订单实付款'] - data['订单结算价']
                except: data['订单利润'] = None
                self.保留小数(data, 2)
                kws.append(data)
        return kws

    def 查询订单详情(self, params):
        api = 'finance/order-detail'
        for n in range(30):  # 重试15次
            try:
                r = self.请求服务器('get', api, params=params)
                break
            except Exception as err:
                e = err
                if 'Max retries exceeded with url' in str(e): time.sleep(1)
                else: raise e
        else: raise e
        data = r['data']
        self.转为中文(data)
        data.pop('订单结算价')
        for item in data['bookingInformation']:
            item['goods_settlement_price'] = item.pop('settlementPrice')
            self.转为中文(item)
            try: item['预估利润'] = item['套餐售价'] - item['预估结算价']
            except: pass
            try: item['套餐利润'] = item['预估利润'] = item['套餐售价'] - item['套餐结算价']
            except: pass
            try: item['性别'] = '女' if int(item['bookingIdcard'][16]) % 2 == 0 else '男'
            except: item['性别'] = '未知'
            self.保留小数(item, 2)
        self.保留小数(data, 2)
        return r
    
    def 获取商务机构信息(self, params={}):  # 没问题
        api = 'commercial/hospital-list'
        params['per'] = self.请求服务器('get', api, params=params)['total']
        r = self.请求服务器('get', api, params=params)
        data = r['data']
        item = {
            'businessDirector': '商务负责人',
            'channel': '渠道类型',
             'holdName': '商务录入人',
             'operateTime': '操作时间',
             'settlementDiscount': '结算折扣',
             'mecname': '机构名称',
             'settlementPeriod': '结算周期',
             'meclevel': '机构等级',
             'mecstatus': '机构状态',
            'provinceName': '省', 'cityName': '市', 'areaName': '区',
            'notice':'备注'
        }

        机构等级 = {'glsj':'公立三甲', 'glyy':'公立医院', 'mysj':'民营三级', 'myyy':'民营医院', 'sjjd':'民营三甲', 'zyjg':'专业机构'}
        机构状态 = {0:'未审核' , 1:'审核通过合作中' , 2:'暂停' ,3:'驳回' ,4:'逻辑删除'}
        渠道类型 = {1:'直签-机构', 2:'直签-个人', 3:'第三方-公司' ,4:'第三方-个人'}
        df = pd.DataFrame(data).rename(columns=item)
        df['机构等级'] = df.机构等级.apply(lambda x: 机构等级.get(x, x))
        df['机构状态'] = df.机构状态.apply(lambda x: 机构状态.get(x, x))
        df['渠道类型'] = df.渠道类型.fillna('-')
        df['渠道类型'] = df.渠道类型.apply(lambda x: 渠道类型.get(x, x).split('-'))
        df['渠道1'] = df.渠道类型.apply(lambda x:x[0])
        df['渠道2'] = df.渠道类型.apply(lambda x:x[-1])
        df['城市等级'] = df.市.apply(lambda x: 全国城市字典.get(x, {}).get('等级', 6))
        df.drop('渠道类型', axis=1, inplace=True)
        df = df[~df['机构名称'].str.contains('test|测试')]
        
        品牌s = ['美亚', '美年', '中信健康', '艾诺', '福华', '慈铭', '新华', '民流健康', '美兆', '中信', '普惠', '国药阳光', '新华体检', '民众', '艾博', '熙康', '第一健康', '仁泰', '爱康', '瑞慈', 'PET', '医院']
        品牌s = '|'.join(set(品牌s))
        df['品牌'] = df.机构名称.apply(lambda x: (re.findall(品牌s, x) or ['其它'])[0])

        return df

    
    def 获取机构套餐(self, esid):
        api = 'util/hospital-products'
        r = self.请求服务器('get', api, params=dict(esid=esid))
        return r['data']
    
    def 获取省市区(self, 行政级别, 有机构有套餐=False):
        api = 'util/address'
        params = dict(dataType=行政级别, bizType= 2 if 有机构有套餐 else 1)
        r = self.请求服务器('get', api, params=params)
        for x in r['data']:
            x['行政级别'] = 行政级别
        return r['data']
    
    def 获取区域下的机构(self, 行政级别, 地区编号):
        api = 'util/address-hospitals'
        params = dict(dataType=行政级别, bizId=地区编号)
        r = self.请求服务器('get', api, params=params)
        return r['data']
    
    def 获取区号字典(self, key='区号'):  # key: 区号, 城市, 双向
        headers = {"User-Agent": "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/65.0.3325.146 Safari/537.36"}
        r = requests.get('https://www.tijian8.com/', timeout=30, headers=headers)
        quhaos = list(set(re.findall('<li ><a href="/(\d*)">(.*)</a></li>', r.text)))
        if key == '区号': return {a:b for a,b in quhaos}
        elif key == '城市': return {b:a for a,b in quhaos}
        elif key == '双向': return {x:y for a,b in quhaos for x,y in ((a,b), (b,a))}

    def 获取全部机构(self):
        orgs = self.获取区域下的机构(行政级别=None, 地区编号=None)
        orgs = [x for x in orgs if 'test' not in x['name']]
        城市字典 = {x['id']:x['title'] for x in self.获取省市区(2)}
        区号字典 = self.获取区号字典(key='城市')
        for x in orgs:
            x['city'] = city = 城市字典[x['city']]
            x['city_b'] = city = city.replace('市', '')
            x['区号'] = 区号字典.get(city)
        return orgs
