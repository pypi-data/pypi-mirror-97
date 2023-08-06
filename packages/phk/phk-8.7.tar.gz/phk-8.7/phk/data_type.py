# -!- coding: utf-8 -!-
import datetime, re, time, hashlib

class 数据类型():

    class time():
        
        def __init__(self, time):
            self.o_set_time(time)

        def o_set_time(self, o):  # 以秒为单位的时间戳
            if type(o) in (int, float):
                self.时间戳 = o
                self.时间字符 = self.时间戳转字符串(o)
                self.毫秒时间戳 = self.时间戳 * 1000
            elif type(o) is str:
                self.时间戳 = self.字符串转时间戳(o)
                self.时间字符 = self.时间戳转字符串(self.时间戳)
                self.毫秒时间戳 = self.时间戳 * 1000
            else:
                raise Exception('不支持的格式')
        
        def 字符串转时间戳(self, 字符串):
            return time.mktime(time.strptime('-'.join(re.findall('\d+', 字符串)), "%Y-%m-%d-%H-%M-%S"))

        def 时间戳转字符串(self, 时间戳):
            return time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(时间戳))
        
        def __str__(self): return str(self.时间字符)
        
        def __add__(self, count):
            return 数据类型.time(self.时间戳 + count)
        
        def 时间差(self, time):
            return self.时间戳 - 数据类型.time(time).时间戳
        
        def 偏移(self, s):
            return 数据类型.time(self.时间戳 + s)

if __name__ == '__main__':
    t = 数据类型.time

    现在 = t(time.time())
    print(现在.时间戳)
    print(现在.毫秒时间戳)
    print(现在.时间字符)
    print()

    刚才 = t('2021-02-01 10:10:10')
    print(刚才 + 100)  # 与 .偏移(100) 等价
    print(刚才.偏移(100))  # 与 + 100 等价
    print(刚才.时间差('2021-02-01 10:11:10'))
