# -!- coding: utf-8 -!-
import re, os, sys, requests, json, math, time, copy, random, pickle
import pandas as pd
from copy import deepcopy
from collections import Counter
from math import ceil
from .shanjianwang_api2_taocan import 善检网api第2版_套餐

class 善检网api第2版_套餐_阿里(善检网api第2版_套餐):
    
    def __init__(self):
        善检网api第2版_套餐.__init__(self)
        print('阿里套餐接口')
        self.生成单项字典()
        self.生成机构字典()
        self.获取标签列表()
        self.初始化人群标签()
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
        item_group_id = '项目组id', item_group_name = '项目组名称', address='地址', publish='发布',
        org_phone='机构电话', label='标签', status='状态', package_group_id='套餐组id', 
        package_group_name='套餐组名称', category_id='类别id', package_ids='套餐ids',
        package_group_status='套餐组状态', gender='性别', contract_price='合同价',
        settlement_price='结算价',
    )
    
    def 初始化人群标签(self):
        self.人群标签互斥字典 = {
            '入职体检': {'父母体检', '儿童体检', '职场体检', '深度体检', '婚检孕检体检', '婚前孕前体检'},
            '父母体检': {'入职体检', '证件体检', '儿童体检', '婚前孕前体检'},
            '女性体检': {'男性体检', '儿童体检', '证件体检'},
            '男性体检': {'女性体检', '儿童体检', '证件体检'},
            '深度体检': {'入职体检', '儿童体检', '证件体检'},
            '儿童体检': {'入职体检', '父母体检', '女性体检', '男性体检', '深度体检', '儿童体检', '白领体检', '证件体检', '婚前孕前体检', '特惠体检'},
            '专项体检': {'入职体检', '父母体检', '深度体检', '婚检孕检体检', '婚前孕前体检', '证件体检'},
            '白领体检': {'父母体检', '入职体检', '婚检孕检体检', '婚前孕前体检', '证件体检'},
            '证件体检': {'白领体检', '父母体检', '深度体检', '婚检孕检体检', '婚前孕前体检', '儿童体检'},
            '婚前孕前体检': {'入职体检', '父母体检', '儿童体检', '专项体检', '证件体检'},
            '特惠体检': set(),
        }
        for k, v in deepcopy(self.人群标签互斥字典).items():
            k = {k}
            for x in v:
                x = self.人群标签互斥字典.get(x, set())
                x |= k
        self.人群标签数值字典 = {10 ** i: x for i, x in enumerate(self.人群标签互斥字典)}
        self.人群标签数值字典.update({v: k for k, v in self.人群标签数值字典.items()})
        self.人群标签转数值 = lambda s: sum(self.人群标签数值字典[x] for x in s)
        self.人群标签结果字典 = {}
    
    def 选择人群标签(self, o=set(), s=set()):  # o表示已选择, s表示待选择
        # 未匹配到任意项目时将会返回: [set()]
        rkey = (self.人群标签转数值(o), self.人群标签转数值(s))
        if rkey in self.人群标签结果字典:
            return self.人群标签结果字典[rkey]
        else:
            rvalue = [o]
            for x in o: s = s - self.人群标签互斥字典[x]
            if s:
                rs = {len(o): [o]}
                for x in s:
                    for r in self.选择人群标签(o = o | {x}, s = s - {x}):
                        rs.setdefault(len(r), []).append(r)
                rvalue = list({self.人群标签转数值(x): x for x in rs[max(rs)]}.values())
            self.人群标签结果字典[rkey] = rvalue
            return rvalue
    
    def 匹配人群标签(self, text):
        项目规则 = {
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
        text = text.lower()
        tags = set(k for k, v in 项目规则.items() for x in v if x in text)
        return self.选择人群标签(s=tags)
    
    "已完成"
    def 查询单项类型(self, 单项级别, 父级id=None, 单项名称=None):
        ''' 单项级别: 1, 2 '''
        params = dict(groupLevel=单项级别, groupName=单项名称, parentId=父级id, per=1)
        params['per'] = self.get("item/ah-item-group/groups", params=params)['total']
        data = self.get("item/ah-item-group/groups", params=params)['data']
        for x in data:
            x['单项id'] = x.pop('项目组id')
            x['单项名称'] = x.pop('项目组名称')
        self.转中文(data)
        return data  # 父级id, 单项id, 单项名称
    
    "已完成"
    def 套餐详情(self, 套餐id):
        params = dict(packageId=套餐id)
        return self.get("alibaba/package", params=params)['data']
    
    "已完成"
    def 套餐列表(self, 机构id, 套餐名称=None, 上架=None, 创建时间范围=(None, None)):
        params = dict(orgId=机构id, bizField=套餐名称, per=1)
        if 上架 != None:
            params['status'] = 上架  # 套餐组状态 0:未发布  1:发布上架 2:发布下架
        params['per'] = self.get("alibaba/packages", params=params)['total']
        data = self.get("alibaba/packages", params=params)['data']
        f = lambda x: time.mktime(time.strptime(x, "%Y-%m-%d %H:%M:%S"))
        start_time = f(创建时间范围[0] or '1999-10-10 10:10:10')
        end_time = f(创建时间范围[1] or '2999-10-10 10:10:10')
        return [x for x in data if start_time <= f(x['创建时间']) <= end_time]
    
    "已完成"
    def 套餐组详情(self, 套餐组id):
        params = dict(packageGroupId=套餐组id)
        return self.get("alibaba/package-group", params=params)['data']
    
    "已完成"
    def 新增二级单项(self, 一级单项id, 单项名称=None):
        data = dict(parentId=一级单项id, itemGroupName=单项名称, sort=1)
        r = self.post("item/ah-item-group/group", data=data)
        self.生成单项字典()
        msg = r.get('message') or str(r)
        if msg in ['OK', '提交的类型名称已存在,请修改后重新提交', 'SUCCESS', '单项类型名称已存在', '成功']:
            return '成功', msg
        else:
            return '失败', msg
    
    "已完成"
    def 查询统一单项(self, 二级单项id=None, 单项名称=None):
        params = dict(itemGroupId=二级单项id, per=1, mutualItemName=单项名称)
        params['per'] = self.get("alibaba/mutualItems", params=params)['total']
        return self.get("alibaba/mutualItems", params=params)['data']
    
    "已完成"
    def 新增统一单项(self, 二级单项id, 单项名称, 描述=None, 设为基础项=None):
        data = dict(itemGroupId=二级单项id, mutualItemName=单项名称, sort=1, mutualItemDesc=描述)
        if 设为基础项 != None:
            data['basic'] = 1 if 设为基础项 else 0
        r = self.post("alibaba/mutualItem", data=data)
        msg = r.get('message') or str(r)
        if msg in ['OK', '提交的类型名称已存在,请修改后重新提交', '统一单项名称已存在', 'SUCCESS', '成功']:
            return '成功', msg
        else:
            return '失败', msg
    
    "已完成"
    def 生成单项字典(self):
        print('正在生成单项字典..')
        self.统一单项字典 = item = {x['统一单项id']:x['统一单项名称'] for x in self.查询统一单项()}
        item.update({v:k for k,v in item.items()})
        item = {}
        self.单项字典 = 单项字典 = {}
        for x in self.查询单项类型(单项级别=2):
            一级单项id, 二级单项id, 单项名称 = [x[y] for y in ('父级id', '单项id', '单项名称')]
            if 一级单项id not in item:
                item[一级单项id] = {}
            item[一级单项id][二级单项id] = item[一级单项id][单项名称] = dict(二级单项id=二级单项id, 二级单项名称=单项名称)
        for x in self.查询单项类型(单项级别=1):
            一级单项id, 单项名称 = [x[y] for y in ('单项id', '单项名称')]
            单项字典[一级单项id] = 单项字典[单项名称] = dict(
                一级单项id=一级单项id,
                一级单项名称=单项名称,
                二级单项=item.get(一级单项id) or {}
            )
        self.二级单项字典 = {y:dict(一级单项名称=k) for k, x in 单项字典.items() for y in x['二级单项']}
    
    "已完成"
    def 查询机构单项(self, 二级单项id=None, 机构id=None, 单项名称=None, 单项id=None):
        params = dict(itemGroupId=二级单项id, orgId=机构id, orgItemName=单项名称, per=1, orgItemId=单项id)
        params['per'] = self.get("item/ah-org-item/orgItems", params=params)['total']
        return self.get("item/ah-org-item/orgItems", params=params)['data']
    
    "已完成"
    def 获取机构列表(self, 状态=None):
        params = dict(per=1)
        if 状态 != None:
            params['publish'] = 1 if 状态 else 0
        params['per'] = self.get("alibaba/orgs", params=params)['total']
        data = self.get("alibaba/orgs", params=params)['data']
        for x in data:
            x['完整地址'] = x['省份'] + x['城市'] + x['区'] + x['地址']
            x['地址完整性'] = '暂无' not in x['完整地址']
        return data
    
    "已完成"
    def 获取套餐组列表(self, 机构id, 套餐组名称=None, 上架=None):
        params = dict(bizField=套餐组名称, orgId=机构id)
        if 上架 != None:  # 0:未发布 1:发布上架 2:发布下架
            params['status'] = 上架
        return self.get("alibaba/package-groups", params=params)['data']
    
    def 提取套餐组id_未发布(self, 机构名称):
        机构id = self.机构字典[机构名称]['机构id']
        tgs = self.获取套餐组列表(机构id=机构id, 上架=0)
        tgs = [x for x in tgs if 'test' not in x['套餐组名称']]
        return [x['套餐组id'] for x in tgs]
    
    def 提取套餐组id_已发布未上架(self, 机构名称):
        机构id = self.机构字典[机构名称]['机构id']
        tgs = self.获取套餐组列表(机构id=机构id, 上架=2)
        tgs = [x for x in tgs if 'test' not in x['套餐组名称']]
        return [x['套餐组id'] for x in tgs]
    
    def 提取套餐组id_已发布且上架(self, 机构名称):
        机构id = self.机构字典[机构名称]['机构id']
        tgs = self.获取套餐组列表(机构id=机构id, 上架=1)
        tgs = [x for x in tgs if 'test' not in x['套餐组名称']]
        return [x['套餐组id'] for x in tgs]
    
    def 提取套餐组id_全部(self, 机构名称):
        机构id = self.机构字典[机构名称]['机构id']
        tgs = self.获取套餐组列表(机构id=机构id)
        tgs = [x for x in tgs if 'test' not in x['套餐组名称']]
        return [x['套餐组id'] for x in tgs]
    
    "已完成"
    def 获取标签列表(self, group_key=None):
        r = self.get("alibaba/tag/List", params=dict(groupKey=None))['data']
        self.标签字典 = item = {}
        for x in r:
            type_ = x['group_key']
            if type_ not in item:
                item[type_] = {}
            item[type_][x['标签id']] = item[type_][x['标签名称']] = item[type_][x['标签代号']] = x
        item['套餐分类标签'] = item['package_type']
        item['机构等级'] = item['org_rank']
        item['套餐特色标签'] = item['package_feature']
        if group_key:
            return [x for x in r if x['group_key'] == group_key]
        return r
    
    "已完成"
    def 生成机构字典(self):
        print('正在生成机构字典..')
        self.机构字典 = 机构字典 = {}
        for x in self.获取机构列表():
            机构id, 机构名称 = [x[y] for y in ('机构id', '机构名称')]
            机构字典[机构id] = 机构字典[机构名称] = x
    
    "已完成"
    def 批量新增统一单项(self, kws, 一级字段='一级', 二级字段='二级', 三级字段='三级', 设为基础项=False):
        type_kws = type(kws)
        if type_kws is pd.core.frame.DataFrame:
            kws = json.loads(kws.to_json(orient='records'))
        elif type_kws is str:
            df = pd.read_excel(kws)
            重复的 = [k for k, v in dict(Counter([a[1] for a, b in df.groupby([一级字段, 二级字段])])).items() if v > 1]
            if 重复的:
                print(重复的)
                return None
            kws = json.loads(df.to_json(orient='records'))
        for x in kws:
            一级 = self.二级单项字典.get(x['二级'], {}).get('一级单项名称') or None
            if x['一级'] not in self.单项字典:
                print(f"一级单项 {x['一级']} 不存在")
                强制报错
            if 一级 and 一级 != x['一级']:
                print(f"二级单项 {x['二级']} 已存在于 {一级}中, 无法向 {x['一级']} 添加")
                强制报错
        kws = [x for x in kws if x['三级'] not in self.统一单项字典]
        total = len(kws)
        for count, x in enumerate(kws):
            一级单项名称, 二级单项名称, 三级单项名称 = [x[y] for y in (一级字段, 二级字段, 三级字段)]
            二级单项 = self.单项字典[一级单项名称]['二级单项'].get(二级单项名称)
            if 二级单项:
                二级单项id = 二级单项['二级单项id']
            else:
                print(f'\r{x} - 二级单项不存在, 将自动创建二级单项', end='')
                一级单项id = self.单项字典[一级单项名称]['一级单项id']
                self.新增二级单项(一级单项id=一级单项id, 单项名称=二级单项名称)
                二级单项id = self.单项字典[一级单项名称]['二级单项'][二级单项名称]['二级单项id']
            x['状态'], x['msg'] = self.新增统一单项(二级单项id=二级单项id, 单项名称=三级单项名称, 设为基础项=设为基础项)
        print()
        self.生成单项字典()
        return kws
    
    "已完成"
    数据分组 = lambda self, data, size: [data[size*(i-1): size*i] for i in range(1, ceil(len(data)/size)+1)]
    
    "已完成"
    def 套餐组改成test(self, 机构id, 套餐组id):
        data = dict(
            orgId=机构id,
            packageGroupId=套餐组id,
            packageGroupName='test',
            targetGroup='test',  # 套餐组目标人群
            description='test',  # 套餐组描述
            label = 'B' if ('test' in self.domain) else 'C',
            mode = 1,
        )
        r = self.post("alibaba/package-group", data=data)
        msg = r.get('message') or str(r)
        if msg in ['SUCCESS', '成功']:
            return '成功'
        else:
            return '失败', msg
    
    def 清空机构套餐(self, 机构id):
        for x in [x['套餐组id'] for x in self.获取套餐组列表(机构id=机构id)]:
            self.套餐组改成test(机构id=机构id, 套餐组id=x)
            
    "已完成"
    def 获取机构详情(self, 机构id):
        params = dict(orgId=机构id)
        return self.get("alibaba/org", params=params)['data']
    
    '''验证通过'''
    def 修改机构信息(self, 机构id, olddata=None, **kvs):
        kvs = {k: v for k, v in kvs.items() if v is not None}
        data = olddata or self.获取机构详情(机构id=机构id)
        newdata = dict(
            address = kvs.get('地址', data['地址']),
            agreement = kvs.get('协议图片', data['agreement']),
            businessLicense = kvs.get('营业执照图片', data['business_license']),
            cityCode = kvs.get('城市code', data['city_code']),
            cityId = kvs.get('城市id', data['city_id']),
            cityName = kvs.get('城市名称', data['城市']),
            description = kvs.get('描述', data['描述']),
            districtId = kvs.get('区域id', data['district_id']),
            districtName = kvs.get('区域名称', data['区']),
            environmentPictures = kvs.get('环境图s', [x['env_picture_name'] for x in data['environments']]),
            examNotice = kvs.get('特别提醒', data['exam_notice']),
            latitude = kvs.get('纬度', data['latitude']),
            logo = kvs.get('logo', data['logo']),
            longitude = kvs.get('经度', data['longitude']),
            medicalLicense = kvs.get('医疗许可证图片', data['medical_license']),
            mode = data['mode'],
            notify = data['notify'],
            onlineReport = data['online_report'],
            orgId = 机构id,
            orgName = kvs.get('机构名称', data['机构名称']),
            orgPhone = kvs.get('电话', data['机构电话']),
            orgRank = data['机构排名'],
            provinceId = kvs.get('省份id', data['province_id']),
            provinceName = kvs.get('省份名称', data['省份']),
            reportWay = data['report_way'],
            reportWayOnline = data['report_way_online'],
            routes = kvs.get('交通路线', data['routes']),
            workTime = kvs.get('工作时间', data['work_time'])
        )
        r = self.put("alibaba/org", data=newdata)
        if r['message'] in ('SUCCESS', ):
            return True
        else:
            print(机构id, r)
            return dict(机构id=机构id, 参数=deepcopy(newdata), r=r)
    
    '''验证通过'''
    def 更新所有机构的经纬度(self):
        try:
            with open('阿里机构经纬度', 'rb') as fa:
                已更新 = pickle.load(fa)
        except:
            已更新 = []
        机构s = {k: v['完整地址'] for k, v in self.机构字典.items() if (type(k) is int) and v['地址完整性'] and (k not in 已更新)}
        for 机构id, 机构地址 in 机构s.items():
            经纬度 = self.地址get经纬度(地址=机构地址)
            if 经纬度:
                print(f"正在更新经纬度 - {self.机构字典[机构id]['机构名称']} - {经纬度}")
                self.修改机构信息(机构id=机构id, 经度=经纬度['经度'], 纬度=经纬度['纬度'])
            已更新.append(机构id)
        with open('阿里机构经纬度', 'wb') as fa:
            pickle.dump(已更新, fa)
        print('已更新全部经纬度')
    
    "已完成"
    def 发布套餐组(self, 套餐组id):
        data = dict(groupId=套餐组id)
        r = self.post("alibaba/goods-publish-external", data=data)
        try:
            r_pro = json.loads(r['data']['body'])['alibaba_alihealth_examination_goods_publish_response']
            if r_pro['result']['success'] == True:
                print(r_pro)
                return '成功', r_pro
            else:
                return '失败', str(r)
        except:
            return '失败', str(r)

    def 匹配特色标签(self, 项目):
        项目规则 = [
            ('外科', '外科'), ('肝功', '肝功能'), ('糖尿', '糖尿病'), ('眼', '眼科'), ('基因', '基因检测'),
            ('肿瘤和癌', '肿瘤筛查'), ('胃镜', '胃镜'), ('肠镜', '肠镜'), ('心肌', '心肌功能'),
            ('肾功', '肾功能'), ('甲功', '甲状腺功能')
        ]
        return [y for x, y in 项目规则 if x in 项目]
    
    "已完成"
    def 新增套餐组(self, 机构id, 名称):  # 新增后套餐组状态为0, 需要手动修改
        # 可添加同名套餐组
        data = dict(
            orgId=机构id,
            packageGroupName=名称,
            targetGroup=名称,  # 套餐组目标人群
            description=名称,  # 套餐组描述
            label = 'B' if ('test' in self.domain) else 'C',
            mode = 1,
        )
        r = self.post("alibaba/package-group", data=data)
        msg = r.get('message') or str(r)
        if msg in ['SUCCESS', '成功']:
            return dict(套餐组id=r['data'])
        else:
            print(msg)
            return '失败', msg
    
    '------------------------- 新增套餐相关 -----------------------------------------------'
    
    
    "已完成"
    def 从Excel提取套餐(self, path, 唯一识别字段='唯一识别', 机构字段='医院名称', 套餐名称字段='套餐名称',
                   单项字段='单项库叫法', 图片字段='图片', 性别字段='性别', 年龄字段='适用年龄',
                   价格字段='价格', 挂网折扣字段='挂网折扣', 结算折扣字段='结算折扣', 结算价字段='结算价'):
        try:
            df = pd.read_excel(path)
        except:
            df = pd.read_excel(path)
        # 判断字段是否缺失
        字段s = df.columns.to_list()
        for x in ('唯一识别', '医院名称', '套餐名称', '单项库叫法', '图片', '性别', '适用年龄',
                 '价格', '结算价', '结算折扣', '挂网折扣'):
            if x not in 字段s:
                print(f"字段 [{x}] 不在Excel文档中")
                强制报错
        # 判断机构是否重复
        机构s = set(df[机构字段].to_list())
        if len(机构s) > 1:
            print(f"机构名称不一致: {机构s}")
            强制报错
        else:
            机构名称 = list(机构s)[0]       

        df[性别字段].replace(['男', '男已婚', '已婚男', '男未婚', '未婚男'], ['男通用'] * 5, inplace=True)
        # api接口对男性只支持男性通用, 所以统一修改为男性通用
        df[性别字段].replace(['已婚女', '未婚女'],['女已婚', '女未婚'], inplace=True)
        df[性别字段].replace(['女性通用', '女'], ['女通用'] * 2, inplace=True)
        性别拆分字典 = dict(
            男女通用 = ('通用', '通用', '男女通用'),  # 性别, 婚否, 套餐补名
            男通用 = ('男', '通用', '男士'),
            女通用 = ('女', '通用', '女士'),
            女未婚 = ('女', '未婚', '女士'),
            女已婚 = ('女', '已婚', '女士')
        )
        # 提取所需数据
        套餐s = []
        for 标识符, df in df.groupby(唯一识别字段):
            df = df.copy()
            套餐 = {}
            套餐s.append(套餐)
            # 套餐名称
            套餐名称 = set(df[套餐名称字段].to_list())
            if len(套餐名称) > 1:
                print(f"{机构名称} 唯一识别 {标识符} 套餐名称不唯一: {套餐名称}")
                强制报错
            else:
                套餐['套餐名称'] = 套餐名称 = list(套餐名称)[0]

            # 性别 和 婚否
            性别 = list(set([y for x in list(df[性别字段]) for y in re.split(' +', x) if y]))
            if len(性别) > 1:
                print("套餐性别过多")
                强制报错
            else:
                套餐['性别'], 套餐['婚否'], 套餐补名 = 性别拆分字典[性别[0]]
            
            # 价格
            df[结算价字段].fillna(-1, inplace=True)
            df[结算折扣字段].fillna(-1, inplace=True)
            价格 = set(df[价格字段])
            挂网折扣 = set(df[挂网折扣字段])
            结算折扣 = set(df[结算折扣字段])
            结算价 = set(df[结算价字段])
            if (len(价格) > 1) or (len(挂网折扣) > 1) or (len(结算折扣) > 1) or (len(结算价) > 1):
                print(f"价格数量有误 - {价格, 挂网折扣, 结算折扣, 结算价}")
                强制报错
            else:
                价格 = float(list(价格)[0])
                挂网折扣 = float(list(挂网折扣)[0])
                结算折扣 = float(list(结算折扣)[0])
                结算价 = float(list(结算价)[0])
                if 结算折扣 > 0:
                    结算价 = 价格 * 结算折扣 / 100
                套餐['结算价'] = 结算价
                套餐['价格'] = 价格 = 价格 * 挂网折扣 / 100

            # 图片
            套餐['图片'] = random.sample(self.图片库[df[图片字段].to_list()[0]], 1)[0]

            # 单项 和 特色标签
            单项 = re.split(' *\[SEP\] *| *\[SEG\] *', '[SEP]'.join(list(df[单项字段])).replace('|', '[SEP]'))
            套餐['单项'] = 单项 = list(set(单项))
            套餐['单项id'] = [self.统一单项字典.get(x) or self.统一单项字典.get(re.sub(' +$', '', x)) or self.统一单项字典[x] for x in 单项]
            套餐['特色标签'] = 特色标签 = self.匹配特色标签(项目=str(单项).replace(' ', ''))
            套餐['特色标签参数'] = [dict(groupKey='package_feature', tagId=self.标签字典['package_feature'][x]['标签id']) for x in 特色标签]
            if not 套餐['特色标签参数']:
                print(f"{标识符} - 未匹配到特色标签")
            # 分类标签(即: 人群标签)
            套餐['分类标签'] = 分类标签 = self.匹配人群标签(text=f"{set(df[年龄字段])}{套餐名称}")[0]
            套餐['分类标签参数'] = [dict(groupKey='package_type', tagId=self.标签字典['package_type'][x]['标签id']) for x in 分类标签]
            if not 套餐['分类标签参数']:
                print(f"{标识符} - 未匹配到分类标签")
            套餐['套餐名称'] = 套餐名称
        
        
        return dict(机构名称=机构名称, 套餐s=套餐s)
    
    def 修改套餐(self, 机构id, 套餐id, olddata=None, **kvs):
        婚否字典 = dict(已婚=1, 是=1, 未婚=0, 否=0, 通用=2)
        性别字典 = dict(男=0, 女=1, 通用=2)
        kvs = {k: v for k, v in kvs.items() if v is not None}
        data = olddata or self.套餐详情(套餐id=套餐id)
        newdata = dict(
            contractPrice = kvs.get('合同价', data['合同价']),
            description = kvs.get('描述', data['描述']),
            detailImage = kvs.get('详情图', data['detail_image']),
            gender = 性别字典[kvs['性别']] if ('性别' in kvs) else data['性别'],
            items = [dict(itemId=x['item_id'], source=x['source']) for x in data['mutual_items']],
            listImage = kvs.get('列表图', data['list_image']),
            marriage = 婚否字典[kvs['婚否']] if ('婚否' in kvs) else data['marriage'],
            orgId = 机构id,
            packageFeature = [dict(groupKey='package_feature', tagId=self.标签字典['package_feature'][x]['标签id']) for x in kvs['特色标签s']] if ('特色标签s' in kvs) else [dict(groupKey=x['group_key'], tagId=x['标签id']) for x in data['features']],
            packageGroupId = data['组id'],
            packageId = 套餐id,
            packageName = kvs.get('套餐名称', data['套餐名称']),
            packageTypes = [dict(groupKey='package_type', tagId=self.标签字典['package_type'][x]['标签id']) for x in kvs['分类标签s']] if ('分类标签s' in kvs) else [dict(groupKey=x['group_key'], tagId=x['标签id']) for x in data['types']],
            settlementPrice = kvs.get('结算价', data['结算价']),
        )
        r = self.put("alibaba/package", data=newdata)
        if r['message'] in ('SUCCESS', ):
            return True
        else:
            print(r)
            return str(r)
    
    
    "已完成"
    def 新增套餐(self, datas, 套餐名称字段, 价格字段, 单项id字段, 性别字段, 婚否字段, 特色标签参数字段,
                 分类标签参数字段, 图片字段, 结算价字段):
        
        # 打印屏幕提醒
        机构名称 = datas['机构名称']
        机构id = self.机构字典[机构名称]['机构id']
        print(机构id, 机构名称)
        
        # 根据套餐名称生成套餐组
        套餐组s = {}
        for 套餐 in datas['套餐s']:
            jua = re.sub('（*\(*[男女士]*(通用)*\)*）*', '', 套餐[套餐名称字段])
            if jua in 套餐组s:
                套餐组s[jua].append(dict(数据=套餐))
            else:
                套餐组s[jua] = [dict(数据=套餐)]
        套餐组s = [dict(套餐组名称=name, 套餐=x) for name, ts in 套餐组s.items() 
                for x in self.数据分组(data=ts, size=3)]
        # 根据阿里组合重组套餐组
        new套餐组s = []
        jud = dict(男='0', 女='1', 通用='2')
        juc = dict(未婚='0', 已婚='1', 通用='2')
        允许组合 = [
            {'22'}, {'02'}, {'12'}, {'10'}, {'11'},
            {'02', '12'}, {'02', '10'}, {'02', '11'}, {'10', '11'},
            {'02', '10', '11'}
        ]
        for 套餐组 in 套餐组s:
            组合 = set([jud[套餐['数据'][性别字段]] + juc[套餐['数据'][婚否字段]] for 套餐 in 套餐组['套餐']])
            if 组合 in 允许组合:
                new套餐组s.append(套餐组)
            else:
                套餐组名称 = 套餐组['套餐组名称']
                for 套餐 in 套餐组['套餐']:
                    new套餐组s.append(dict(套餐组名称=套餐组名称, 套餐=[套餐]))
        # 确定套餐组
        datas['套餐组s'] = 套餐组s = new套餐组s
        
        # 批量上传
        for 套餐组 in 套餐组s:
            # 新建套餐组
            套餐组名称 = 套餐组['套餐组名称']
            套餐组['套餐组id'] = 套餐组id = self.新增套餐组(机构id=机构id, 名称=套餐组名称)['套餐组id']

            # 批量上传套餐
            for 套餐 in 套餐组['套餐']:
                数据 = 套餐['数据']
                套餐['参数'] = data = dict(
                    contractPrice = 数据[价格字段] * 100,
                    detailImage = f"https://img.tijian8.com/tha/package/origin/{数据[图片字段]}",
                    gender = dict(男=0, 女=1, 通用=2)[数据[性别字段]],
                    items = [dict(itemId=x, source=1) for x in 数据[单项id字段]],
                    listImage = f"https://img.tijian8.com/tha/package/sm/{数据[图片字段].replace('.', '_SM.')}",
                    marriage = dict(未婚=0, 已婚=1, 通用=2)[数据[婚否字段]],
                    orgId = 机构id,
                    packageFeature = 数据[特色标签参数字段],
                    packageGroupId = 套餐组id,
                    packageName = 数据[套餐名称字段],
                    packageTypes = 数据[分类标签参数字段],
                    settlementPrice = 数据[结算价字段] * 100
                )
                r = self.post("alibaba/package", data=data)
                if r['message'] in ('SUCCESS', '成功'):
                    套餐['状态'] = '成功'
                    套餐['套餐id'] = r['data']
                else:
                    套餐['状态'] = str(r)
                    套餐['套餐id'] = r.get('data') or None
        print(set([y['状态'] for x in datas['套餐组s'] for y in x['套餐']]))
        return datas
    
    def 重置所有套餐的人群标签(self):
        性别字典 = {0: '男', 1: '女', 2: '男女'}
        rs = {}
        for 机构id in [x for x in self.机构字典 if type(x) is int]:
            for 套餐 in self.套餐列表(机构id=机构id):
                套餐id = 套餐['套餐id']
                套餐详情 = self.套餐详情(套餐id=套餐id)
                text = f"{套餐详情['套餐名称']}{[x['标签名称'] for x in 套餐详情['types']]}"
                分类标签s = self.匹配人群标签(text=text)[0] or self.匹配人群标签(text=性别字典[套餐['性别']])[0]
                r = self.修改套餐(机构id=机构id, 套餐id=套餐id, olddata=套餐详情, 分类标签s=分类标签s)
                rs[(机构id, 套餐id)] = r
                print(f"\r{机构id} - {套餐id} - {r}    ", end='')
        return rs
