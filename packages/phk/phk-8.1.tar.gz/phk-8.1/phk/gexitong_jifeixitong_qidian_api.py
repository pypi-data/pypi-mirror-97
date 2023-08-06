# -!- coding: utf-8 -!-
import re, os, sys, requests, json, time, math, base64, traceback
from Crypto.Cipher import AES

class 起点计费系统api():
    AppKey = ""
    key = ''
    headers = {'Content-Type':'application/json', 'Connection': 'close'}
    审核字典 = {-1:-1, 0:0, 2:2, '全部':-1, True:2, False:0}
    启用字典 = {-1:-1, 0:0, 1:1, '全部':-1, True:1, False:0}
    # 1:百度桌面, 2:360PC, 3:百度移动, 4:360移动, 5:搜狗PC, 6:搜狗移动, 7:神马
    搜索引擎字典 = {1:1, 2:2, 3:3, 4:4, 5:5, 6:6, 7:7, -1:-1, '全部':-1}
    覆盖字典 = {0:0, 1:1, True:1, False:0}
    请求失败日志路径 = ''
    
    def __init__(self, appkey='', key=''):
        if appkey: self.AppKey = appkey
        if key: self.key = key
    
    def aes_ecb_pkcs7(self, req):
        req = req + (16- len(req) % 16) * chr(16 - len(req) % 16)
        req = str.encode(req)
        aes = AES.new(str.encode(self.key), AES.MODE_ECB)
        encrypted_text = str(base64.encodebytes(aes.encrypt(req)), encoding='utf8').replace('\n', '')
        decrypted_text = str(aes.decrypt(base64.decodebytes(bytes(encrypted_text, encoding='utf8'))).rstrip(b'\0').decode("utf8"))
        return encrypted_text
    
    def 请求服务器(self, url, datas):
        入参data = datas
        datas = {"AppKey": self.AppKey, "TimeStamp": math.floor(time.time()), "Data": datas}
        req = f'"{self.aes_ecb_pkcs7(json.dumps(datas))}"'
        for n in range(20):  # 因为计费系统的服务器太垃圾, 经常会无响应, 所以需要多次重试
            try:
                return requests.post(url, headers=self.headers, data=req).json()
            except Exception as err:
                print(err)
                e = err
                if 'Max retries exceeded with url' in str(err): time.sleep(1.5)
                # 服务器无响应时, request库不断进行重新请求, 于是便会导致连接过多
        if self.请求失败日志路径:
            try:
                with open(self.请求失败日志路径, 'r', encoding='utf8') as fa: text = fa.read()
            except: text = ''
            当前时间 = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
            text = f"{text}\n\n{当前时间} - {入参data}"
            with open(self.请求失败日志路径, 'w+', encoding='utf8') as fa: fa.write(text)
        raise e

    def 获取关键词(self, 审核=True, 启用=True, 搜索引擎='全部'):  # 返回结构: [{}, {}]
        r = ''
        for i in range(20):
            try:
                审核, 启用, 搜索引擎 = self.审核字典[审核], self.启用字典[启用], self.搜索引擎字典[搜索引擎]
                req = {"AuditState":审核, "RankType":搜索引擎, "PageSize": 30000, "PageNum": 1, 'IsEnabled':启用}
                r = self.请求服务器('http://api.235kk.com/api/Words', req)
                print('\n获取关键词'+r['message'], '  请求状态', r['state'], end='    ')
                d = r['data']
                print('总记录', d['TotalNum'], '   当前页', d['CurrentPage'], '   总页数', d['TotalPageCount'], '  ', d['OtherData'])
                r = d['Items']
                for x in r: x['kwid'] = x.pop('WordID')
                return r
            except:
                print(str(r)[:500])
                time.sleep(10)
        else:
            审核, 启用, 搜索引擎 = self.审核字典[审核], self.启用字典[启用], self.搜索引擎字典[搜索引擎]
            req = {"AuditState":审核, "RankType":搜索引擎, "PageSize": 30000, "PageNum": 1, 'IsEnabled':启用}
            r = self.请求服务器('http://api.235kk.com/api/Words', req)
            print('\n获取关键词'+r['message'], '  请求状态', r['state'], end='    ')
            d = r['data']
            print('总记录', d['TotalNum'], '   当前页', d['CurrentPage'], '   总页数', d['TotalPageCount'], '  ', d['OtherData'])
            r = d['Items']
            for x in r: x['kwid'] = x.pop('WordID')
            return r
    
    def 修改审核状态(self, kws):  # 传入结构: [{'kwid':kwid, '审核':True}, {'kwid':kwid, '审核':True}]
        kws = [dict(WordID=kw['kwid'], AuditState=self.审核字典[kw['审核']]) for kw in kws]
        r = self.请求服务器('http://api.235kk.com/api/WordsInfo', kws)
        print('\n修改审核状态  '+r['message'], '  请求状态:',r['state'], '  修改成功数量:',r['data'])
        return r['data']
    
    def 修改启用状态(self, kws):  # 传入结构 [{'kwid':kwid, '启用':True, '说明':说明}]
        kws = [dict(WordID=k['kwid'], State=self.启用字典[k['启用']], Remark=k['说明']) for k in kws]
        r = self.请求服务器('http://api.235kk.com/api/WordsEnable', kws)
        print('\n关键词禁用接口  ' + r['message'], '  请求状态:', r['state'], '  修改成功数量:', r['data'])
    
    def 提交排名(self, kws):  # 传入结构 [{'kwid':kwid, '排名':排名, '时间':时间, '覆盖':False}]
        kws = [dict(WordID=k['kwid'], RankNum=k['排名'], RankTime=k['时间'], IsOverride=self.覆盖字典[k.get('覆盖', False)]) for k in kws]
        r = self.请求服务器('http://api.235kk.com/api/WordsRank', kws)
        print('\n修改排名  '+r['message'], '  请求状态:', r['state'], '  修改成功数量:', r['data'])
        r = r['data']
        return r

    def 根据关键词查询kwid(self, kws, 关键词字段='kw', 域名字段='domain', kwid字段='WordID'):
        allkw = self.获取关键词(审核='全部', 启用='全部', 搜索引擎='全部')
        allkw = {(k['Name'], k['DomainName']):k['WordID'] for k in allkw}
        for k in kws:
            k[kwid字段] = allkw.get((k[关键词字段], k[域名字段]))
        return kws
