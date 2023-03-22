from corpus_reader import document_texts,corpus_reader
from inverted_index import build_dictionary,build_inverted_index
from scorer import scorer
import numpy as np
from sklearn.cluster import DBSCAN,KMeans
from sklearn import preprocessing
import matplotlib.pyplot as plt
docs=corpus_reader()
words, word2id, word2docset = build_dictionary(docs)
# print(len(words))
# print(len(word2id))
# print('Word到ID的映射')
# for word, wid in word2id.items():
#     print(word, wid)

# print('Word到文档映射')
word2df = {}  # 记录DF信息
for word, docset in word2docset.items():
    # print(word, docset, 'DF: ', len(docset))
    word2df[word] = len(docset)

inv_inx = build_inverted_index(word2id, docs)

inverted_index = inv_inx


def search(query):
    ranked_docs = scorer(inverted_index, word2id, word2df, query)


    return ranked_docs


def KmeansCut(query,doc):
    wd_list = []
    for i in range(0, len(doc)):
        if doc[i] in query:
            wd_list.append([i, 0])
    wd_list_init = np.array(wd_list)
    wd_list = preprocessing.scale(wd_list_init)
    # wd_list = wd_list_init
    # print(wd_list_init, wd_list)
    # print(query)
    if len(wd_list) > len(query):
        k = int(len(wd_list) / len(query))-1
    else:
        k=len(query)
    print("n_sample:",k)
    # y_pred=DBSCAN(eps=15,min_samples=1).fit_predict(wd_list)
    kmeans = KMeans(n_clusters=k)
    # # print(k,type(k))
    y_pred = kmeans.fit_predict(wd_list)
    y_pred = y_pred.tolist()
    # np.set_printoptions(threshold=10000)

    # plt.scatter(wd_list[:,0],wd_list[:,1], c=y_pred)
    # plt.show()
    # print(y_pred)
    wd_index = 0
    wd_count = 0
    for i in range(k):
        count = y_pred.count(i)
        if count > wd_count:
            wd_index = i
            wd_count = count
    wd_list_index = y_pred.index(wd_index)
    # print(wd_list_index, wd_count)
    doc_index = wd_list_init[wd_index][0]
    # print(doc_index, doc[doc_index])

    cut_l,cut_r=limit_cut_test(doc_index,len(doc))

    textcut = doc[cut_l:cut_r]
    # print("查看",doc_index, doc[doc_index], cut_l, cut_l, textcut)
    return list(wd_list),list(y_pred),textcut

def DbscanCut(query,doc):
    wd_list = []
    for i in range(0, len(doc)):
        if doc[i] in query:
            wd_list.append([i, 0])
    wd_list_init = np.array(wd_list)
    # wd_list = preprocessing.scale(wd_list_init)
    wd_list = wd_list_init
    print(wd_list)
    # print(wd_list_init, wd_list)
    # print(query)
    # if len(wd_list) > len(query):
    #     k = int(len(wd_list) / len(query))-1
    # else:
    #     k=len(query)
    # print("n_sample:",k)
    y_pred=DBSCAN(eps=15,min_samples=1).fit_predict(wd_list)
    # kmeans = KMeans(n_clusters=k)
    # # print(k,type(k))
    # y_pred = kmeans.fit_predict(wd_list)
    y_pred = y_pred.tolist()
    # np.set_printoptions(threshold=10000)

    # plt.scatter(wd_list[:,0],wd_list[:,1], c=y_pred)
    # plt.show()
    print(y_pred)
    wd_index = 0
    wd_count = 0
    k=len(set(y_pred))
    for i in range(k):
        count = y_pred.count(i)
        if count > wd_count:
            wd_index = i
            wd_count = count
    wd_list_index = y_pred.index(wd_index)
    # print(wd_list_index, wd_count)
    doc_index = wd_list_init[wd_index][0]
    # print(doc_index, doc[doc_index])

    cut_l,cut_r=limit_cut_test(doc_index,len(doc))

    textcut = doc[cut_l:cut_r]
    # print("查看",doc_index, doc[doc_index], cut_l, cut_l, textcut)
    return list(wd_list),list(y_pred),textcut

def limit_cut_test(doc_index,doc_len):
    limit = 15
    # print(type(doc_len))
    cut_l = 0
    cut_r = 0
    if doc_len < limit:
        # print("!1")
        cut_l = 0
        cut_r = doc_len
        return 0,doc_len
    else:
        # print("!2")
        if doc_index + limit < doc_len:
            # print("!21")
            cut_l = doc_index
            cut_r = doc_index + limit

        else:
            # print("!23")
            cut_l = doc_len - limit
            cut_r = doc_len
    return cut_l,cut_r
def max_Cut(query,doc):


    word_locate = []
    # print(type(doc))

    lenth=doc.__len__()
    for word in query:
        for i in range(0,lenth):
            if word ==doc[i]:
                word_locate.append(i)
    word_locate.sort()
    # print(word_locate)
    l=int(lenth/10)
    # print(lenth,len)
    cells=[x for x in range(0,lenth,l)]
    cells_count=dict()
    for item in cells:
        cells_count[item]=0
    # print(cells_count)
    for loc in word_locate:
        for cell in cells:
            if loc>cell:
                cells_count[cell]+=1;
                continue

    doc_index=0
    loc=0
    # print(cells_count)
    for cell in cells_count:
        # print(cells_count[cell])
        if cells_count[cell]>doc_index:
            loc=cell
            doc_index=cells_count[cell]
            # print('find_max:',doc_index)
    # print("before locate:",doc_index)
    for item in word_locate:
        # print('change:',item,doc[item],doc_index,doc[doc_index])
        if item>doc_index:
            doc_index=item
            break

    # l_limit=5
    # r_limt=20
    # if doc_index>l_limit:
    #     l = doc_index - l_limit
    # if doc_index<lenth-r_limt:
    #     r= doc_index+r_limt
    # else:
    #     r=lenth
    # print(doc_index,l,r)
    # # textcut=doc[l:r]
    cut_l,cut_r=limit_cut_test(doc_index,len(doc))

    textcut = doc[cut_l:cut_r]
    # print("查看",doc_index, doc[doc_index], cut_l, cut_l, textcut)
    return textcut

def eachDoctsCut(query,doc):
    # textcut = KmeansCut(query, doc)
    try:
        try:
            wd_list, y_pred, textcut=DbscanCut(query,doc)
            print("使用Dbscan")
            # print(query)
            # print(textcut)
            return '使用DBSCAN算法聚类',wd_list,y_pred,textcut
        except Exception as e:
            print("有错误", e)
            wd_list, y_pred, textcut=KmeansCut(query,doc)
            print("使用Kmeans")
            # print(query)
            # print(textcut)
            return '使用Kmeans算法聚类', wd_list, y_pred,textcut
    except Exception as e:
        print("有错误",e)

        textcut=max_Cut(query,doc)
        print('使用原始算法')
        print(query)
        print(textcut)
    return textcut

    # print(max,l,r)
    # textcut=doc[l:r]
    # textcut=doc[0:10]
    # return textcut



def getSearchResult(query,query_init):
    ranked_docs=search(query)
    results=[]
    for doc_id, score in ranked_docs: # 展示前三个文档
        # textcut=eachDoctsCut(query,docs[doc_id])
        textget=eachDoctsCut(query_init,docs[doc_id])
        if len(textget)==1:
            textcut=textget
            havePic="None"
            pic_data=[]
        else:
            textcut=textget[3]
            title=textget[0]
            wd_list_init=textget[1]
            wd_list=[]

            for item in wd_list_init:
                wd_list.append(int(item[0]))
                havePic = "Have"
            y_pred=textget[2]
            # print(type(title),type(wd_list),type(y_pred))
            pic_data = [title, wd_list, y_pred]
        # print(doc_id,score,textcut, docs[doc_id])
        res = {
            "search_data": [doc_id, score, textcut, document_texts[doc_id][0:300]],
            "havePic":havePic,
            "pic_data": pic_data
        }
        results.append(res)
    # print(ranked_docs)
    return results
if __name__=="__main__":
    # query=['俄罗斯', '海军', '力量', '中坚', '而', '据', '外电报道', '瓦良格', '号', '在', '完工', '9', '5', '后', '由于']
    query=['台湾']
    # getSearchResult(query)
    eachDoctsCut(query,docs[71])
