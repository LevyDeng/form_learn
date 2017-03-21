from time import sleep
import requests
import threading


urls=['http://300report.jumpw.com/match.html?id=71453614',\
      'http://300report.jumpw.com/match.html?id=71452663',
      'http://300report.jumpw.com/match.html?id=71450730',
      'http://300report.jumpw.com/match.html?id=71449134',
      'http://300report.jumpw.com/match.html?id=71407320']
def test(url):
    html=requests.get(url)
    print html.headers

threads=[threading.Thread(target=test,args=(u,)) for u in urls]
for t in threads:
    try:
        t.start()
        sleep(0.00001)

    except requests.exceptions.ConnectionError:
        print  'connection confused'
