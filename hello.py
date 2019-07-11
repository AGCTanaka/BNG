# -*- coding:utf-8 -*-
# Flask などの必要なライブラリをインポートする
from flask import Flask,render_template,request,redirect,url_for
import requests
import json
import re
import os
import numpy as np

#きょうのトークンせってい
token = "LuKoXHnH43dxVGDTbMoMMw4sNgq1"

# 自身の名称を app という名前でインスタンス化する
app = Flask(__name__)

#以下各APIを起動するための関数を定義する


#COTOHA API 音声認識誤り検知
def error_detect(text):
    url = "https://api.ce-cotoha.com/api/dev/nlp/beta/detect_misrecognition"
    headers = {
            "Content-Type":"application/json;charset=UTF-8",
            "Authorization":"Bearer " + token
            }
    data = {
            "sentence":text
            }
    r_post = requests.post(url,headers=headers,json=data)
    r_json=r_post.json()
    return r_json

def make_sentence(text,json):
#begin_posを取得
#end_posを取得
#textのbegin_posからend_posまでをcorrection[0]に置き換える
    jstext = json["result"]
    if jstext["candidates"] == []:
        text = text + "\n" + "<認識誤りは検知されませんでした。>"
        return text
    else:
        for adjust in jstext["candidates"]:
            beginpos = adjust["begin_pos"]
            endpos = adjust["end_pos"]
            head = text[:beginpos]
            berry = adjust["correction"][0]
            tail = text[endpos:]
            text = head + berry["form"] + tail
        return text



#COTOHA API 感情分析
def detect_sentiment(text,json):
#begin_posを取得
#end_posを取得
#textのbegin_posからend_posまでをcorrection[0]に置き換える
    jstext = json["result"]
    if jstext["emotional_phrase"] == []:
        text = text + "\n" + "<感情値は検知されませんでした。>"
        return text
    else:
        retvar = ""
        for emotions in jstext["emotional_phrase"]:
            root =emotions["form"]
            emotion =emotions["emotion"]
            retvar = retvar + "\n" + emotion + "\n" + root
        return retvar



#アプリケーションルートにアクセスがあった場合
@app.route('/')
def hello():
    return render_template("index.html",title = "COTOHA API test",name1 = "温泉認識は誤りを含む。",name2 = "")

#プルダウンの値を読み取り、内容によって用いる関数と使い方部分に渡すパラグラフを変更する。
@app.route('/post',methods=['GET','POST'])
def post():
    if request.method == 'POST':
        text = request.form['text']
        detectedText = error_detect(text)
        writeText = make_sentence(text,detectedText)
    return render_template('index.html',name1=text,name2=writeText,title ="API Test Result")

if __name__ == '__main__':
    app.run() # どこからでもアクセス可能に
