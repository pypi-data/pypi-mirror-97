# -!- coding: utf-8 -!-
import re, os, sys, requests, json, math, time, copy, random
import pandas as pd
from copy import deepcopy
from collections import Counter
from .shanjianwang_api2_taocan import 善检网api第2版_套餐


class 善检网api第2版_套餐_腾讯(善检网api第2版_套餐):
    
    def __init__(self):
        善检网api第2版_套餐.__init__(self)
        print('腾讯套餐接口')
        self.生成单项字典()
        self.生成机构字典()
        self.机构和统一对应表 = {}
        self.获取标签列表()
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
        org_phone = '机构电话', report_types='报告类型',
    )

    ''' 已测试通过 '''
    def 修改基础项(self, 单项id, 单项库类型='统一库', 设为基础项=False):
        ''' 单项库类型: '统一库', '机构库' '''
        updItem2BasicDTO = dict(itemId=单项id, basic=1 if 设为基础项 else 0, type=dict(统一库=1, 机构库=2)[单项库类型])
        r = self.put("tencent/basic-items", data=updItem2BasicDTO)
        msg = r.get('message') or str(r)
        if msg in ['OK', 'SUCCESS', '成功']:
            return '成功', msg
        else:
            return '失败', msg
    
    ''' 已测试通过 '''
    def 查询单项类型(self, 单项级别, 父级id=None, 单项名称=None):
        ''' 单项级别: 1, 2 '''
        params = dict(groupLevel=单项级别, groupName=单项名称, parentId=父级id, per=1)
        params['per'] = self.get("tencent/item-groups", params=params)['total']
        data = self.get("tencent/item-groups", params=params)['data']
        for x in data:
            x['单项id'] = x.pop('组id')
            x['单项名称'] = x.pop('组名称')
        self.转中文(data)
        return data

    ''' 已测试通过 '''
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

    ''' 已测试通过 '''
    def 新增或修改二级单项(self, 一级单项id, 二级单项id=None, 单项名称=None):
        itemGroupDTO = dict(parentId=一级单项id, groupId=二级单项id, groupName=单项名称)
        r = self.post("tencent/item-group", data=itemGroupDTO)
        if not 二级单项id:  # 如果是新增
            self.生成单项字典()
        msg = r.get('message') or str(r)
        if msg in ['OK', '提交的类型名称已存在,请修改后重新提交', 'SUCCESS', '单项类型名称已存在', '成功']:
            return '成功', msg
        else:
            return '失败', msg

    ''' 已测试通过 '''
    def 查询统一单项(self, 二级单项id=None):
        params = dict(groupId=二级单项id, per=1)
        params['per'] = self.get("tencent/mutual-items", params=params)['total']
        return self.get("tencent/mutual-items", params=params)['data']
    
    ''' 已测试通过 '''
    def 查询统一基础项(self):
        return self.get("tencent/mutual-basic-items")['data']
    
    ''' 已测试通过 '''
    def 新增或修改统一单项(self, 二级单项id, 单项名称, 单项id=None, 描述=None, 设为基础项=None):
        mutualItemDTO = dict(groupId=二级单项id, mutualItemId=单项id, mutualItemName=单项名称)
        if 描述 != None:
            mutualItemDTO['mutualItemDesc'] = 描述
        if 设为基础项 != None:
            mutualItemDTO['basic'] = 1 if 设为基础项 else 0
        r = self.post("tencent/mutual-item", data=mutualItemDTO)
        msg = r.get('message') or str(r)
        if msg in ['OK', '提交的类型名称已存在,请修改后重新提交', '成功', '统一单项名称已存在', 'SUCCESS']:
            return '成功', msg
        else:
            return '失败', msg
    
    ''' 已测试通过 '''
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
                self.新增或修改二级单项(一级单项id=一级单项id, 单项名称=二级单项名称)
                二级单项id = self.单项字典[一级单项名称]['二级单项'][二级单项名称]['二级单项id']
            x['状态'], x['msg'] = self.新增或修改统一单项(二级单项id=二级单项id, 单项名称=三级单项名称, 设为基础项=设为基础项)
        print()
        self.生成单项字典()
        return kws
    
    ''' 已测试通过 '''
    def 查询机构基础项(self, 机构id):
        params = dict(orgId=机构id)
    
    ''' 已测试通过 '''
    def 新增或修改机构单项(self, 机构id, 二级单项id, 单项名称, 单项id=None, 设为基础项=None, 描述=None):
        orgItemDTO = dict(orgId=机构id, groupId=二级单项id, orgItemName=单项名称, orgItemId=单项id)
        if 描述 != None:
            orgItemDTO['orgItemDesc'] = 描述
        if 设为基础项 != None:
            orgItemDTO['basic'] = 1 if 设为基础项 else 0
        r = self.post("tencent/org-item", data=orgItemDTO)
        msg = r.get('message') or str(r)
        if msg in ['OK', '该机构下已存在当前项目名称，请核对数据', '成功', 'SUCCESS']:
            return '成功', msg
        else:
            return '失败', msg

    ''' 已测试通过 '''
    def 查询机构单项(self, 二级单项id=None, 机构id=None, 单项名称=None):
        params = dict(groupId=二级单项id, orgId=机构id, orgItemName=单项名称, per=1)
        params['per'] = self.get("tencent/org-items", params=params)['total']
        return self.get("tencent/org-items", params=params)['data']

    
    ''' 已测试通过 '''
    def 套餐列表(self, 机构id, 套餐名称=None, 上架=None, 创建时间范围=(None, None)):
        params = dict(orgId=机构id, bizField=套餐名称, per=1)
        if 上架 != None:
            params['status'] = 1 if 上架 else 0
        params['per'] = self.get("tencent/packages", params=params)['total']
        data = self.get("tencent/packages", params=params)['data']
        f = lambda x: time.mktime(time.strptime(x, "%Y-%m-%d %H:%M:%S"))
        start_time = f(创建时间范围[0] or '1999-10-10 10:10:10')
        end_time = f(创建时间范围[1] or '2999-10-10 10:10:10')
        return [x for x in data if start_time <= f(x['创建时间']) <= end_time]
    
    ''' 已测试通过 '''
    def 套餐详情(self, 套餐id):
        params = dict(packageId=套餐id)
        data = self.get("tencent/package", params=params)['data']
        data['items'] = {x['label']: x['data']for x in data['items']}
        return data
    
    ''' 已测试通过 '''
    def 获取机构列表(self, 状态=None):
        params = dict()
        if 状态 != None:
            params['status'] = 1 if 状态 else 0
        params['per'] = self.get("tencent/orgs", params=params)['total']
        return self.get("tencent/orgs", params=params)['data']
    
    ''' 已测试通过 '''
    def 获取机构详情(self, 机构id):
        params = dict(orgId=机构id)
        data = self.get("tencent/org", params=params)['data']
        item = [('org_province', '省份id'), ('org_city', '城市id'), ('org_district', '区id')]
        for a, b in item:
            data[b] = data.pop(a) if a in data else None
        return data
    
    ''' 已测试通过 '''
    def 生成机构单项和统一单项对应表(self, 机构id):
        item = {}
        for 一级单项 in self.get("tencent/package-items", params=dict(orgId=机构id))['data']:
#             item[一级单项['组名称']] = item[一级单项['组id']] = x_item = {}
            for 二级单项 in 一级单项['group_lv2']:
#                 x_item[二级单项['组名称']] = x_item[二级单项['组id']] = y_item = {}
                for x in 二级单项['items']:
#                     机构单项id, 机构单项名称 = [f"机构单项_{三级单项[z]}" for z in ('机构单项id', '机构单项名称')]
#                     统一单项id, 统一单项名称 = [f"统一单项_{三级单项[z]}" for z in ('统一单项id', '统一单项名称')]
#                     y_item[机构单项id] = y_item[机构单项名称] = y_item[统一单项id] = y_item[统一单项名称] = 三级单项
                    item[f"机构单项id_{x['机构单项id']}"] = x
                    item[f"统一单项id_{x['统一单项id']}"] = x
                    item[f"机构单项名称_{x['机构单项名称']}"] = x
                    item[f"统一单项名称_{x['统一单项名称']}"] = x
        self.机构和统一对应表[机构id] = item
        return item
    
    ''' 已测试通过 '''
    def 拉取统一单项到机构单项(self, 机构id, 统一单项ids):
        统一单项ids = [dict(mutualItemId=x) for x in 统一单项ids]
        data = dict(orgId=机构id, items=统一单项ids)
        r = self.post("tencent/push-org-item", data=data)
        self.生成机构单项和统一单项对应表(机构id=机构id)
        msg = r.get('message') or str(r)
        if msg in ['OK', '成功', 'SUCCESS']:
            return '成功', msg
        else:
            return '失败', msg

    ''' 已测试通过 '''
    def 生成机构字典(self):
        print('正在生成机构字典..')
        self.机构字典 = 机构字典 = {}
        for x in self.获取机构列表():
            机构id, 机构名称, 机构状态 = [x[y] for y in ('机构id', '机构名称', '机构状态')]
            机构字典[机构id] = 机构字典[机构名称] = dict(机构id=机构id, 机构名称=机构名称, 机构状态=机构状态)
    
    ''' 已测试通过 '''
    def 删除套餐(self, 机构id, 套餐id):
        data = {'bigPicture': None, 'genders': None, 'orgId': 机构id, 'packageName': 'test', 'packageId': 套餐id,
                'packagePrice': 99999999.0, 'packageStatus': 0, 'packagesItems': None, 'smallPicture': None}
        r = self.put("tencent/package", data=data)
        msg = r.get('message') or str(r)[:100]
        if msg in ['OK', 'SUCCESS', '成功']:
            return '成功', msg
        else:
            return '失败', msg

    def 匹配特色标签(self, 项目):
        项目规则 = [
            ('外科', '外科'), ('肝功', '肝功能'), ('糖尿', '糖尿病'), ('眼', '眼科'), ('基因', '基因检测'),
            ('肿瘤和癌', '肿瘤筛查'), ('胃镜', '胃镜'), ('肠镜', '肠镜'), ('心肌', '心肌功能'),
            ('肾功', '肾功能'), ('甲功', '甲状腺功能')
        ]
        return [y for x, y in 项目规则 if x in 项目]
    
    ''' 已测试通过 '''
    def 清空机构套餐(self, 机构id):
        if type(机构id) is str:
            机构id = self.机构字典[机构id]['机构id']
        rs = []
        for x in [x['套餐id'] for x in self.套餐列表(机构id=机构id)]:
            rs.append(self.删除套餐(机构id=机构id, 套餐id=x))
            print(set(rs))
    
    ''' 已测试通过 '''
    def 新增套餐(self, 机构s, 套餐名称字段, 性别字段, 套餐价格字段, 年龄字段,
                图片字段, 单项字段, 上架字段, 套餐id字段=None, 描述字段=None):
        套餐性别字典 = {x['标签名称']:x['标签代号'] for x in self.获取标签列表('package_gender')}
        套餐性别字典['已婚女'] = 套餐性别字典['女已婚']
        套餐性别字典['未婚女'] = 套餐性别字典['女未婚']
        alldata = []
        for 机构名称, 套餐s in 机构s.items():
            机构id = self.机构字典[机构名称]['机构id']
            jt对应表 = self.生成机构单项和统一单项对应表(机构id)
            
            for 套餐 in 套餐s:
                套餐id, 套餐名称, 描述 = [套餐.get(x) for x in (套餐id字段, 套餐名称字段, 描述字段)]
                
                性别 = [套餐性别字典[x] for x in set(套餐.get(性别字段) or [])]
                性别中文 = [x for x in set(套餐.get(性别字段) or [])]
                套餐价格 = 套餐[套餐价格字段] * 100
                上架 = 1 if 套餐.get(上架字段) else 0
                
                # 年龄标签
                年龄 = list(套餐.get(年龄字段) or [])
                if ('入职' in 套餐名称) or ('招工' in 套餐名称):
                    年龄.append('入职体检')
                if ('婚前' in 套餐名称) or ('孕前' in 套餐名称) or ('优生' in 套餐名称):
                    年龄.append('婚检孕检')
                年龄 = set(年龄)
                

                图片 = random.sample(self.图片库[套餐.get(图片字段)], 1)[0]
                大图 = f"https://img.tijian8.com/tha/package/origin/{图片}"
                小图 = f"https://img.tijian8.com/tha/package/sm/{图片.replace('.', '_SM.')}"
                
                单项参数 = []
                单项s = set(套餐.get(单项字段) or [])
                for 单项 in 单项s:
                    统一单项id = self.统一单项字典.get(单项) or self.统一单项字典.get(re.sub(' +$', '', 单项)) or self.统一单项字典[单项]
                    机构单项id = jt对应表.get(f"统一单项id_{统一单项id}", {}).get('机构单项id')
                    if not 机构单项id:
                        self.拉取统一单项到机构单项(机构id=机构id, 统一单项ids=[统一单项id])
                        机构单项id = self.机构和统一对应表[机构id][f"统一单项id_{统一单项id}"]['机构单项id']
                    单项参数.append(dict(mutualItemId=统一单项id, orgItemId=机构单项id))
                项目标签 = self.匹配特色标签(项目=''.join(单项s).replace(' ', ''))

                self.重置套餐标签(套餐id=None, 项目标签=项目标签, 人群标签=年龄, 性别标签=性别, 上传=False)  # 只验证, 不上传

                data = dict(bigPicture=大图, genders=性别, orgId=机构id, packageName=套餐名称, packagePrice=套餐价格,
                            packageStatus=上架, packagesItems=单项参数, smallPicture=小图)
                if 描述 != None:
                    data['description'] = 描述
                if 套餐id != None:
                    data['packageId'] = 套餐id
                
                alldata.append((data, 年龄, 项目标签, 性别))

        成功, 上传套餐失败, 添加标签失败 = [], [], []
        for data, 年龄, 项目标签, 性别 in alldata:
            机构id, 套餐名称 = data['orgId'], data['packageName']
            套餐id_old = set([x['套餐id'] for x in self.套餐列表(机构id=机构id, 套餐名称=套餐名称)])
            
            r = self.put("tencent/package", data=data)
            msg = r.get('message') or str(r)[:100]
            print(机构id, 套餐名称, msg)
            
            if msg in ['OK', 'SUCCESS', '成功']:
                套餐id_new = set([x['套餐id'] for x in self.套餐列表(机构id=机构id, 套餐名称=套餐名称)])
                套餐id = list(套餐id_new - 套餐id_old)
                if len(套餐id) == 1:
                    套餐id = 套餐id[0]
                    标签状态, 标签msg = self.重置套餐标签(套餐id=套餐id, 项目标签=项目标签, 人群标签=年龄, 性别标签=性别, 上传=True)
                    if 标签状态 == '成功':
                        成功.append((msg, data, 年龄, 项目标签, 性别, 标签msg))
                    else:
                        添加标签失败.append((msg, data, 年龄, 项目标签, 性别, 标签msg))
                else:
                    添加标签失败.append((msg, data, 年龄, 项目标签, 性别, f'套餐id:{套餐id}'))
            else:
                上传套餐失败.append((msg, data, 年龄, 项目标签, 性别))
        return dict(成功=成功, 上传套餐失败=上传套餐失败, 添加标签失败=添加标签失败)
    
    ''' 已测试通过 '''
    def 获取标签列表(self, group_key=None):
        r = self.get("tencent/tag/List", params=dict(groupKey=None))['data']
        self.标签字典 = item = {}
        for x in r:
            type_ = x['group_key']
            if type_ not in item:
                item[type_] = {}
            item[type_][x['标签id']] = item[type_][x['标签名称']] = item[type_][x['标签代号']] = x
        item['项目'] = item['package_item']
        item['人群'] = item['package_group']
        item['性别'] = item['package_gender']
        item['机构等级'] = item['org_rank']
        item['机构类型'] = item['org_level']
        if group_key:
            return [x for x in r if x['group_key'] == group_key]
        else:
            return r

    def 新增标签(self, 标签组, 标签代号, 标签名称):
        data = dict(groupKey=标签组, tagCode=标签代号, tagName=标签名称)
        r = self.post("tencent/tag", data=data)
        msg = r.get('message') or str(r)
        if msg in ['OK', 'SUCCESS', '成功']:
            self.获取标签列表()
            return '成功', msg
        else:
            return '失败', msg
    
    ''' 已测试通过 '''
    def 从Excel上传套餐(self, path, 唯一识别字段='唯一识别', 机构字段='医院名称', 套餐名称字段='套餐名称',
                   单项名称字段='单项库叫法', 上架字段='上架', 套餐价格字段='价格', 图片字段='图片', 性别字段='性别',
                  年龄字段='适用年龄', 清空旧套餐=False, 挂网折扣字段='挂网折扣'):
        df = pd.read_excel(path)
        
        # 检查字段是否齐全
        字段s = df.columns.to_list()
        for x in ('唯一识别', '医院名称', '套餐名称', '单项库叫法', '价格', '图片', '性别', '适用年龄', '挂网折扣'):
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
        
        # 提取所需数据
        机构s = {}
        for 标识符, df in df.groupby(唯一识别字段):
            for 机构名称, df in df.groupby(机构字段):
                if 机构名称 in 机构s:
                    套餐s = 机构s[机构名称]
                else:
                    机构s[机构名称] = 套餐s = []
                for 套餐名称, df in df.groupby(套餐名称字段):
                    套餐 = df.iloc[0].to_dict()
                    套餐[单项名称字段] = re.split(' *\[SEP\] *| *\[SEG\] *', '[SEP]'.join(list(df[单项名称字段])).replace('|', '[SEP]'))
                    套餐[上架字段] = True if 套餐.get(上架字段, '是') in ['是', True, 1] else False
                    套餐[性别字段] = [y for x in list(df[性别字段]) for y in re.split(' +', x)]
                    套餐[年龄字段] = [y for x in list(df[年龄字段]) for y in re.split(' +', x)]
                    套餐[套餐价格字段] = float(套餐[套餐价格字段]) * float(套餐[挂网折扣字段]) / 100
                    套餐s.append(套餐)
        
        if 清空旧套餐:
            for 机构名称 in 机构s:
                self.清空机构套餐(机构id=机构名称)
        
        return self.新增套餐(机构s=机构s, 套餐名称字段=套餐名称字段, 性别字段=性别字段, 套餐价格字段=套餐价格字段,
                图片字段=图片字段, 单项字段=单项名称字段, 上架字段=上架字段, 年龄字段=年龄字段)
    
    ''' 已测试通过 '''
    def 重置套餐标签(self, 套餐id, 项目标签=[], 人群标签=[], 性别标签=[], 上传=True):  # 同类型的原有标签将被清空
        项目标签代号 = [self.标签字典['项目'][x]['标签代号'] for x in set(项目标签 or [])]
        人群标签代号 = [self.标签字典['人群'][x]['标签代号'] for x in set(人群标签 or [])]
        性别标签代号 = [self.标签字典['性别'][x]['标签代号'] for x in set(性别标签 or [])]
        if 上传:
            rs = {}
            if 项目标签代号:
                data = dict(codes=项目标签代号, groupKey=2, packageId=套餐id)
                rs['项目'] = self.post("tencent/package/tag", data=data)
            if 性别标签代号:
                data = dict(codes=性别标签代号, groupKey=0, packageId=套餐id)
                rs['性别'] = self.post("tencent/package/tag", data=data)
            if 人群标签代号:
                data = dict(codes=人群标签代号, groupKey=1, packageId=套餐id)
                rs['人群'] = self.post("tencent/package/tag", data=data)
            for r in rs.values():
                if r['message'] not in ['SUCCESS', '成功']:
                    return '失败', str(rs)
            else:
                return '成功', str(rs)
    
    def 套餐转参数(self, 机构id, 套餐id):
        t = self.套餐详情(套餐id=套餐id)
        data = dict(
            bigPicture = t['大图'],
            description = t['描述'],
            genders = [x['gender_code'] for x in t['性别']],
            orgId = 机构id,
            packageId = 套餐id,
            packageName = t['套餐名称'],
            packagePrice = t['套餐价格'],
            packageStatus = t['套餐状态'],
            packagesItems = [dict(mutualItemId=y['统一单项id'], orgItemId=y['机构单项id']) for x in t['items'].values() for y in x],
            salesVolume = t['销售量'],
            smallPicture = t['小图']
        )
        
        bq = t['tags']
        标签 = dict(
            套餐id = 套餐id,
            项目标签 = [x['text'] for x in bq['标签项目']],
            人群标签 = [x['text'] for x in bq['标签组']],
            性别标签 = [x['text'] for x in bq['标签性别']]
        )
        return dict(套餐=data, 标签=标签)

    def 修改机构信息(self, 机构id, olddata=None, **kvs):
        if True:
            未验证
        kvs = {k: v for k, v in kvs.items() if v is not None}
        data = olddata or self.获取机构详情(机构id=机构id)
        newdata = dict(
            cityName = kvs.get('城市名称', data['城市']),
            districtName = kvs.get('地区名称', data['区']),
            orgAddress = kvs.get('地址', data['机构地址']),
            orgCity = kvs.get('城市id', data['城市id']),
            orgDistrict = kvs.get('地区id', data['区id']),
            orgId = 机构id,
            orgLevel = kvs.get('机构等级', data['机构等级']),
            orgName = kvs.get('机构名称', data['机构名称']),
            orgPhone = kvs.get('机构电话', data['机构电话']),
            orgPicture = kvs.get('机构图片', data['机构图片']),
            orgProvince = kvs.get('省份id', data['省份id']),
            orgRank = kvs.get('机构排名', data['机构排名']),
            orgStatus = kvs.get('机构状态', data['机构状态']),
            provinceName = kvs.get('省份', data['省份']),
            reportTypes = ','.join([x['id'] for x in data['报告类型']]),
        )
        r = self.put("alibaba/package", data=newdata)
        if r['message'] in ('SUCCESS', ):
            return True
        else:
            print(机构id, r)
            return dict(机构id=机构id, 参数=deepcopy(newdata), r=r)
