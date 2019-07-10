# -*- coding:utf-8 -*-
# Flask などの必要なライブラリをインポートする
from flask import Flask,render_template,request,redirect,url_for
import requests
import json
import re
import os
import numpy as np


# 自身の名称を app という名前でインスタンス化する
app = Flask(__name__)



#アプリケーションルートにアクセスがあった場合
@app.route('/')
def hello():
    return "Hello,World!"

if __name__ == '__main__':
    app.run() # どこからでもアクセス可能に
