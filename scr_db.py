from urllib.request import urlopen
import urllib.parse
from bs4 import BeautifulSoup
import re
import time
import unicodedata
import sqlite3


def createDB():
    conn = sqlite3.connect("database.db")
    c = conn.cursor()
    c.execute("create table text(id integer, text text)")
    conn.commit()
    conn.close()


def is_japanese(string):
    for ch in string:
        name = unicodedata.name(ch)
        if "CJK UNIFIED" in name \
        or "HIRAGANA" in name \
        or "KATAKANA" in name:
            return True
    return False

def get_links(page_url,urllist):
    page_url= urllib.parse.quote(page_url)
    page_url = re.sub("%3A",":",page_url)
    page_url = re.sub("%23","#",page_url)
    html = urlopen(page_url)
    BsObj=BeautifulSoup(html,features = "html.parser")
    for link in BsObj.findAll("a"):
        if "href" in link.attrs:
            new_page = link.attrs['href']
            #print(new_page)
            if "http" not in new_page:
                if ".." in new_page:
                    new_page = re.sub("\.\.","",new_page)
                #new_page = "https://www.hagoromofoods.co.jp" + new_page
                new_page = "https://www.timeless-edition.com/archives/2614" + new_page
                urllist.append(new_page)
            if new_page  not in urllist and "#" not in new_page and "tel:" not in new_page and "jbr" in new_page:
                urllist.append(new_page)
            elif "asp" in new_page and "http" not in new_page:
                #new_page = "https://www.hagoromofoods.co.jp" + new_page
                new_page = "https://www.timeless-edition.com/archives/2614" + new_page
                urllist.append(new_page)
            pass
    return urllist

def get_textContent(page_url):
    time.sleep(1)
    page_url= urllib.parse.quote(page_url)
    page_url = re.sub("%23","#",page_url)
    page_url = re.sub("%3A",":",page_url)
    page_url = re.sub("%3D","=",page_url)
    page_url = re.sub("%3F","?",page_url)
    html = urlopen(page_url)
    #print(page_url)
    BsObj=BeautifulSoup(html,features = "html.parser")
    txt = ""
    for text in BsObj.find_all("p"):
        txt = text.get_text()
        return txt
        #if "ページ内を移動する" not in text.get_text():
        #    txt = text.get_text()
        '''
    for lists in BsObj.findAll("li"):
        if ("#" not in str(lists) and "span" not in str(lists) and "month" not in str(lists)):
            txt = lists.get_text()
        return txt
'''
def executeDB(txt):
    txtlist = txt.split("\n")
    setlist = []
    for i in txtlist:
        myset = (i,txtlist[i])
        setlist.append(myset)
    c.executemany("insert into text values(?,?)",setlist)

urllist = get_links("https://www.timeless-edition.com/archives/2614",[])
createDB()
conn = sqlite3.connect("database.db")
c = conn.cursor()
num = 0
pages = set()
for i in urllist:
 #   if "html" in i:
    if "javascript" not in i : 
        try:
            txt = get_textContent(i)
            executeDB(txt)
        except:
            pass
c.execute("select distinct text from text")
g = c.fetchall()
print(g)
conn.commit()
conn.close()




