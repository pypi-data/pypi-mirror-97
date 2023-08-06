import jieba, re, random, requests
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from .phk import phk
百度class = phk.seo.百度.pc()


字符串排列 = phk.字符串排列
sqlalchemy执行sql = phk.sqlalchemy执行sql


class 网站综合得分(百度class):
    # 可自定义的变量
    站长api = '...{domain}...'
    rn = 10
    网址智能协议 = 'http'  # str
    域名智能前缀 = ['www', 'm', 'wap']  # 若url前缀不在此列表中, 则自动添加前缀
    搜索词最大长度 = 30  # len(f"{title} {域名中间}")
    打印查询结果 = False

    # 固有属性, 勿动!
    无排名返回 = False
 
    def __组合site搜索词(self, title, domain):
        域名中间 = domain.split('.')[-2]
        域名长度 = len(域名中间) + 1  # +1是因为title和domain之间有1个空格
        搜索词 = f"{title[:self.搜索词最大长度 - 域名长度]} {域名中间}"
        return 搜索词

    def url_get_各项数据(self, url):
        print(f"\r{url}", end='    ')
        item = dict(入参url=url)
        url = self.url_get_完整url(url)
        domain = self.url_get_domain(url)
        item['实际url'] = url
        item['实际domain'] = domain
        item['查询rn'] = self.rn
        # site收录量
        print(f"\r正在获取 site收录量", end='    ')
        item['site收录量'] = self.kw_get_num(f'site: {domain}')
        print(f"\r正在获取 title", end='    ')
        item['title'] = title = self.url_get_title(url)
        # 标题排名
        item['title排名'] = False
        if title:
            print(f"\r正在获取 title排名", end='    ')
            搜索词 = self.__组合site搜索词(title, domain)
            item['title排名'] = self.kw_get_ranking(kw=搜索词, domain=domain)
        # 内页标题排名
        item['内页标题排名'] = False
        title = ''
        print(f"\r正在搜索 site:{domain}", end='    ')
        res = self.html_get_results(self.r_get_html(self.搜索(f"site:{domain}")))
        for x in sorted(res.keys()):
            x = res[x]
            if self.url_get_是否内页(x.get('底部文字') or ''):  # 判断是否是内页
                title = x.get('顶部文字')
                if title:
                    print(f"\r正在获取 内页标题排名", end='    ')
                    搜索词 = self.__组合site搜索词(title, domain)
                    item['内页标题排名'] = self.kw_get_ranking(kw=搜索词, domain=domain)
                    break
        # 获取站长权重和关键词数量
        print(f"\r正在获取 站长权重和关键词数量", end='    ')
        r = requests.get(self.站长api.format(domain=domain)).json()['Result']
        item['站长权重'] = r['Br']
        item['站长关键词数量'] = r['Kwcount']
        return item

def random_name():
    xing = '赵钱孙李周吴郑王冯陈褚卫蒋沈韩杨朱秦尤许何吕施张孔曹严华金魏陶姜戚谢邹喻柏水窦章云苏潘葛' \
           '奚范彭郎鲁韦昌马苗凤花方俞任袁柳酆鲍史唐费廉岑薛雷贺倪汤滕殷罗毕郝邬安常乐于时傅皮卞齐康' \
           '伍余元卜顾孟平黄和穆萧尹姚邵湛汪祁毛禹狄米贝明臧计伏成戴谈宋茅庞熊纪舒屈项祝董梁杜阮蓝闵' \
           '席季麻强贾路娄危江童颜郭梅盛林刁钟徐邱骆高夏蔡田樊胡凌霍虞万支柯昝管卢莫经房裘缪干解应宗' \
           '丁宣贲邓郁单杭洪包诸左石崔吉钮龚程嵇邢滑裴陆荣翁荀羊於惠甄曲家封芮羿储靳汲邴糜松井段富巫' \
           '乌焦巴弓牧隗山谷车侯宓蓬全郗班仰秋仲伊宫宁仇栾暴甘钭厉戎祖武符刘景詹束龙叶幸司韶郜黎蓟薄' \
           '印宿白怀蒲邰从鄂索咸籍赖卓蔺屠蒙池乔阴鬱胥能苍双闻莘党翟谭贡劳逄姬申扶堵冉宰郦雍卻璩桑桂' \
           '濮牛寿通边扈燕冀郏浦尚农温别庄晏柴瞿阎充慕连茹习宦艾鱼容向古易慎戈廖庾终暨居衡步都耿满弘' \
           '匡国文寇广禄阙东欧殳沃利蔚越夔隆师巩厍聂晁勾敖融冷訾辛阚那简饶空曾毋沙乜养鞠须丰巢关蒯相' \
           '查后荆红游竺权逯盖益桓公万俟司马上官欧阳夏侯诸葛闻人东方赫连皇甫尉迟公羊澹台公冶宗政濮阳' \
           '淳于单于太叔申屠公孙仲孙轩辕令狐钟离宇文长孙慕容鲜于闾丘司徒司空丌官司寇仉督子车颛孙端木' \
           '巫马公西漆雕乐正壤驷公良拓跋夹谷宰父谷梁晋楚闫法汝鄢涂钦段干百里东郭南门呼延归海羊舌微生' \
           '岳帅缑亢况郈有琴梁丘左丘东门西门商牟佘佴伯赏南宫墨哈谯笪年爱阳佟第五言福'
    ming = '伟刚勇毅俊峰强军平保东文辉力明永健世广志义兴良海山仁波宁贵福生龙元全国胜学祥才发武新利清' \
           '飞彬富顺信子杰涛昌成康星光天达安岩中茂进林有坚和彪博诚先敬震振壮会思群豪心邦承乐绍功松善' \
           '厚庆磊民友裕河哲江超浩亮政谦亨奇固之轮翰朗伯宏言若鸣朋斌梁栋维启克伦翔旭鹏泽晨辰士以建家' \
           '致树炎德行时泰盛秀娟英华慧巧美娜静淑惠珠翠雅芝玉萍红娥玲芬芳燕彩春菊兰凤洁梅琳素云莲真环' \
           '雪荣爱妹霞香月莺媛艳瑞凡佳嘉琼勤珍贞莉桂娣叶璧璐娅琦晶妍茜秋珊莎锦黛青倩婷姣婉娴瑾颖露瑶' \
           '怡婵雁蓓纨仪荷丹蓉眉君琴蕊薇菁梦岚苑筠柔竹霭凝晓欢霄枫芸菲寒欣滢伊亚宜可姬舒影荔枝思丽秀' \
           '飘育馥琦晶妍茜秋珊莎锦黛青倩婷宁蓓纨苑婕馨瑗琰韵融园艺咏卿聪澜纯毓悦昭冰爽琬茗羽希'
    X = random.choice(xing)
    M = "".join(random.choice(ming) for i in range(random.randint(1, 2)))
    name = X + M
    return name


def 字符串分割(text, 分割符, 最少字数=1, 最大字数=100):
    ts = [re.sub('\s+$', '', re.sub('^\s+', '', x)) for x in text.split(分割符)]
    最少字数 = max(1, 最少字数)
    return [x for x in ts if 最大字数 >= len(x) >= 最少字数]

if __name__ == '__main__':
    字符串排列('数据恢复软件下载',2, ['数据恢复软件'])
    sqlalchemy执行sql('mysql+pymysql://...', ['select * from danju limit 2'])
