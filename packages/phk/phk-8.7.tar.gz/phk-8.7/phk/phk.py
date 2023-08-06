import jieba, re
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

class phk:

    class 数据类型:
        def time():
            from phk.data_type import 数据类型
            return 数据类型.time
    
    class 善检网:
        class 供应链:
            def api():
                from phk.shanjianwang_gongyinglian_api import 供应链api
                return 供应链api
        class api第2版():
            class 财务():
                def api():
                    from phk.shanjianwang_api2_caiwu import 善检网api第2版_财务
                    return 善检网api第2版_财务
            class 套餐():
                def 腾讯():
                    from phk.shanjianwang_api2_taocan_tengxun import 善检网api第2版_套餐_腾讯
                    return 善检网api第2版_套餐_腾讯
                def 阿里():
                    from phk.shanjianwang_api2_taocan_ali import 善检网api第2版_套餐_阿里
                    return 善检网api第2版_套餐_阿里
                def 百度():
                    from phk.shanjianwang_api2_taocan_baidu import 善检网api第2版_套餐_百度
                    return 善检网api第2版_套餐_百度

    class 站群系统:
        class 设置相似文章:
            def 在相同分类中推荐():
                from phk.zhanqun_shezhi_xiangsi_wenzhang import 设置相似文章
                return 设置相似文章

    class 算法:
        def dfa():
            from phk.dfa import dfa
            return dfa

    class webtool:
        def tool():  # 网络操作工具
            from phk.webtool import webtool
            return webtool
        
    class 爬虫:
        def 基础爬虫():
            from phk.req_base import req_base
            return req_base
        
        class 百度:
            def pc():
                from phk.req_baidu_pc import req_baidu_pc
                return req_baidu_pc

    class seo:
        class 百度:
            def pc():
                from phk.seo_baidu_pc import seo_baidu_pc
                return seo_baidu_pc

    class localtool:
        
        def tool():  # 本地操作工具
            from phk.tool import tool
            return tool

        def 装饰器():
            from phk.deco import 装饰器
            return 装饰器
        
        def 自动任务():
            from phk.autotask import 自动任务
            return 自动任务
    
    class 第三方平台:

        class 百度:
            class ai开放平台:
                def 百度aip():
                    from phk.baidu_aip import baidu_aip
                    return baidu_aip

        class 计费系统:
            class 起点:
                def api():
                    from phk.gexitong_jifeixitong_qidian_api import 起点计费系统api
                    return 起点计费系统api
                def 爬虫():
                    from phk.gexitong_jifeixitong_qidian_pachong import 起点系统爬虫
                    return 起点系统爬虫
                def 代理商关键词():
                    from phk.gexitong_jifeixitong_qidian_pachong import 代理商关键词
                    return 代理商关键词
    
    class 数据库:
        class mysql:
            def orm2():
                from phk.orm_mysql_2 import orm_mysql
                return orm_mysql

            def tool():
                from phk.pmysql import pmysql
                return pmysql

            def orm():
                from phk.orm_mysql import orm_mysql
                print('orm 模仿 pandas 的过滤器, 因此也延续了pandas的重大缺陷')
                print('此版本的orm已停止维护, 导入 phk.数据库.mysql.orm2() 使用最新版本的orm')
                return orm_mysql

    # 兼容张工代码
    def 字符串排列(text, long=3, 不拆分=[]):
        # long: 返回时, 将排除 len(x) < long 的组合
        # 不拆分: 作为一个不可分割的最小字符, 不进一步拆分的词
        for x in 不拆分: jieba.add_word(x)
        text = ''.join(re.findall('[\u4e00-\u9fa5a-zA-Z]', text))  # 去掉所有空格和符号
        kws = list(set(jieba.cut(text)))
        total = len(kws)
        # 排列组合
        list_all = kws.copy()
        for i1 in range(0, total-1):
            for i2 in range(i1+1, total):
                list_all.append(kws[i1] + kws[i2])
        # 去重和按字数过滤
        list_all = [x for x in set(list_all) if len(x) >= long]
        return list_all

    # 兼容张工代码
    def sqlalchemy执行sql(mysql_url, sqls):
        engine = create_engine(mysql_url, encoding='utf-8')  # 创建的数据库引擎
        DBSession = sessionmaker(bind=engine)  #创建session类型
        session = DBSession()  #创建session对象，进行增删改查:
        rs = {}
        for sql in sqls:
            r = session.execute(sql)
            try:
                rs[sql] = [dict(zip(result.keys(), result)) for result in r]
                print(f'{sql} --> done')
            except Exception as err:
                rs[sql] = str(err)
                print(f'{sql} --> {err}')
        session.commit()
        session.close()
        return rs
