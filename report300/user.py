#coding:utf-8

import requests
import re
from bs4 import BeautifulSoup
from urllib import quote
from time import sleep
import threading
from time import sleep
#from urllib3.exceptions import NewConnectionError
TIME_SPLIT2=1

class User():
    def __init__(self,name):
        self.TIME_SPLIT=0.2
        self.name=name
        self.base_url = "http://300report.jumpw.com/list.html?name=%s"%name
        self.match_urls=[]
        self.match_info=[]    #保存每场比赛的信息,每个元素都是一个字典
        self.USER_VALID=False      #标记用户名是否存在

        html=requests.get(self.base_url)
        #print html.text
        soup=BeautifulSoup(html.text,'lxml')
        #print soup.tr
        tr=soup.find_all("tr")
        if len(tr)!=0:
            self.USER_VALID=True
            self.set_user_info(tr)


    def set_user_info(self,tr):
        self.user_info={ 'username':tr[0].td.next_sibling.string,\
                         'userlevel':int(tr[1].td.next_sibling.string),\
                         'jiecao':int(tr[2].td.next_sibling.string),
                         'totalwins':int(tr[3].td.next_sibling.string),\
                         'totalplays':int(tr[4].td.next_sibling.string)}

        #获取每个比赛详情页面的地址
        self.match_urls=self.find_match_url(self.base_url)

        #循环访问比赛详情页面,获取每局比赛的信息
        threads=[threading.Thread(target=self.find_match_content,args=(match_urlsi,)) \
                 for match_urlsi in self.match_urls]
        for t in threads:
            try:
                sleep(self.TIME_SPLIT)
                t.start()
            except:
                sleep(1)
                pass
        #match_urls = re.findall(re_match_url, html.text)

    def find_match_url(self,url):
        re_match_url=r"match\.html\?id\=\d+"
        re_match_url=re.compile(re_match_url)
        match_urls=[]
        pages=int((self.user_info['totalplays']-1)/10)  #每页10条信息,计算一共有多少页
        for i in range(1,pages+2):
            try:
                sleep(TIME_SPLIT2)
                content=requests.get(self.base_url+"&index=%s"%str((i-1)*10)).text
                tmplist=re.findall(re_match_url,content)        #抓取比赛详情页面的url
                if len(tmplist)!=0:
                    for l in tmplist:
                        match_urls.append("http://300report.jumpw.com/"+l)
            except:
                sleep(TIME_SPLIT2)
                continue
        return match_urls

    #获取每场比赛的详细数据
    def find_match_content(self,match_url):
        content=requests.get(match_url).text
        match_id=int( match_url.split('=')[1] )
        soup=BeautifulSoup(content,'lxml')
        tr=soup.find_all('tr')
        for t in tr:
            if re.search(self.name,t.text):
                tds=[td for td in t.children]
                this_match_info={"id":match_id,\
                                 "hero":tds[3].text.split(")")[1].split("(")[0],\
                                 'kills':tds[5].string,\
                                 'wins':True if (tds[7].parent.parent.previous_element.previous_element==u"胜利") else False,\
                                 'buildings':int(tds[9].string),\
                                 'soldiers':int(tds[11].string),\
                                 'golds':int(tds[13].string),\
                                 'score':tds[15].string,\
                                 'exps':tds[21].string,\
                                 'jiecao':int(tds[23].string),\
                                 'wins_p':tds[25].string,}
        self.match_info.append(this_match_info)
        return this_match_info