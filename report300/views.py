#coding:utf-8

from django.shortcuts import render
from .user import User

# Create your views here.
TIME_SPLIT=0.2
HERO_SHOWS=10

def form(request):
    a={'1':1,'2':2,'3':3,'4':4,'5':5}
    b={'a':'a','b':'b','c':'c','d':'d','e':'e'}
    return render(request,"form.html",{'a1':a,'b1':b})

def index(request):
    if (request.method=='POST'):
        username=request.POST['username']
        if type(username)=="<type 'unicode'>":
            username=username.encode('utf-8')
        if request.POST['time_split']!='':
            TIME_SPLIT=float(request.POST['time_split'.strip()])
        #print username
        newuser,sum,heros=stats(username)
        if newuser==False:
            return render(request,'index.html',{"name_error":"未找到该用户"})
        #print newuser
        sum_avg={}
        for key,value in sum.items():
            sum_avg[key]=float(value)/float(len(newuser.match_info))
            sum_avg[key]=float('%.2f'%sum_avg[key])

        stat_per=str(len(newuser.match_info))+'/'+str(len(newuser.match_urls))
        sorted_heros=sorted(heros.items(),key=lambda i:i[1],reverse=True)
        if len(sorted_heros)>HERO_SHOWS:
            sorted_heros=sorted_heros[:HERO_SHOWS]

        print sum_avg
        print sorted_heros

        return render(request,'show_resault.html',{'sum':sum_avg,'heros':sorted_heros,'stat_per':stat_per})
    #return HttpResponse('hehe')
    else:
        return render(request,"index.html")

def stats(name):
    newuser = User(name.strip())
    if newuser.USER_VALID==False:
        return False,1,1
    newuser.TIME_SPLIT=TIME_SPLIT
    #print newuser.user_info
    #print newuser.match_info
    #print '\n'
    sum = {'平均杀人次数':0,'平均死亡次数':0,'平均助攻次数':0,'平均摧毁建筑':0\
           ,'平均补兵':0,'平均获取金币':0}
    heros={}
    for mi in newuser.match_info:
        #print mi
        #print mi['kills']
        kill=mi['kills'].split('/')
        #print kill
        sum['平均杀人次数'] = sum['平均杀人次数']+int(kill[0])
        sum['平均死亡次数'] = sum['平均死亡次数'] + int(kill[1])
        sum['平均助攻次数'] = sum['平均助攻次数'] + int(kill[2])
        sum['平均摧毁建筑']=sum['平均摧毁建筑']+mi['buildings']
        sum['平均补兵']=sum['平均补兵']+mi['soldiers']
        sum['平均获取金币']=sum['平均获取金币']+mi['golds']
        hero=mi['hero'].strip().encode('utf8')
        if heros.has_key(hero):
            heros[hero]=heros[hero]+1
        else:
            heros[hero]=1
    #print heros

    return newuser,sum,heros

