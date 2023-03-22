import corpus_reader
from inverted_index import build_dictionary,build_inverted_index
from scorer import scorer


if __name__=="__main__":
    query=['武器系统','塔斯社']
    docs=corpus_reader.corpus_reader()
    words, word2id, word2docset = build_dictionary(docs)
    print(len(words))
    print(len(word2id))
    print('Word到ID的映射')
    for word, wid in word2id.items():
        print(word, wid)

    print('Word到文档映射')
    word2df = {}  # 记录DF信息
    for word, docset in word2docset.items():
        print(word, docset, 'DF: ', len(docset))
        word2df[word] = len(docset)

    inv_inx = build_inverted_index(word2id, docs)
    inverted_index=inv_inx
    ranked_docs = scorer(inverted_index, word2id, word2df, query)

    for doc_id, score in ranked_docs[0:3]:  # 展示前三个文档
        print(doc_id, docs[doc_id])
        print('---------------')