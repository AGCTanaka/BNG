# -*- coding:utf-8 -*-
# Flask などの必要なライブラリをインポートする
from flask import Flask,render_template
import os
import numpy as np

# 自身の名称を app という名前でインスタンス化する
app = Flask(__name__)

#アプリケーションルートにアクセスがあった場合
@app.route('/')
def hello():
    return "Hello,World!"

#アプリケーション/indexにアクセスがあった場合
@app.route("/index")
def index():
    return render_template("index.html")
if __name__ == '__main__':
    app.run() # どこからでもアクセス可能に
