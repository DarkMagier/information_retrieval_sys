
# 假设已经进行文本处理，将文档表示为词项列表
d0=["据", "报道", "计算机", "病毒", "最近", "猖獗", "计算机"]
d1=["邮件", "是", "电脑", "病毒", "传播", "途径", "之一", "电脑"]
d2=["小王", "在", "医院", "学习", "为了", "研究", "病毒", "整天", "坐", "在", "计算机", "前", "查", "资料"]
d3 = ["北京", "仁和", "医院", "病毒", "感冒"]
d4 = ["电脑", "技术", "科学", "计算机", "研究", "病毒"]
docs =[d0, d1, d2, d3,d4]

# 建立词典
def build_dictionary(docs):
    '''
    建立词典，并返回相关数据对象
    '''
    all_words = []  # 词的顺序列表
    word2id = {}    # 词到ID的映射
    word2docs = {}  # 记录包含词的文档集合

    # 遍历所有文档
    # 按照遍历顺序对文档进行编号
    for docid, d in enumerate(docs):
        for w in d:
            if w not in word2id: # 如果遇到一个新的、未见过的词
                all_words.append(w)       # 加入词列表
                word2id[w] = len(word2id) # 分配编号

            if w not in word2docs: # 如果遇到一个新词，为其建立包含它的文档集合
                word2docs[w] = set()

            word2docs[w].add(docid)

    return all_words, word2id, word2docs


def build_inverted_index(word2id, docs):
    '''
    建立倒排索引的倒排表。需要与词典等信息配合使用。
    '''
    inverted_index = [[] for i in range(len(word2id))]

    for docid, d in enumerate(docs):
        for w in set(d): #每个词处理一次，用Set
            tf = d.count(w)
            wid = word2id[w]
            inverted_index[wid].append((docid, tf))

    return inverted_index


if __name__ == '__main__':
    words, word2id, word2docset = build_dictionary(docs)
    print(len(words))
    print(len(word2id))
    print('Word到ID的映射')
    for word, wid in word2id.items():
        print(word, wid)

    print('Word到文档映射')
    word2df = {} # 记录DF信息
    for word, docset in word2docset.items():
        print(word, docset, 'DF: ', len(docset))
        word2df[word] = len(docset)

    inv_inx = build_inverted_index(word2id, docs)

    import pickle # 用于数据序列化的工具
    # 将倒排文档相关的对象存储到磁盘，以后可以直接载入而不必重新建立索引
    pickle.dump([words, word2id, word2df, inv_inx], open('inverted_index.save', 'wb'))

