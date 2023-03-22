""" loadDict从文本将词典载入内存
"""

def loadDict(fname):
     # set是集合类型，其中的元素不会重复
     # 因此当需要找出各自不同的元素或过滤掉不想要的元素是可以使用set
     # set 查找速度快O(1)复杂度
    words = set()
    f = open(fname,'r',encoding='utf-8')             # 读文件
    lines = f.readlines()
    f.close()                   # 记得关闭文件哦

    for line in lines:
        line = line.strip()     # 去掉两端的空白字符，如空格、回车等
        words.add(line)
        #words.add(line.decode('utf-8', 'ignore'))  # 转码，程序内全部是用Unicode编码

    return words


dictionary = loadDict("dictionary.txt")

""" 正向最大匹配算法(forward maximum match, fmm)
    参数1：待分词的字符串，要求类型为unicode
    参数2：词典
"""
def fmm_seg(sentence, dictionary):
    max_len = 7  # 最长词的长度
    result = []  # 结果列表，用于保存分词之后的结果
    start = 0    # 正向最大匹配，从0开始

    while start < len(sentence):
        end = min(start + max_len, len(sentence))  # 处理边界，句子的长度有数
        while end > 0:
            candidate = sentence[start:end]        # 获得一个候选
            #print("Candidate：", candidate)
            if candidate in dictionary or end == start + 1:  # 判断候选是否在词典中，或者长度是否为1，满足任意条件都匹配
                #print("找到一个词：", sentence[start: end])
                result.append(candidate)
                start = end    # 更新下次开始匹配的位置
                break         # 当前匹配成功，跳出循环！
            else:
                end -= 1

    return result


""" 逆向最大匹配算法(backward maximum match, bmm)
    参数1：待分词的字符串，要求类型为unicode
    参数2：词典
"""
def bmm_seg(sentence, dictionary):
    max_len = 7  # 最长词的长度
    result = []
    end = len(sentence)  #从后向前扫描，因此end表示结束位置
    while end > 0:
        start = max(end - max_len, 0)  # 从后向前决定起始位置，注意下标不要小于0
        while start < end:
            candidate = sentence[start:end]
            #print("candidate：", candidate)
            if candidate in dictionary or end == start + 1:
                #print("找到一个词：", sentence[start: end])
                result.append(candidate)
                end = start
                break
            else:
                start += 1

    result.reverse()     # 结果是逆序的，所以调转一下。用list自带的函数reverse，非常简单的呦！
    return result

if __name__ == "__main__":
    results_bmm = bmm_seg(u'我们在野生动物园玩', dictionary)
    results_fmm = bmm_seg(u'我们在野生动物园玩', dictionary)

    # join是字符串操作过程中常用的一个函数，可以将一个列表中的各个字符串拼接起来，返回一个字符串
    # 拼接符.join(列表)
    print("FMM: ", " / ".join(results_fmm))
    print("BMM: ", " / ".join(results_bmm))
