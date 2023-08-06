# -!- coding: utf-8 -!-
import re, os, sys, smtplib, time
from email.mime.text import MIMEText
from email.header import Header

class webtool():
    账号s = {}

    class 电子邮箱():
        
        def __init__(self, 账号s={}):
            if 账号s: self.账号s = 账号s
        
        def 发邮件(self, 发件人, 接收人, 标题=None, 正文=None, 昵称=None, 发件人昵称=None, 最高次数=10, 重试间隔=10):
            # 昵称 和 发件人昵称 是一回事, 之所以同时出现这两个字段, 是为了兼容旧代码, 传任意1个字段即可
            发件人 = self.账号s[发件人]
            接收人 = [self.账号s[x]['账号'] for x in (接收人 if (type(接收人) is list) else [接收人])]
            接收人 = list(set(接收人))
            data = dict(
                发件人 = 发件人['账号'],
                授权码 = 发件人['授权码'],
                昵称 = 昵称 or 发件人昵称 or 发件人.get('昵称') or 发件人['账号'],
                标题 = 标题 or 正文 or '无',
                正文 = 正文 or 标题 or '无',
                接收人 = 接收人
            )
            for i in range(最高次数):
                try: return self.发邮件base(**data)
                except: time.sleep(重试间隔)
            return False
        
        def 发邮件base(self, 发件人, 授权码, 昵称, 标题, 正文, 接收人):
            服务器, 端口号 = 'smtp.qq.com', 465
            stmp = smtplib.SMTP_SSL(服务器, 端口号)
            stmp.login(发件人, 授权码)
            message = MIMEText(正文, 'plain', 'utf-8')
            message['Subject'] = Header(标题, 'utf-8')
            message['From'] = Header(昵称, 'utf-8')
            message['To'] = Header("管理员", 'utf-8')
            stmp.sendmail(发件人, 接收人, message.as_string())
            return True
