# -*- coding:utf-8 -*-
# Flask などの必要なライブラリをインポートする
from flask import Flask,render_template,request,redirect,url_for
import os
import numpy as np

# 自身の名称を app という名前でインスタンス化する
app = Flask(__name__)

def error_detect(text):
    pass
    #Cotoha APIサーバーにルーティングする？
    #いつも通りリクエストを投げつける
    #戻り値を得てリターン

def vm():
    pass
    #ボタンが押されたらerror_detectを動かす

#アプリケーションルートにアクセスがあった場合
@app.route('/')
def hello():
    #vm()を動かす
    return render_template("index.html",title = "ErrorDetectTest")
if __name__ == '__main__':
    app.run() # どこからでもアクセス可能に

