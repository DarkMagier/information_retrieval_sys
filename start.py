from flask import Flask,render_template,request,redirect,url_for
import json
import core
from mm_seg import fmm_seg,bmm_seg,dictionary
from corpus_reader import document_texts,remove_stopwords,getStopwords
app = Flask(__name__)
#设置


@app.route('/search',methods=['GET','POST'])
def index_search():
    if request.method=='GET':
        wd=request.args.get('wd')
        # print(type(wd))
        print('get',wd)
        return render_template('search.html',search_wd=wd)
        # return render_template('search.html',search_wd=wd)
    elif request.method=='POST':
        wd = request.form.get('wd')
        read_to_search=request.form.get('read_to_search')
        print('post', wd,read_to_search)

        if read_to_search!=None:
            return render_template('search.html', search_wd=wd)

        query=[]
        query_1=wd.split(" ")
        temp=wd.replace(" ","")
        print(query,temp)
        results_bmm = bmm_seg(wd, dictionary)
        results_fmm = fmm_seg(wd, dictionary)

        query.extend(query_1)
        query.extend(results_bmm)
        query.extend(results_fmm)
        query=list(set(query))
        if ' ' in query:
            query.remove(' ')
        if '' in query:
            query.remove('')

        query_init=query.copy()
        stopwords=getStopwords()
        # print(stopwords)
        # print('before',len(query),query)
        query=remove_stopwords(query,stopwords)
        print('after',len(query), query)
        res=core.getSearchResult(query,query_init)
        print(res)
        if len(res)==0:
            res=core.getSearchResult(query_init,query_init)
            query=query_init
        resp={
            'wd_split':query,
            'data':res,
        }

        return json.dumps(resp)
@app.route('/')
def index():
    return render_template('index.html')

@app.route('/docs')
def docs():
    if request.method=='GET':
        doc_id=request.args.get('doc_id')
        return render_template("docs.html",text=document_texts[int(doc_id)])

    return render_template()
if __name__ == '__main__':
    # app.run(debug='true')
    app.run(host="0.0.0.0",port=8001,debug='true')
