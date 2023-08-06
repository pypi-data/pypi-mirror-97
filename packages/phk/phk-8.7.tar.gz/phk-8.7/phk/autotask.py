import re, os, sys, time
from apscheduler.schedulers.blocking import BlockingScheduler

class 自动任务():
    最大实例数量 = 100
    
    def __init__(self): self.任务池 = BlockingScheduler()
    
    # 间隔, 并非从任务完成后开始计算, 而是从任务开始时开始计算
    # 当 'max_instances' 键值对的值小于 任务时长/任务间隔 时，程序会报错。
    def 添加间隔任务(self, func, 间隔=(None, ) * 4, 开始时间=None, 结束时间=None):
        item = dict(func=func, trigger='interval', seconds=间隔, max_instances=self.最大实例数量)
        for k, v in zip(('days', 'hours', 'minutes', 'seconds'), 间隔):
            if v: item[k] = v
        if 结束时间: item['end_date'] = 结束时间  # '2019-11-30 21:30:00'
        十秒前 = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time() - 10))
        item['start_date'] = 开始时间 or 十秒前  # '2019-10-30 21:30:00'
        self.任务池.add_job(**item)
    
    def 添加周期任务(self, func, 周期=(None, ) * 6, 开始时间=None, 结束时间=None):
        item = dict(func=func, trigger='cron', max_instances=self.最大实例数量)
        for k, v in zip(('year', 'month', 'day', 'hour', 'minute', 'second'), 周期):
            if v: item[k] = v  # month='3-4,7-9', day='1-3', hour='3'
        if 开始时间: item['start_date'] = 开始时间  # '2019-11-30 21:30:00'
        if 结束时间: item['end_date'] = 结束时间
        self.任务池.add_job(**item)
    
    def 添加一次性任务(self, func, 时间):
        # 时间: '2019-10-30 21:30:00'
        self.任务池.add_job(func=func, trigger='date', run_date=时间, max_instances=self.最大实例数量)
    
    def 开始(self): self.任务池.start()
