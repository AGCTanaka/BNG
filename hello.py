# -*- coding:utf-8 -*-
# Flask などの必要なライブラリをインポートする
from flask import Flask,render_template,request,redirect,url_for
import requests
import json
import re
import os
import numpy as np

#きょうのトークンせってい
token = "tcVbPE2dVMW61MjqK86ZQHRN5YdH"
# 自身の名称を app という名前でインスタンス化する
app = Flask(__name__)

#ipアドレスに制限をかける
'''
def ip_check(func):
    def wrapper(*args,**kwargs):
        if "piyopiyo" in request.remote_addr:
            print ("IP Check : Okay")
            return func(*args,**kwargs)
        else:
            print(request.remote_addr)
            print("403")
            return "Request Denied"
    return wrapper
'''


#以下各APIを起動するための関数を定義する

#類似度算出のみ引数を必ず二つ求める。よって類似度算出は別の関数で定義する
def similarity_calculate(text):
    textlist = text.split("\n")
    text1 = textlist[0]
    text2 = textlist[1]
    url = "https://api.ce-cotoha.com/api/dev/nlp/v1/similarity"
    headers = {
            "Content-Type":"application/json;charset=UTF-8",
            "Authorization":"Bearer " + token
            }
    data = {
            "s1":text1,
            "s2":text2
            }
    r_post = requests.post(url,headers=headers,json=data)
    r_json=r_post.json()
    return r_json["result"]["score"]



#API問い合わせ
def api_parse(text,option):
    url = ""
    if option == "音声認識誤り検知":
        url = "https://api.ce-cotoha.com/api/dev/nlp/beta/detect_misrecognition"
    elif option == "感情分析":
        url = "https://api.ce-cotoha.com/api/dev/nlp/v1/sentiment"
    elif option == "固有表現抽出":
        url = "https://api.ce-cotoha.com/api/dev/nlp/v1/ne"
    elif option == "構文解析":
        url = "https://api.ce-cotoha.com/api/dev/nlp/v1/parse"
    elif option == "キーワード抽出":
        url = "https://api.ce-cotoha.com/api/dev/nlp/v1/keyword"
    elif option == "文タイプ判定":
        url = "https://api.ce-cotoha.com/api/dev/nlp/v1/sentence_type"
    elif option == "ユーザ属性推定":
        url = "https://api.ce-cotoha.com/api/dev/nlp/beta/user_attribute"
    elif option == "言い淀み除去":
        url = "https://api.ce-cotoha.com/api/dev/nlp/beta/remove_filler"
    elif option == "照応解析":
        url = "https://api.ce-cotoha.com/api/dev/nlp/v1/coreference"
    headers = {
            "Content-Type":"application/json;charset=UTF-8",
            "Authorization":"Bearer " + token
            }
    data = {
            "sentence":text,
            "document":text,
            "text":text
            }
    r_post = requests.post(url,headers=headers,json=data)
    r_json=r_post.json()
    return r_json

#COTOHA API 音声認識誤り検知
def correct_recognitionError(text,json):
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
        emotion_words = ""
        for emotions in jstext["emotional_phrase"]:
            root =emotions["form"]
            emotion =emotions["emotion"]
            if emotion == "P":
                emotion = "ポジティヴ"
            elif emotion == "N":
                emotion = "ネガティヴ"
            elif emotion == "NP":
                emotion = "ポジネガ"
            blacket = "(" + emotion + ")"
            emotion_words = emotion_words + root + " " + blacket + "\n"
        return emotion_words

#COTOHA API 固有表現抽出
def word_extract(text,json):
    jstext_list = json["result"]
    if jstext_list == []:
        text = text + "\n" + "<固有表現は検出されませんでした。>"
        return text
    else:
        terms = ""
        for term in jstext_list:
            form = term["form"]
            term_class = term["class"]
            j_term_class = {
                "ORG" : "組織名",
                "PSN" : "人名",
                "LOC" : "場所",
                "ART" : "固有物名",
                "DAT" : "日付表現",
                "TIM" : "時刻表現",
                "NUM" : "数値表現",
                "MNY" : "金額表現",
                "PCT" : "割合表現",
                "OTH" : "その他"
            }

            blacket = "("+ j_term_class[term_class] + ")"
            terms = terms + form + " " + blacket + "\n"
        return terms
#COTOHA API 構文解析
def text_parse(text,json):
    jstext_list = json["result"]
    return jstext_list

#COTOHA API キーワード抽出
def abstruct_keywords(text,json):
    jstext_list = json["result"]
    keywordList = ""
    for keyword in jstext_list:
        keywordList = keywordList + "キーワード:" + keyword["form"] + "  " + "スコア:" + str(keyword["score"]) + "\n"
    return keywordList

#COTOHA API 文タイプ判定
def classify_text(text,json):
    jstext = json["result"]
    modality = jstext["modality"]
    dialog_act = jstext["dialog_act"]
    j_modalities = {
        "declarative" : "叙述",
        "interrogative" : "質問",
        "imperative" : "命令"
    }
    j_dialog_acts = {
        "greeting" : "挨拶",
        "information-providing" : "情報提供",
        "feedback" : "フィードバック、相槌",
        "information-seeking" : "情報獲得",
        "agreement" : "賛成",
        "feedbackElicitation" : "理解確認",
        "commissive" : "約束",
        "acceptOffer" : "受領",
        "selfCorrection" : "言い直し",
        "thanking" : "感謝",
        "apology" : "謝罪",
        "stalling" : "時間稼ぎ",
        "directive" : "指示",
        "goodbye" : "別れ"
    }
    classified = "文タイプ:" + j_modalities[modality] + "\n" + "詳細:"
    for j in dialog_act:
        classified = classified + j_dialog_acts[j]+ "\n"
    return classified


#cotoha api ユーザ属性推定(β)
def estimate_usertype(text,json):
    jstext = json["result"]
    userattr = "年代:" + str(jstext.get("age","不明")) + "\n既婚/未婚:" + str(jstext.get("civilstatus","不明")) + "\n給与:" + str(jstext.get("earnings","不明")) + "\n性別:" + str(jstext.get("gender","不明")) + "\n習慣:" + str(jstext.get("habit","不明")) + "\n趣味:" + str(jstext.get("hobby","不明")) + "\n業種:" + str(jstext.get("kind_of_business","不明")) + "\n職種:" + str(jstext.get("kind_of_occupation","不明")) + "\n出身地:" + str(jstext.get("location","不明")) + "\n移動手段:" +  str(jstext.get("moving","不明")) + "\n職業:" + str(jstext.get("occupation","不明")) + "\n役職:" + str(jstext.get("position","不明"))
    return userattr

#COTOHA API 言い淀み除去
def remove_filler(text,json):
    jstext = json["result"]
    filler_concat = ""
    for fillers in jstext:
        filler_concat = filler_concat + fillers["fixed_sentence"]
    return filler_concat

#COTOHA API 照応解析
def call_analysis(text,json):
    jstext = json["result"]["coreference"]
    reference_concat_list = []
    for i in jstext:
        referents_list =i["referents"]
        for j in referents_list:
            reference_concat_list.append(j["form"])
    return " = ".join(reference_concat_list)

#アプリケーションルートにアクセスがあった場合
@app.route('/')
#@ip_check
def hello():
    return render_template("index.html",title = "COTOHA API test",name1 = "プルダウンから機能を選択してください",name2 = "")

#プルダウンの値を読み取り、内容によって用いる関数と使い方部分に渡すパラグラフを変更する。


@app.route('/post',methods=['GET','POST'])
def change_function():
    apimenu = request.args.get("apimenu")
    structedText = ""
    text = request.args.get("text")
    if apimenu == "類似度算出":
        structedText = similarity_calculate(text)
    else:
        text = request.args.get("text")
        parsedText = api_parse(text,apimenu)
#構文解析機能
        if apimenu == "音声認識誤り検知":
            structedText = correct_recognitionError(text,parsedText)
#感情分析機能
        elif apimenu == "感情分析":
            structedText = detect_sentiment(text,parsedText)
#固有表現抽出機能
        elif apimenu == "固有表現抽出":
            structedText = word_extract(text,parsedText)
        elif apimenu == "構文解析":
            structedText = text_parse(text,parsedText)
        elif apimenu == "キーワード抽出":
            structedText = abstruct_keywords(text,parsedText)
        elif apimenu == "文タイプ判定":
            structedText = classify_text(text,parsedText)
        elif apimenu == "ユーザ属性推定":
            structedText = estimate_usertype(text,parsedText)
        elif apimenu == "言い淀み除去":
            structedText = remove_filler(text,parsedText)
        elif apimenu == "照応解析":
            structedText =call_analysis(text,parsedText)
    return render_template('index.html',name1=text,name2=structedText,title ="API Test Result")
    

if __name__ == '__main__':
    app.run() # どこからでもアクセス可能に
