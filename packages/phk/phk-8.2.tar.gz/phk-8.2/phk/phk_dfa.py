import re
from .dfa import dfa


class phk_dfa(dfa):
    
    网址正则 = '\[[^])([]+\][(]https?://[\w./:]+[)]|https?://[\w./:]+'
    
    def 替换格式(self, 敏感词): return f'[{敏感词}]'

    def 替换(self, text, 敏感词):
        新词 = self.替换格式(敏感词)
        if 新词 in text:  # 替换过了, 不重复替换
            return text
        elif 敏感词 in str(re.findall(self.网址正则, text)):  # 敏感词在网址里面, 不替换
            return text
        return text.replace(敏感词, 新词)
    
    def 敏感词替换(self, text):
        敏感词s = set(self.检测敏感词(text=text, 匹配模式='最长'))
        for 敏感词 in 敏感词s:
            text = self.替换(text, 敏感词)
        return text
