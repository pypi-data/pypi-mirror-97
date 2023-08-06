import requests, time, re

class 起点系统爬虫():
    cookie = ''  # 只要账号密码不修改, cookie就不需要更换
    
    def __init__(self, cookie=None):
        if cookie: self.cookie = cookie
    
    def 获取关键词(self, **kw):
        url = 'http://youhua.gsyjiao.com/API/Words/RankDataByDay'
        headers = {
            'ccept': 'application/json, text/javascript, */*; q=0.01',
            'Accept-Encoding': 'gzip, deflate',
            'Accept-Language': 'zh-CN,zh;q=0.9',
            'Connection': 'keep-alive',
            'Content-Length': '123',
            'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
            'Cookie': self.cookie,
            'Host': 'youhua.gsyjiao.com',
            'Origin': 'http://youhua.gsyjiao.com',
            'Referer': 'http://youhua.gsyjiao.com/New/WordsStat/List',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/78.0.3904.108 Safari/537.36',
            'X-Requested-With': 'XMLHttpReques'
        }
        data  = dict(
            wordName = None, domainName = None, Url = None, comName = None,
            rankDate1 = None,  # 查询日期 '2020-09-16'
            rankNum = 0, undefined = -1, rankType = -1, WordsType = -1,
            page = 1, pagesize = 15,  # 最大不能超过5000
        )
        data.update(kw)
        if data['pagesize'] > 5000:
            print('最大不能超过5000')
            return None
        if not data['rankDate1']:
            print('rankDate1查询日期不能为空, 格式: 2020-09-16')
            return None
        r = requests.post(url, headers=headers, data=data).json()
        for x in r['Items']: x['kwid'] = x.pop('WordID')
        return r

    def 智能提取关键词(self, 日期):
        kws = []
        page_total = ''
        for page in range(1, 100):
            print(f'\r正在获取第{page}/{page_total}页    ', end='')
            ikws = self.获取关键词(rankDate1=日期, page=page, pagesize=5000)
            kws += ikws['Items']
            page_total = ikws['TotalPageCount']
            if page >= page_total:
                break
        print('\n提取完成')
        return kws


class 代理商关键词():
    cookie = ''
    
    def __init__(self, cookie=None):
        if cookie: self.cookie = cookie
    
    def 获取关键词(self, 代理商=None, pagesize=None, page=None):
        url = 'http://youhua.gsyjiao.com/API/Words/ComAgentWordsData'
        headers = {
            'Accept': 'application/json, text/javascript, */*; q=0.01',
            'Accept-Encoding': 'gzip, deflate',
            'Accept-Language': 'zh-CN,zh;q=0.9',
            'Connection': 'keep-alive',
            'Content-Length': '174',
            'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
            'Cookie': self.cookie,
            'Host': 'youhua.gsyjiao.com',
            'Origin': 'http://youhua.gsyjiao.com',
            'Referer': 'http://youhua.gsyjiao.com/New/Words/ComAgentWords',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/78.0.3904.108 Safari/537.36',
            'X-Requested-With': 'XMLHttpRequest'
        }
        data = dict(
            wordName = None, domainName = None, Url = None,
            LoginName = None, comName = None, onlyAgent = 0, ComAgent = 1, reachType = None,
            undefined = -1, rankType = -1, auditState = 99, IsEnabled = -1, rankNum = 0, WordsType = -1,
            page = 1,
            pagesize = 15,  # 最大不能超过5000
        )
        if 代理商: data['comName'] = 代理商
        if pagesize: data['pagesize'] = pagesize
        if page: data['page'] = page
        if data['pagesize'] > 5000: raise Exception('pagesize 最大不能超过5000')
        for i in range(20):
            try:
                r = requests.post(url, headers=headers, data=data).json()
                break
            except Exception as err:
                e = err
                time.sleep(20)
        else: raise e
        
        for x in r['Items']:
            x['代理商'] = x.pop('ComName')
            x['kwid'] = x.pop('UID')
            x['kw'] = x.pop('Name')
            x['domain'] = x.pop('DomainName')
            try:
                排名时间 = int(re.findall('\((\d+)\)', x.pop('RankTime'))[0]) / 1000
                x['排名时间'] = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(排名时间))
            except:
                x['排名时间'] = ''
        return r

    def 智能提取关键词(self, 代理商=None, count=None):
        kws = []
        page_total = ''
        pagesize = min(count or 1000, 1000)
        for page in range(1, 100000):
            print(f'\r正在获取第{page}{page_total}页', end='    ')
            ikws = self.获取关键词(代理商=代理商, pagesize=pagesize, page=page)
            for x in ikws['Items']: kws.append(x)
            page_total = f"/{ikws['TotalPageCount']}"
            if page >= ikws['TotalPageCount']: break
            if count and (len(kws) >= count): break
        if count and (len(kws) > count):
            kws = kws[:count]
        print('\n提取完成')
        return kws
