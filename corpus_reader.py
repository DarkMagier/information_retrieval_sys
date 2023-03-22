from mm_seg import fmm_seg, dictionary


def read_documents_from_file(filename):
    '''
    从文件读入所有文档
    '''
    document_texts = []

    with open(filename,'r',encoding='utf-8') as fread:
        for line in fread:
            document_texts.append(line.strip())

    return document_texts


def word_segmentation_documents(document_texts):
    '''
    对文本数据进行分词，得到分词之后的文档列表
    采用逆向最大匹配算法(FMM)
    '''
    document_words = []

    for line in document_texts:
        document_words.append(fmm_seg(line, dictionary))

    return document_words


def load_stopwords(fname):
    '''
    读入停用词
    '''
    stopwords = set()
    with open(fname,'r',encoding='utf-8') as fread:
        for line in fread:
            stopwords.add(line.strip())

    return stopwords


def remove_stopwords(word_list, stopwords):
    '''
    去掉词列表中的停用词
    '''
    new_list = []

    for word in word_list:
        if word not in stopwords:
            new_list.append(word)

    return new_list
document_texts = read_documents_from_file('corpus.txt')
def getStopwords():
    stopwords = load_stopwords('stoplist_utf8.txt')
    puncs = load_stopwords('punctuation_utf8.txt')
    # print(stopwords)
    print(puncs)
    stopwords = stopwords | puncs
    # print(stopwords)
    return list(stopwords)

stopwords=getStopwords()
def corpus_reader():
    stopwords = load_stopwords('stoplist_utf8.txt')
    puncs = load_stopwords('punctuation_utf8.txt')
    # print(stopwords)
    stopwords = stopwords & puncs
    # print(stopwords)
    #raise ''
    # document_texts = read_documents_from_file('corpus.txt')
    # print(len(document_texts),document_texts)
    docs_words = word_segmentation_documents(document_texts)
    # print(len(docs_words),docs_words)
    docs_words_rm = []
    #
    for word_list in docs_words:
        new_list = remove_stopwords(word_list, stopwords)
        docs_words_rm.append(new_list)
    #
    # for word_list in docs_words_rm:
    #     print(word_list)
    #
    # print('docs_words_rm 保存了分词之后的文档，每个文档是一个词列表')
    return docs_words_rm
if __name__ == '__main__':
    '''
    测试
    '''
    stopwords = load_stopwords('stoplist_utf8.txt')
    print(stopwords)
    puncs = load_stopwords('punctuation_utf8.txt')
    print(stopwords)
    stopwords = stopwords & puncs
    # print(stopwords)
    # #raise ''
    # document_texts = read_documents_from_file('corpus.txt')
    # # print(len(document_texts),document_texts)
    # docs_words = word_segmentation_documents(document_texts)
    # # print(len(docs_words),docs_words)
    # docs_words_rm = []
    # #
    # for word_list in docs_words:
    #     new_list = remove_stopwords(word_list, stopwords)
    #     docs_words_rm.append(new_list)
    # #
    # for word_list in docs_words_rm:
    #     print(word_list)
    # #
    # print('docs_words_rm 保存了分词之后的文档，每个文档是一个词列表')
