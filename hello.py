# -*- coding:utf-8 -*-
# Flask などの必要なライブラリをインポートする
from flask import Flask
import os
import numpy as np

# 自身の名称を app という名前でインスタンス化する
app = Flask(__name__)

# ここからウェブアプリケーション用のルーティングを記述
# index にアクセスしたときの処理
@app.route('/')
def index():
    return "Hello,World!"

if __name__ == '__main__':
    app.run() # どこからでもアクセス可能に
