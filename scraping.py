from urllib.request import urlopen
import urllib.parse
from bs4 import BeautifulSoup
import re
pages = set()
import time
import unicodedata

def is_japanese(string):
    for ch in string:
        name = unicodedata.name(ch)
        if "CJK UNIFIED" in name \
        or "HIRAGANA" in name \
        or "KATAKANA" in name:
            return True
    return False
#作戦：
#サブメニューの中を2階層までget_textする。

num = 0
def get_textContent(page_url):
    time.sleep(1)
    page_url= urllib.parse.quote(page_url)
    page_url = re.sub("%23","#",page_url)
    page_url = re.sub("%3A",":",page_url)
    page_url = re.sub("%3D","=",page_url)
    page_url = re.sub("%3F","?",page_url)
    html = urlopen(page_url)
    print(page_url)
    print("yes")
    BsObj=BeautifulSoup(html,features = "html.parser")
    for text in BsObj.find_all("p"):
        if "ページ内を移動する" not in text.get_text():
            print(text.get_text())
    for lists in BsObj.findAll("li"):
        if ("#" not in str(lists) and "span" not in str(lists) and "month" not in str(lists)):
            print(lists.get_text())

def get_links(page_url,urllist):
    page_url= urllib.parse.quote(page_url)
    page_url = re.sub("%3A",":",page_url)
    page_url = re.sub("%23","#",page_url)
    html = urlopen(page_url)
    BsObj=BeautifulSoup(html,features = "html.parser")
    for link in BsObj.findAll("a"):
        if "href" in link.attrs:
            new_page = link.attrs['href']
            if "http" not in new_page:
                if ".." in new_page:
                    new_page = re.sub("\.\.","",new_page)
                new_page = "https://www.treeoflife.co.jp/library/aromablendlab/essentialoil" + new_page
                urllist.add(new_page)
            if new_page  not in urllist and "#" not in new_page and "tel:" not in new_page and "jbr" in new_page:
                urllist.add(new_page)
            elif "asp" in new_page and "http" not in new_page:
                new_page = "https://www.treeoflife.co.jp/library/aromablendlab/essentialoil" + new_page
                urllist.add(new_page)
        else:
            print("yes")
            urllist.add(link)
    return urllist

urllist = get_links("https://www.treeoflife.co.jp/library/aromablendlab/essentialoil/",pages)
print(urllist)
for i in urllist:
    print(i)
 #   if "html" in i:
    if "javascript" not in i : 
        try:
            get_textContent(i)
        except:
            pass


