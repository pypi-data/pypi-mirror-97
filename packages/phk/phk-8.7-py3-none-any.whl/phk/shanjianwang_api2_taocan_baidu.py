# -!- coding: utf-8 -!-
import re, os, sys, requests, json, math, time, copy, random, pickle
import pandas as pd
from collections import Counter
from copy import deepcopy
from .shanjianwang_api2_taocan import 善检网api第2版_套餐

'''
服务id与套餐id的区别:
新增服务基础时, 从已有的套餐中选择n个套餐, 服务器会自动生成n个服务id, 并与套餐id关联.
即: 1个套餐可以在多个服务基础包中存在, 套餐可复用
'''

class 善检网api第2版_套餐_百度(善检网api第2版_套餐):

    def __init__(self):
        善检网api第2版_套餐.__init__(self)
        print('百度套餐接口')
        self.获取机构列表()
        self.获取品牌列表()
        self.获取统一单项列表()
        self.获取标签字典()
        self.生成一级单项字典()
        self.生成二级单项字典()
        print('实例化完成')
    
    中文字典 = dict(
        tag_id='标签id', group_name='组名称', tag_code='标签代号', tag_name='标签名称', group_id='组id',
        district_name='区', province_name='省份', org_picture='机构图片', org_address='机构地址',
        org_id='机构id', org_item_id='机构单项id', org_item_name='机构单项名称', org_item_desc='机构单项描述',
        mutual_item_id='统一单项id', mutual_item_name='统一单项名称', mutual_item_desc='统一单项描述',
        city_name='城市', org_level='机构等级', org_rank='机构排名', org_status='机构状态', org_name='机构名称',
        basic = '基础', parent_id = '父级id', description = '描述', genders = '性别',
        package_id = '套餐id', package_name = '套餐名称', package_price = '套餐价格', package_status = '套餐状态',
        big_picture = '大图', small_picture = '小图', sales_volume = '销售量', tag_item = '标签项目',
        create_time = '创建时间', update_time = '更新时间', tag_gender = '标签性别', tag_group = '标签组',
        packages = '套餐s', city_id='城市id', province_id='省份id', district_id='区域id',
        service_id='服务id', brand_id='品牌id', service_list='服务列表', title_name='标题名称',
        org_video='机构视频', org_lgt='机构经度', org_lat='机构纬度', org_work_time='机构工作时间',
        org_tel='机构电话', org_logo='机构logo', org_certify_d_t_o='机构认证内容',
        item_group_id = '项目组id', item_group_name = '项目组名称', delay='延迟',
        org_limit='机构限制', suspend_time='暂停时间'
    )
    

    

    
    '''验证通过'''
    def 名称标准化(self, name, 小写=False):
        name = re.sub('\s', '', name)  # 去除空白字符
        name = name.replace('（', '(').replace('）', ')')  # 括号统一
        if 小写:
            name = name.lower()
        return name
    
    '''验证通过'''
    def 获取品牌列表(self):
        print('正在获取品牌列表')
        品牌列表 = self.get("org/bh-brand/brands-all", params=None)['data']
        if '获取品牌字典':
            self.品牌字典 = 品牌字典 = {x['品牌id']: x for x in 品牌列表}
            品牌字典.update({x['brand_name']: x for x in 品牌列表})
        return 品牌列表
    
    
    '''验证通过'''
    def 获取品牌详情(self, 品牌id):
        params = dict(brandId=品牌id)
        return self.get("org/bh-brand/brand", params=params)['data']
    
    def 获取服务基础列表(self):
        params = dict(per=1)
        params['per'] = self.get("svc/bh-service/services", params=params)['total']
        return self.get("svc/bh-service/services", params=params)['data']
    
    '''验证通过'''
    def 获取套餐详情(self, 套餐id):
        params = dict(packageId=套餐id)
        return self.get("product/bh-package/package", params=params)['data']

    def 获取服务基础详情(self, 服务基础id):
        params = dict(serviceId=服务基础id)
        return self.get("svc/bh-service/service", params=params)['data']
    
    '''验证通过'''
    def 获取机构列表(self):
        print('正在获取机构列表')
        params = dict(per=1)
        params['per'] = self.get("baidu/org/list", params=params)['total']
        机构列表 = self.get("baidu/org/list", params=params)['data']
        if '生成机构概况字典':
            df = pd.DataFrame(机构列表)
            df['完整地址'] = df.省份 + df.城市 + df.区 + df.address
            f = lambda x: not(('暂无' in x.完整地址) or (x.省份id == 0) or (x.城市id == 0) or (x.区域id == 0))
            df['地址完整性'] = df.apply(f, axis=1)
            orgs = df = df.to_dict(orient='reocde')
            self.机构概况字典 = 机构概况字典 = {x['机构名称']: x for x in orgs}
            机构概况字典.update({x['机构id']: x for x in orgs})
        return 机构列表
    
    '''验证通过'''
    def 获取机构套餐列表(self, 机构id, 去除test=False):
        params = dict(orgId=机构id)
        datas = self.get("product/bh-package/packageByorgId", params=params)['data']
        if 去除test:
            datas = [x for x in datas if 'test' not in x['套餐名称'].lower() and '测试' not in x['套餐名称']]
        return datas
    

    
    '''验证通过'''
    def 新增服务基础(self, 机构id, 服务名称, 套餐ids):
        org = self.机构概况字典[机构id]
        机构id = org['机构id']
        if org['地址完整性']:
            params = dict(
                cityId = org['城市id'],
                cityName = org['城市'],
                districtId = org['区域id'],
                districtName = org['区'],
                orgId = 机构id,
                packages = 套餐ids,
                provinceId = org['省份id'],
                provinceName = org['省份'],
                titleName = 服务名称,
            )
            r = self.post("svc/bh-service/service", data=params)
            if r['message'] in ('SUCCESS', ):
                return r['data']
            else:
                r = f"{机构id} - {org['机构名称']} - {服务名称} - {r}"
        else:
            r = f"{机构id} - {org['机构名称']} - 地址不完整"
        print(r)
        return r

    
    '''验证通过'''
    def 修改服务基础(self, 机构id=None, 服务名称=None, 套餐ids=None, 服务基础id=None):
        olddata = self.获取服务基础详情(服务基础id)
        机构id = 机构id or olddata['机构id']
        服务名称 = 服务名称 or olddata['标题名称']
        if 套餐ids is None:
            套餐ids = list(set(x['套餐id'] for x in olddata['套餐s']))

        org = self.机构概况字典[机构id]
        机构id = org['机构id']
        if org['地址完整性']:
            params = dict(
                cityId = org['城市id'],
                cityName = org['城市'],
                districtId = org['区域id'],
                districtName = org['区'],
                orgId = 机构id,
                packages = 套餐ids,
                provinceId = org['省份id'],
                provinceName = org['省份'],
                serviceId = 服务基础id,
                titleName = 服务名称,
            )
            r = self.put("svc/bh-service/service", data=params)
            if r['message'] in ('SUCCESS', ):
                return r['data']
            else:
                r = f"{机构id} - {org['机构名称']} - {服务名称} - {r}"
        else:
            r = f"{机构id} - {org['机构名称']} - 地址不完整"
        print(r)
        return r
    


    def 获取全部(self, api, params={}):
        params['per'] = 1
        params['per'] = self.get(api, params=params)['total']
        return self.get(api, params=params)['data']

    def 获取品牌服务列表(self, 品牌id):
        品牌id = self.品牌字典[品牌id]['品牌id']
        data = self.获取全部('svc/bh-service/services/relation', dict(bizType=3, bizField=品牌id))
        for x in data: x['品牌id'] = int(x['品牌id'])
        data = [x for x in data if x['品牌id'] == 品牌id]
        return data

    def 服务上下架(self, 套餐id, 服务id, 状态):
        状态字典 = {'下架':3, 3:3, '上架':1, 1:1}
        data = dict(packageId=套餐id, serviceId=服务id, status=状态字典[状态])  # 服务状态，枚举值：1=>有服务、2=>无服务、3=>已下架、4=>隐藏不展现
        r = self.put("svc/bh-service/service/status", data=data)
        if r['message'] in ('SUCCESS', ):
            return True
        else:
            print(r)
            return r

    def 获取机构排期默认策略(self, 机构id):
        机构id = self.机构概况字典[机构id]['机构id']
        data = self.get('baidu/org/default-schedule', params=dict(orgId=机构id))['data']
        for x, y in [('延迟', '延迟天数'), ('机构限制', '预约上限')]:
            data[y] = data.pop(x)
        return data

    def 新增机构排期默认策略(self, 机构id, 延迟天数=None, 预约上限=None, 暂停时间=None):
        data = dict(delay = 延迟天数, orgId=机构id, orgLimit=预约上限, suspendTime=暂停时间)
        data = dict(delay = 延迟天数, orgId=机构id, orgLimit=预约上限, suspendTime=暂停时间)
        r = self.post("baidu/org/default-schedule", data=data)
        if r['message'] in ('SUCCESS', ):
            return True
        else:
            r = dict(机构id=机构id, r=r)
            print(r)
            return r

    def 修改机构排期默认策略(self, 机构id, 延迟天数=None, 预约上限=None, 暂停时间=None):
        机构id = self.机构概况字典[机构id]['机构id']
        olddata = self.获取机构排期默认策略(机构id=机构id)
        if 延迟天数 is None: 延迟天数 = olddata['延迟天数']
        if 预约上限 is None: 预约上限 = olddata['预约上限']
        if 暂停时间 is None: 暂停时间 = olddata['暂停时间']
        data = dict(delay = 延迟天数, orgId=机构id, orgLimit=预约上限, suspendTime=暂停时间)
        r = self.put("baidu/org/default-schedule", data=data)
        if r['message'] in ('SUCCESS', ):
            return True
        else:
            r = dict(机构id=机构id, r=r)
            print(r)
            return r

    def 生成机构商用中服务基础字典(self):
        # print('正在生成机构商用中服务基础字典')
        jiius = self.获取服务基础列表()
        item = {}
        jiius = [x for x in jiius if not [y for y in ('暂停使用', 'test', '测试') if y in x['标题名称']]]
        for x in jiius:
            lis = item.setdefault(x['机构id'], [])
            lis.append(x)
        return item

    '''验证通过'''
    def 获取机构服务基础字典(self, 机构id, key='id', 套餐s=None):
        机构id = self.机构概况字典[机构id]['机构id']
        套餐s = 套餐s or self.获取机构套餐列表(机构id=机构id)  # 所有套餐
        服务基础s = [服务基础 for 套餐 in 套餐s for 服务基础 in 套餐['服务列表']]
        服务基础s = [x for x in 服务基础s if '暂停使用' not in x['标题名称']]
        if key == 'id':
            item = {x['服务id']: x for x in 服务基础s if x['机构id'] == 机构id}
        elif key == '名称':
            item = {x['标题名称']: x for x in 服务基础s if x['机构id'] == 机构id}
        else:
            item = {x['服务id']: x for x in 服务基础s if x['机构id'] == 机构id}
            item.update({x['标题名称']: x for x in item.values()})
        return item

    '''验证通过'''
    def 机构增量生成服务基础(self, 机构id):
        org = self.机构概况字典[机构id]
        机构id, 机构名称 = org['机构id'], org['机构名称']
        成功, 失败 = {}, {}
        处理结果 = dict(机构id=机构id, 机构名称=机构名称, data=dict(成功=成功, 失败=失败))
        if org['地址完整性']:
            基础ids = self.生成机构商用中服务基础字典().get(机构id) or []
            基础ids = list(set([(x['服务id'], x['标题名称']) for x in 基础ids]))
            name_id = {y: x for x, y in 基础ids}
            item = {}
            jua = {}
            for jid, jname in 基础ids:
                if jname in jua: raise Exception(f"机构[{机构id}] 存在同名的服务基础, {jname}:[{jid}, {jua['jname']}]")
                else: jua[jname] = jid
                lis = item[jname] = []
                for x in self.获取服务基础详情(jid)['套餐s']:
                    lis.append(x['套餐id'])
            # item  {'基础套餐(常规检查)(癌胚抗原定量(CEA))-男': [1882, 1883, 1884, 1885, 1886, 1887, 1888, 1889]}
            需更新 = set()
            需新增 = set()
            for t in self.获取机构套餐列表(机构id=机构id, 去除test=True):
                tid, tname = t['套餐id'], t['套餐名称']
                lis = item.setdefault(tname, [])
                if tid not in lis:
                    lis.append(tid)
                    if tname in name_id:
                        需更新.add(tname)
                    else:
                        需新增.add(tname)
            print(机构id, 机构名称, '需更新:',len(需更新), '需新增:',len(需新增))
            for name in 需更新:
                tids = item[name]
                jid = name_id[name]
                r = self.修改服务基础(机构id=机构id, 服务名称=name, 套餐ids=tids, 服务基础id=jid)
                (成功 if type(r) is int else 失败)[name] = r
            for name in 需新增:
                tids = item[name]
                r = self.新增服务基础(机构id=机构id, 服务名称=name, 套餐ids=tids)
                (成功 if type(r) is int else 失败)[name] = r
        else:
            处理结果['data'] = '地址不完整'
        return 处理结果

    '''验证通过'''
    def 全部机构增量生成服务基础(self, 机构名称包含=''):
        rs = []
        机构ids = list(set(x['机构id'] for x in self.机构概况字典.values() if 机构名称包含 in x['机构名称']))
        total = len(机构ids)
        for i, x in enumerate(机构ids):
            rs.append(self.机构增量生成服务基础(机构id=x))
            print(f"\r{i}/{total} - {x}", end='    ')
        return rs
    
    '''验证通过'''
    def 获取机构详情(self, 机构id):
        params = dict(orgId=机构id)
        return self.get("baidu/org/detail", params=params)['data']
    
    '''验证通过'''
    def 按品牌修改市场价(self, 品牌名称, 市场价与实际价的比值=1.1):
        print(f'正在修改市场价 - {品牌名称}')
        品牌id = self.品牌字典[品牌名称]['品牌id']
        套餐ids = [x['套餐id'] for x in self.获取品牌套餐列表(品牌id=品牌id)]
        rs = {}
        for 套餐id in 套餐ids:
            data = self.获取套餐详情(套餐id=套餐id)
            实际价 = data['price']
            市场价 = math.ceil(实际价 * 市场价与实际价的比值)
            rs[套餐id] = self.修改套餐(套餐id=套餐id, olddata=data, 市场价=市场价)
        return rs

    '''验证通过'''
    def 获取品牌套餐列表(self, 品牌id):
        params = dict(brandId=品牌id, per=1)
        params['per'] = self.get("product/bh-package/packages", params=params)['total']
        return self.get("product/bh-package/packages", params=params)['data']
    
    def 把品牌下的套餐修改为test(self, 品牌id):
        套餐ids = [x['套餐id'] for x in self.获取品牌套餐列表(品牌id=品牌id)]
        rs = {}
        for 套餐id in 套餐ids:
            rs[套餐id] = self.套餐改为test(套餐id=套餐id)
        if set(rs.values()) == {True}:
            print('修改成功')
        else:
            print('部分修改失败')
        return rs
    
    def 套餐改为test(self, 套餐id):
        test专用品牌id = 135
        return self.修改套餐(
            套餐id=套餐id,
            注意事项 = 'test',
#             品牌id = test专用品牌id,
#             机构ids = [],
            性别 = '通用',
            头图 = 'https://img.tijian8.com/bh/package/1608256929923.jpg',
            市场价=99999,
            婚否='通用',
            名称='test',
            实际价=99999,
            销售量=0,
        )
    
    '''验证通过'''
    def 修改套餐(self, 套餐id, olddata=None, **kvs):
        婚否字典 = dict(已婚=1, 是=1, 未婚=0, 否=0, 通用=2)
        性别字典 = dict(男=0, 女=1, 通用=2)
        kvs = {k: v for k, v in kvs.items() if v is not None}
        data = olddata or self.获取套餐详情(套餐id=套餐id)
        newdata = dict(
            attention = kvs.get('注意事项', data['attention']),
            attributes = kvs.get('标签s', [dict(groupKey=x['group_key'], tagCode=x['标签代号'], tagId=x['标签id']) for x in data['package_types']] + [dict(groupKey=x['group_key'], tagCode=x['标签代号'], tagId=x['标签id']) for x in data['package_tags']]),
            brandId = kvs.get('品牌id', data['品牌id']),
            headerImage = kvs.get('头图', data['header_image']),
            items = kvs.get('单项s', [dict(itemId=x['item_id'], source=x['source']) for x in data['mutual_items']]),
            marketPrice = kvs.get('市场价', data['market_price']),
            orgIds = kvs.get('机构ids', [x['机构id'] for x in data['package_orgs']]),
            packageId = 套餐id,
            gender = 性别字典[kvs['性别']] if ('性别' in kvs) else data['gender'],
            married = 婚否字典[kvs['婚否']] if ('婚否' in kvs) else data['married'],
            packageImages = kvs.get('组图s', [x['image'] for x in data['images']]),
            packageName = kvs.get('名称', data['套餐名称']),
            packageVideo = kvs.get('视频', data['package_video']),
            price = kvs.get('实际价', data['price']),
            rank = data.get('rank', 10),
            saleNum = kvs.get('销售量', data['sale_num']),
            sealType = data.get('seal_type', 0),
            serviceIds = kvs.get('挂靠服务s', [x['服务id'] for x in data['services']]),
            serviceItems = [dict(textDesc=x['text_desc'], textTitle=x['text_title'], textImg=x['text_img']) for x in data['service_items']],
        )
        r = self.put("product/bh-package/package", data=newdata)
        if r['message'] in ('SUCCESS', ):
            return True
        else:
            print(套餐id, r)
            return r
    
    '''验证通过'''
    def 修改机构信息(self, 机构id, olddata=None, **kvs):
        kvs = {k: v for k, v in kvs.items() if v is not None}
        data = olddata or self.获取机构详情(机构id=机构id)
        机构名称 = kvs.get('机构名称', data['机构名称'])
        newdata = dict(
            address = kvs.get('地址', data['address']),
            brandId = kvs.get('品牌id', data['品牌id']),
            cityId = kvs.get('城市id', data['城市id']),
            cityName = kvs.get('城市名称', data['城市']),
            districtId = kvs.get('区域id', data['区域id']),
            districtName = kvs.get('区域名称', data['区']),
            images = kvs.get('图片', [x['image'] for x in data['images']]),
            orgCertifyDTO = kvs.get('认证内容', [dict(
                id=x['id'], textDesc=x['text_desc'], textImg=x['text_img'], textTitle=x['text_title']
            ) for x in data['机构认证内容']]),
            orgId = 机构id,
            orgLat = kvs.get('纬度', data['机构纬度']),
            orgLevel = kvs.get('机构等级', data['机构等级']),
            orgLgt = kvs.get('经度', data['机构经度']),
            orgLogo = kvs.get('logo', data['机构logo']),
            orgName = 机构名称,
            orgSketch = kvs.get('机构简介', data['org_sketch']),
            orgTel = kvs.get('电话', data['机构电话']),
            orgType = kvs.get('机构类型', data['org_type']),
            orgWorkTime = kvs.get('工作时间', data['机构工作时间']),
            provinceId = kvs.get('省份id', data['省份id']),
            provinceName = kvs.get('省份名称', data['省份']),
            reportType = kvs.get('报告类型', data['report_type']),
        )
        r = self.put("baidu/org", data=newdata)
        if r['message'] in ('SUCCESS', ):
            return True
        else:
            print(f"{机构id} - {机构名称} - {r}")
            return dict(机构id=机构id, 机构名称=机构名称, 参数=deepcopy(newdata), r=r)
    
    def 更新所有机构的经纬度(self):
        try:
            with open('百度机构经纬度', 'rb') as fa:
                已更新 = pickle.load(fa)
        except:
            已更新 = []
        机构s = {k: v['完整地址'] for k, v in self.机构概况字典.items() if (type(k) is int) and v['地址完整性'] and (k not in 已更新)}
        for 机构id, 机构地址 in 机构s.items():
            经纬度 = self.地址get经纬度(地址=机构地址)
            if 经纬度:
                print(f"正在更新经纬度 - {self.机构概况字典[机构id]['机构名称']} - {经纬度}")
                self.修改机构信息(机构id=机构id, 经度=经纬度['经度'], 纬度=经纬度['纬度'])
            已更新.append(机构id)
        with open('百度机构经纬度', 'wb') as fa:
            pickle.dump(已更新, fa)
        print('已更新全部经纬度')

    def 匹配特色标签(self, text, 规则=None):
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
    
    def 匹配人群标签(self, text, 规则=None):
        text = text.lower()
        规则 = 规则 or {
            '男性体检': ['男'],
            '青少年体检': ['少年'],
            '中老年体检': ['老年'],
            '女性体检': ['女'],
            '商务体检': ['商务'],
            '儿童体检': ['儿童'],
            '白领体检': ['白领'],
            '优生优育': ['优生'],
            '入职体检': ['入职', '招工'],
            '防癌筛查': ['癌'],
            '公务员体检': ['公务员'],
            '父母体检': ['父母'],
            '婚检孕检': ['婚', '孕', '优生']
        }
        return set(k for k, v in 规则.items() for x in v if x in text)
    
    def 提取唯一值(self, 字段名称, data, 非空=False):
        data = set(data)
        if len(data) == 1:
            data = list(data)[0]
            if 非空 and (not data):
                raise Exception(f"{字段名称} - 值不能为空: {data}")
            return data
        raise Exception(f"{字段名称} - 值不唯一: {data}")
        
    def 获取标签字典(self):
        print('正在获取标签字典')
        标签组s = self.get("tag/bh-tag/tag/List", params=dict(groupKey=None))['data']
        标签字典 = {}
        for 标签组 in 标签组s:
            标签字典[标签组['grou_tag_name']] = 标签字典[标签组['group_key']] = item = {}
            for x in 标签组['tags']:
                item[x['标签id']] = item[x['标签名称']] = x
        self.标签字典 = 标签字典
        return 标签字典

    def 新增套餐(self, **kvs):
        婚否字典 = dict(已婚=1, 是=1, 未婚=0, 否=0, 通用=2)
        性别字典 = dict(男=0, 女=1, 通用=2)
        是否特价字典 = dict(是=1, 否=0)
        newdata = dict(
            attention = kvs.get('注意事项', '暂无'),
            packageName = kvs['名称'],
            saleNum = kvs.get('销售量', random.randint(1, 10)),
            gender = 性别字典[kvs['性别']],
            married = 婚否字典[kvs['婚否']],
            orgIds = kvs['机构ids'],
            brandId = kvs['品牌id'],
            packageVideo = kvs.get('视频', None),
            rank = kvs.get('权重', 10),
            marketPrice = math.ceil(kvs['市场价']),
            price = math.ceil(kvs['实际价']),
            headerImage = kvs['头图'],
            packageImages = kvs['图片s'],
            serviceIds = kvs['挂靠服务s'],
            sealType = 是否特价字典[kvs.get('是否特价', '否')],
            serviceItems = kvs.get('服务须知', []),
            items = kvs['单项s'],
            attributes = kvs['标签s']
        )
        r = self.put("product/bh-package/package", data=newdata)
        if r['message'] in ('SUCCESS', ):
            return True
        else:
            r = f"{r}"
            print(r)
            return r



    def 从Excel上传套餐(
        self, path, 唯一识别字段='唯一识别', 机构字段='医院名称', 套餐名称字段='套餐名称', 单项名称字段='单项库叫法',
        市场价字段='市场价', 实际价字段='实际价', 是否特价字段='是否特价',
        图片字段='图片', 性别字段='性别', 年龄字段='适用年龄', 套餐特色标签匹配规则={},
        套餐人群标签匹配规则={}):
        
        def 提取性别和婚否(text):
            if ('男' in text) and ('女' in text):
                性别 = '通用'
            elif '男' in text:
                性别 = '男'
            elif '女' in text:
                性别 = '女'
            else:
                性别 = '通用'
            if '已婚' in text:
                婚否 = '已婚'
            elif '未婚' in text:
                婚否 = '未婚'
            else:
                婚否 = '通用'
            return dict(性别=性别, 婚否=婚否)
        
        df = pd.read_excel(path)
        
        # 提取所需数据
        套餐s = {}
        品牌 = self.提取唯一值(字段名称='品牌名称', data=df[机构字段], 非空=True)
        品牌id = self.品牌字典[品牌]['品牌id']
        机构ids = list(set(x['机构id'] for x in self.机构概况字典.values() if x['品牌id'] == 品牌id))
        if not 机构ids:
            raise Exception(f"该品牌下的机构为空")
        for 标识符, df in df.groupby(唯一识别字段):
            if not 标识符:
                raise Exception(f"唯一识别字段不能为空")
            else:
                套餐名称 = self.提取唯一值(字段名称='套餐名称', data=df[套餐名称字段], 非空=True)
                性别和婚否 = 提取性别和婚否(self.提取唯一值(字段名称='性别', data=df[性别字段], 非空=True))
                图片 = self.图片库.get(list(df[图片字段])[0]) or list(self.图片库.values())[0]
                图片 = random.sample(图片, 1)[0]
                单项名称s = '[SEP]'.join(list(df[单项名称字段])).replace('|', '[SEP]')
                单项名称s = list(set(re.split(' *\[SEP\] *| *\[SEG\] *', 单项名称s)))
                单项s = [self.统一单项字典.get(x) or self.统一单项字典.get(re.sub(' +$', '', x)) or self.统一单项字典[x] for x in 单项名称s]
                套餐名称单项名称 = random.choice(单项s)['统一单项名称']
                单项s = [dict(itemId=x['统一单项id'], source=1) for x in 单项s]
                特色标签s = self.匹配特色标签(str(单项名称s), 规则=套餐特色标签匹配规则)
                特色标签s = [self.标签字典['套餐特色标签'][x] for x in set(特色标签s)]
                特色标签s = [dict(groupKey='package_tag', tagCode=x['标签代号'], tagId=x['标签id']) for x in 特色标签s]
                if not 特色标签s: raise Exception(f"{标识符} - 特色标签不能为空")
                人群名称s = [y for x in list(df[年龄字段]) for y in re.split(' +', x)] + list(self.匹配人群标签(套餐名称, 规则=套餐人群标签匹配规则))
                人群名称s = list(set(人群名称s))
                人群标签s = [self.标签字典['套餐类型'][x] for x in set(人群名称s)]
                if not 人群标签s: raise Exception(f"{标识符} - 类型标签不能为空")
                套餐名称标签类型 = 人群标签s[0]['标签名称']
                人群标签s = [dict(groupKey='package_type', tagCode=x['标签代号'], tagId=x['标签id']) for x in 人群标签s]
                套餐名称 = f"{套餐名称}({套餐名称标签类型})({套餐名称单项名称})-{性别和婚否['性别']}"
                套餐s[标识符] = dict(
                    名称 = 套餐名称,
                    性别 = 性别和婚否['性别'],
                    婚否 = 性别和婚否['婚否'],
                    机构ids = 机构ids,
                    品牌id = 品牌id,
                    市场价 = self.提取唯一值(字段名称='市场价', data=df[市场价字段], 非空=True) * 100,
                    实际价 = self.提取唯一值(字段名称='实际价', data=df[实际价字段], 非空=True) * 100,
                    头图 = f"https://img.tijian8.com/tha/package/origin/{图片}",
                    图片s = [f"https://img.tijian8.com/tha/package/sm/{图片.replace('.', '_SM.')}"],
                    挂靠服务s = [],
                    是否特价 = dict(是='是', 否='否').get(self.提取唯一值(字段名称='是否特价', data=df[是否特价字段]), '否'),
                    服务须知 = [],
                    单项s = 单项s,
                    标签s = 特色标签s + 人群标签s,
                )
        # 上传套餐
        rs = {}
        for 标识符, 套餐 in 套餐s.items():
            rs[标识符] = self.新增套餐(**套餐)
        return rs

    def 获取统一单项列表(self):
        print('正在获取统一单项列表')
        params = dict(per=1)
        params['per'] = self.get("mutual-item/mutualItems", params=params)['total']
        统一单项列表 = self.get("mutual-item/mutualItems", params=params)['data']
        if '生成统一单项字典':
            self.统一单项字典 = 统一单项字典 = {x['统一单项id']:x for x in 统一单项列表}
            统一单项字典.update({x['统一单项名称']:x for x in 统一单项列表})
        return 统一单项列表
    
    '''验证通过'''
    def 获取单项类型(self, 单项级别=1):
        params = dict(per=1, groupLevel=单项级别)
        params['per'] = self.get("item-group/groups", params=params)['total']
        return self.get("item-group/groups", params=params)['data']
    
    '''验证通过'''
    def 生成一级单项字典(self):
        print('正在生成一级单项字典')
        kws = self.获取单项类型(单项级别=1)
        self.一级单项字典 = item = {x['项目组id']: x for x in kws}
        item.update({x['项目组名称']: x for x in kws})
        return item
    
    '''验证通过'''
    def 生成二级单项字典(self):
        print('正在生成二级单项字典')
        kws = self.获取单项类型(单项级别=2)
        self.二级单项字典 = item = {x['项目组id']: x for x in kws}
        item.update({x['项目组名称']: x for x in kws})
        return item
    
    '''验证通过'''
    def 新增二级单项(self, 一级单项id, 单项名称):
        data = dict(parentId=一级单项id, itemGroupName=单项名称, sort=1)
        r = self.post("item-group/group", data=data)
        msg = r.get('message')
        if msg in ['OK', '提交的类型名称已存在,请修改后重新提交', 'SUCCESS', '单项类型名称已存在', '成功']:
            self.生成二级单项字典()
            return True
        else:
            msg = f"{一级单项id} - {单项名称} - {r}"
            print(msg)
            return msg
    
    '''验证通过'''
    def 新增统一单项(self, 二级单项id, 单项名称):
        data = dict(itemGroupId=二级单项id, mutualItemDesc='暂无', mutualItemName=单项名称, sort=1)
        r = self.post("mutual-item/mutualItem", data=data)
        msg = r.get('message')
        if msg in ['OK', '提交的类型名称已存在,请修改后重新提交', '成功', '统一单项名称已存在', 'SUCCESS']:
            return True
        else:
            msg = f"{二级单项id} - {单项名称} - {r}"
            print(msg)
            return msg
    
    def 从Excel新增统一单项(self, file, 一级字段='一级', 二级字段='二级', 三级字段='三级'):
        df = pd.read_excel(file)
        # 判断单项重复
        重复的 = [k for k, v in dict(Counter([a[1] for a, b in df.groupby([一级字段, 二级字段])])).items() if v > 1]
        if 重复的:
            raise Exception(f"二级单项重复: {重复的}")
        重复的 = [k for k, v in dict(Counter(df[三级字段])).items() if v > 1]
        if 重复的:
            raise Exception(f"三级单项重复: {重复的}")
        # 判断数据是否有误
        df = kws = df.to_dict(orient='records')
        for x in kws:
            一级单项, 二级单项, 统一单项 = [x[y] for y in (一级字段, 二级字段, 三级字段)]
            if 一级单项 not in self.一级单项字典:
                raise Exception(f"一级单项 {一级单项} 不存在")
            if 二级单项 in self.二级单项字典:
                实际一级单项 = self.一级单项字典[self.二级单项字典[二级单项]['父级id']]['项目组名称']
                if 一级单项 != 实际一级单项:
                    raise Exception(f"二级单项 {二级单项} 已存在于 一级单项 {实际一级单项} 中")
        # 批量添加
        kws = [x for x in kws if x['三级'] not in self.统一单项字典]
        rs = {}
        for count, x in enumerate(kws):
            一级单项, 二级单项, 统一单项 = [x[y] for y in (一级字段, 二级字段, 三级字段)]
            if 二级单项 not in self.二级单项字典:
                print(f'二级单项 {二级单项} 不存在, 将自动创建二级单项')
                一级单项id = self.一级单项字典[一级单项]['项目组id']
                self.新增二级单项(一级单项id=一级单项id, 单项名称=二级单项)
            二级单项id = self.二级单项字典[二级单项]['项目组id']
            rs[统一单项] = self.新增统一单项(二级单项id=二级单项id, 单项名称=统一单项)
        self.获取统一单项列表()
        return rs
    
    def 品牌简介复制到旗下机构(self, 品牌=''):
        if 品牌:
            x = self.品牌字典[品牌]
            品牌简介s = {x['品牌id']: x['brand_desc']}
        else:
            品牌简介s = {x['品牌id']: x['brand_desc'] for x in self.品牌字典.values()}
        品牌简介s = {k: v for k, v in 品牌简介s.items() if v}
        机构清单 = {机构['机构id']: 机构['品牌id'] for 机构 in self.机构概况字典.values()}
        机构清单 = {机构id: 品牌简介s[品牌id] for 机构id, 品牌id in 机构清单.items() if 品牌id in 品牌简介s}
        rs = {}
        i = 0
        total = len(机构清单)
        for 机构id, 机构简介 in 机构清单.items():
            i += 1
            print(f"\r{i}/{total} - {机构id}    ", end='')
            rs[机构id] = self.修改机构信息(机构id=机构id, 机构简介=机构简介)
        fails = {k: v for k, v in rs.items() if v is not True}
        print(f'修改失败: {fails.keys()}')
        return fails
    
    def 同步服务(self, 单位, id=None):
        类型字典 = dict(服务=1, 品牌=2, 机构=3, 全部=4, 服务基础=5)
        params = {'type': 类型字典[单位]}
        if id: params['id'] = str(id)
        r = self.post("baidu/service/syn/part", data=params)
        print(r)
        if r['message'] in ('SUCCESS', ):
            return True
        else:
            return r
