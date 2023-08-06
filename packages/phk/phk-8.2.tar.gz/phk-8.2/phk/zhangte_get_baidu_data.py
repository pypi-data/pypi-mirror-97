# 第三方库
import requests
import re
import pandas as pd
# 自发布的pip库
from phk.phk import phk
百度class = phk.seo.百度.pc()
爬虫class = phk.爬虫.基础爬虫()

# 初始化
baidu = 百度class()
url_get_title = 爬虫class().url_get_title

#编写思考逻辑过程

#需要至少3次提取百度源代码
#1. site:域名 , 主要的作用
    # * 提取收录量
    # * 判断排名的依据是熊掌号和还是普通域名
    # * 提取一个内页标题

#2. 输入首页标题,判断是否有排名 ( 主要根据第一步提取的判断依据来判断 )
#3. 输入内页标题,判断是否有排名 ( 返回一个item)




class GetBaiduData():
    def __init__(self,url):
        #初始化一个item,然后直接在这个item里面进行更新
        self.item = {
            '百度收录量':0,
            '首页标题降权':True,
            '内页标题降权':True,
                    }
        self.url = url
        self.P = 'http.+?//.+?/.+' #判断内页
    
    # 第一步执行逻辑
    def 更新收录量(self):
        self.html = baidu.搜索(f'site:{self.url}').text   # 这步执行以后,会获取一个html
        self.item['百度收录量'] = baidu.html_get_num(self.html)
        
    
    # 第2步 通过第一步的结果,获取排名判断依据,以及一个内页标题
    def 获取排名判断依据(self):
        # 获取排名判断依据 ( 看是通过熊掌号还是域名来判断 )
        results = baidu.html_get_results(self.html)
        df = pd.DataFrame(results).T  #搜索结果df
        
        if '.' not in df.iloc[0]['底部文字']:
            排名判断 = df.iloc[0]['底部文字']
        else:
            排名判断 = self.url +'/' # 因为底部文字如果是网址的话,就会有一个 /
        
        self.排名判断 = 排名判断
        
        
        if self.item['百度收录量'] > 1: #在大于1的情况下才会有内页标题
            df = df[df['底部文字'].str.contains(排名判断)]  # 过滤,如果该域名是熊掌号域名,就不判断非熊掌号
            
            # 判断是不是内页
            if len(df) > 1:
                # 过滤出非内页的df
                
                import requests
                for i in df.index:
                    rank_url = df['顶部链接'][i]
                    百度真实url = requests.head(rank_url).headers['Location']
                    
                    if re.findall(self.P,百度真实url): # 通过re,判断是不是内页,如果是内页,就直接返回
                        self.内页标题 = df['顶部文字'][i]
                        print ('有内页',self.内页标题)
                        return
                
                # 如果完成循环,就是没有内页...,所以就是降权状态
                self.内页标题 = False   
            else:
                self.内页标题 = False
                
    
    # 功能函数,获取网站的标题,用于获取首页标题
    def 获取网站标题(self,url):
        
        # 定义函数
        
        # 调用
        标题 = url_get_title(f'http://{url}')
        return 标题

    # 功能函数,百度html转df
    def 百度html转df(self,html):
        results = baidu.html_get_results(html)
        df = pd.DataFrame(results).T  #搜索结果df
        return df
    
    def domain_get_域名中间(self, domain):
        domain = baidu.url_get_domain(domain)
        域名中间 = domain.split('.')[-2]
        return 域名中间
    
    # 功能函数,输入一个标题,判断该标题是不是有排名
    def 判断标题排名(self,标题):
        域名中间 = self.domain_get_域名中间(self.url)
        html = baidu.搜索(标题 + ' ' + 域名中间).text
        df = self.百度html转df(html)
        
        过滤排名df = df[df['底部文字'].str.contains(self.排名判断)]
        if len(过滤排名df): #有排名
            return False
        else:
            return True
    
    
    # 组合函数
    def main(self):
        self.更新收录量()
        if self.item['百度收录量'] == 0:
            return self.item  #如果百度都没收录,就不用继续查了,首页标题和内页标题肯定没排名
        
        self.获取排名判断依据()
        # 判断是否标题是否降权
        首页标题 = self.获取网站标题(self.url)
        self.item['首页标题降权'] = self.判断标题排名(首页标题)
        
        内页标题 = self.内页标题
        self.item['内页标题降权'] = self.判断标题排名(内页标题)
        return self.item
    
def 获取网站数据(api, url):
    data = GetBaiduData(url)
    item = data.main()

    if item['百度收录量'] > 0:
        zhanzhang_api = api.format(url=url)
        data_zhanzhang = requests.get(zhanzhang_api).json()
        item['站长BR'] = data_zhanzhang['Result']['Br']
        item['站长词量'] = data_zhanzhang['Result']['Kwcount']
        item['站长预估流量'] = data_zhanzhang['Result']['Uvcount']
    else:
        item['站长BR'] = item['站长词量'] = item['站长预估流量'] = 0
    return item
