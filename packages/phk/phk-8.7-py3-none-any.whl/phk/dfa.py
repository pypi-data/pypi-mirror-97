# -!- coding: utf-8 -!-

class dfa():
    # 无意义词库,在检测中会跳过
    无意义词库 = {' ', '&', '!', '！', '@', '#', '$', '￥', '*', '^', '%', '?', '？', '<', '>', "《", '》'}
    词库 = {}

    def __init__(self, 敏感词库):
        for kw in 敏感词库: self.添加词库(kw)  # 添加词库

    def 添加词库(self, word):
        词库 = self.词库
        for kw in word:
            词库 = 词库.setdefault(kw, {'is_end': False})
        词库['is_end'] = True

    def 从指定的索引开始检测敏感词(self, text, 起始索引, 匹配模式='最长'):
        找到的索引 = []
        rlong = 0
        敏感词长度 = 0  # 包括特殊字符的敏感词的长度
        词库 = self.词库
        for i in range(起始索引, len(text)):
            word = text[i]
            if word in 词库:
                敏感词长度 += 1
                词库 = 词库[word]
                if 词库["is_end"]:
                    if 匹配模式 == '最长':
                        rlong = 敏感词长度
                    elif 匹配模式 == '最短':
                        return [敏感词长度]
                    elif 匹配模式 == '全部':
                        找到的索引.append(敏感词长度)
                    else:
                        raise Exception("匹配模式错误!")
            elif word in self.无意义词库:
                敏感词长度 += 1
            else:
                break
        return [rlong] if rlong else 找到的索引


    def 检测敏感词(self, text, 匹配模式='最长'):
        相匹配的词 = []
        for i in range(len(text)):
            找到的索引 = self.从指定的索引开始检测敏感词(text, i, 匹配模式=匹配模式)
            for x in 找到的索引: 相匹配的词.append(text[i: i + x])
        return 相匹配的词

if __name__ == '__main__':
    print(dfa(敏感词库=["七", "七分彩", '七分彩在线博赌']).检测敏感词('七分彩在线博赌', 匹配模式='最短'))
    print(dfa(敏感词库=["七", "七分彩", '七分彩在线博赌']).检测敏感词('七分彩在线博赌', 匹配模式='最长'))
    print(dfa(敏感词库=["七", "七分彩", '七分彩在线博赌']).检测敏感词('七分彩在线博赌', 匹配模式='全部'))
    # {'七'}
    # {'七分彩在线博赌'}
    # {'七分彩在线博赌', '七', '七分彩'}
