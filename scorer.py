
def fetch_doclist_by_word(inverted_index, wordid):
    '''
    从倒排索引中取出包含词word的文档列表
    '''
    return inverted_index[wordid]


def scorer(inverted_index, word2id, df, query):
    '''
    query: 关键词列表
    df: 词项文档统计
    scorer从倒排索引inverted_index中获取文档并对文档进行相关性评分
    返回排在最前面的文档
    排序函数的计算方法是：文档和查询向量中词的权重为词的频率，采用内积计算相似度
    '''
    doc2score = {} # 记录文档分数

    for w in query: #
        if w not in word2id:
            continue
        wordid = word2id[w]
        doc_tf_list = fetch_doclist_by_word(inverted_index, wordid)
        for (doc, tf) in doc_tf_list:
            if doc not in doc2score:
                doc2score[doc] = tf
            else:
                doc2score[doc] += tf

    doc_score_list = doc2score.items()

    # 排序
    sorted_docs_by_score = sorted(doc_score_list, key=lambda item: item[1], reverse=True)

    return sorted_docs_by_score


if __name__ == '__main__':
    import pickle

    [words, word2id, word2df, inverted_index] = pickle.load(open('inverted_index.save', 'rb'))


    # 假设已经进行文本处理，将文档表示为词项列表
    d0=["据", "报道", "计算机", "病毒", "最近", "猖獗", "计算机"]
    d1=["邮件", "是", "电脑", "病毒", "传播", "途径", "之一", "电脑"]
    d2=["小王", "在", "医院", "学习", "为了", "研究", "病毒", "整天", "坐", "在", "计算机", "前", "查", "资料"]
    d3 = ["北京", "仁和", "医院", "病毒", "感冒"]
    d4 = ["电脑", "技术", "科学", "计算机", "研究", "病毒"]
    docs =[d0, d1, d2, d3,d4]

    query = ['电脑', '病毒']

    ranked_docs = scorer(inverted_index, word2id, word2df, query)

    for doc_id, score in ranked_docs[0:3]: # 展示前三个文档
        print(doc_id, docs[doc_id])
        print('---------------')

