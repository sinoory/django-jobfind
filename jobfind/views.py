# -*- coding: utf-8 -*-
import sys,traceback
import os
reload(sys)
sys.setdefaultencoding('utf8')
sys.path.append(os.path.join(os.path.dirname(__file__),"../pypub/utility"))
sys.path.append(os.path.join(os.path.dirname(__file__),"../pypub/web"))

from uty import *
from datetime import datetime
from webLogin import LoginBroser
from getPage import HtmlReader
from bs4 import BeautifulSoup
from pyquery import PyQuery as pq
import urllib,os
import json,re
import threading
_ck = "guid=7cf733caa27fadb740860c3099054403; nsearch=jobarea%3D%26%7C%26ord_field%3D%26%7C%26recentSearch0%3D%26%7C%26recentSearch1%3D%26%7C%26recentSearch2%3D%26%7C%26recentSearch3%3D%26%7C%26recentSearch4%3D%26%7C%26collapse_expansion%3D; _ujz=MjQ4ODkwNTcw; slife=lowbrowser%3Dnot%26%7C%26lastlogindate%3D20200520%26%7C%26securetime%3DDTFVY1Y4WDUDaFZsDDIKY1VjVmY%253D; partner=0_0_0_0; search=jobarea%7E%60020000%7C%21ord_field%7E%600%7C%21recentSearch0%7E%60020000%A1%FB%A1%FA000000%A1%FB%A1%FA0000%A1%FB%A1%FA00%A1%FB%A1%FA99%A1%FB%A1%FA%A1%FB%A1%FA99%A1%FB%A1%FA99%A1%FB%A1%FA99%A1%FB%A1%FA99%A1%FB%A1%FA9%A1%FB%A1%FA99%A1%FB%A1%FA%A1%FB%A1%FA0%A1%FB%A1%FA%C1%FA%C6%EC%A1%FB%A1%FA1%A1%FB%A1%FA1%7C%21recentSearch1%7E%60020000%A1%FB%A1%FA000000%A1%FB%A1%FA0000%A1%FB%A1%FA00%A1%FB%A1%FA99%A1%FB%A1%FA%A1%FB%A1%FA99%A1%FB%A1%FA99%A1%FB%A1%FA99%A1%FB%A1%FA99%A1%FB%A1%FA9%A1%FB%A1%FA99%A1%FB%A1%FA%A1%FB%A1%FA0%A1%FB%A1%FA%C1%FA%C6%EC%A1%FB%A1%FA2%A1%FB%A1%FA1%7C%21recentSearch2%7E%60020000%A1%FB%A1%FA000000%A1%FB%A1%FA0000%A1%FB%A1%FA00%A1%FB%A1%FA99%A1%FB%A1%FA%A1%FB%A1%FA99%A1%FB%A1%FA99%A1%FB%A1%FA99%A1%FB%A1%FA99%A1%FB%A1%FA9%A1%FB%A1%FA99%A1%FB%A1%FA%A1%FB%A1%FA0%A1%FB%A1%FA%D6%D0%C8%ED%B9%FA%BC%CA%BF%C6%BC%BC%B7%FE%CE%F1%D3%D0%CF%DE%B9%AB%CB%BE%A1%FB%A1%FA2%A1%FB%A1%FA1%7C%21recentSearch3%7E%60020000%A1%FB%A1%FA000000%A1%FB%A1%FA0000%A1%FB%A1%FA00%A1%FB%A1%FA99%A1%FB%A1%FA%A1%FB%A1%FA99%A1%FB%A1%FA99%A1%FB%A1%FA99%A1%FB%A1%FA99%A1%FB%A1%FA9%A1%FB%A1%FA99%A1%FB%A1%FA%A1%FB%A1%FA0%A1%FB%A1%FAAndroid%A1%FB%A1%FA2%A1%FB%A1%FA1%7C%21recentSearch4%7E%60020000%A1%FB%A1%FA000000%A1%FB%A1%FA0000%A1%FB%A1%FA00%A1%FB%A1%FA99%A1%FB%A1%FA%A1%FB%A1%FA99%A1%FB%A1%FA99%A1%FB%A1%FA99%A1%FB%A1%FA99%A1%FB%A1%FA9%A1%FB%A1%FA99%A1%FB%A1%FA%A1%FB%A1%FA0%A1%FB%A1%FAtcl%A1%FB%A1%FA2%A1%FB%A1%FA1%7C%21; ps=needv%3D0; 51job=cuid%3D24889057%26%7C%26cusername%3Dsinoory%26%7C%26cpassword%3D%26%7C%26cname%3D%25CD%25F5%25B4%25DE%26%7C%26cemail%3Dsinoory%2540126.com%26%7C%26cemailstatus%3D3%26%7C%26cnickname%3Dsinoory%26%7C%26ccry%3D.0ETBlTAgdF3.%26%7C%26cconfirmkey%3DsiWoRCbHJRF36%26%7C%26cautologin%3D1%26%7C%26cenglish%3D0%26%7C%26sex%3D0%26%7C%26cnamekey%3DsihiQfuRPViHs%26%7C%26to%3D8b2f01c27406249ec559ccc50ff52b745ec52e57%26%7C%26"
class CookieLogin51(object):
    def __init__(self):
        print("CookieLogin51 init",self)
        self.cl_cookieStr=_ck
        self.cl_viewd_cmps = {"hs":[]}
        self._gtimerUpdateRecentCmpanys = False
        if os.path.exists("viewed_companys.hist") :
            with open("viewed_companys.hist","r") as f :
                hist = f.read()
                self.cl_viewd_cmps = json.loads(hist)
        self.resume_status = {}
        self.cl_last_resume_time=None
    def hasLogin(self):
        url="https://i.51job.com/userset/resume_browsed.php?lang=c"
        rd=HtmlReader(url,cookie=self.cl_cookieStr)
        rd.run()
        #soup=BeautifulSoup(rd.outdata.decode("gbk"),fromEncoding="gbk")
        soup=BeautifulSoup(rd.outdata.decode("gbk"),features="html5lib")
        cmpnyTag=soup.findAll("div",{"class":"txt"})
        #print "hasLogin cmpytag=",cmpnyTag
        return len(cmpnyTag)>0

    def getLoginVerifyImg(self):
        return "CookieLogin51 no img but want cookie"
    def Login(self,kvs):
        return
    def getResumeStates(self):
        n = datetime.now()
        if self.cl_last_resume_time != None :
            if n.hour == self.cl_last_resume_time.hour :
                return
        self.cl_last_resume_time = n
        url="http://i.51job.com/userset/my_apply.php?lang=c&type=sh&tagType=all&page=1"
        rd=HtmlReader(url,cookie=self.cl_cookieStr)
        rd.run()
        d=pq(rd.outdata.decode("gbk"))
        total_txt = d("div.p_in span.td").text() #共7页，到第 页
        pgcnt = int(re.findall(r'\d{1,}',total_txt)[0])
        print total_txt, pgcnt
        res={}
        for pg in range(1,pgcnt+1) :
            url = "http://i.51job.com/userset/my_apply.php?lang=c&type=sh&tagType=all&page=%d" %pg
            print "processing page",pg,":",pgcnt
            rd=HtmlReader(url,cookie=self.cl_cookieStr)
            rd.run()
            d=pq(rd.outdata.decode("gbk"))
            jobs = d("div.apox div.e").items()
            #jobs = d("div.e.cye-lm-tag").items()

            for j in jobs :
                cn,cu = j("a.gs").text(),j("a.gs").attr.href
                holders = j("div.c_light_blue span").text()
                jn,ju = j("a.zhn").text(),j("a.zhn").attr.href
                jid = j("div.hpBox.h_orange input").attr.value

                sturl = "http://i.51job.com/userset/ajax/apply.php?0.431294613asd23&jsoncallback=jQuery1830180sdf8044798423_1594959626386&cvinfo%5B"+jid+"%5D%5Bcvlogid%5D="+jid+"&cvinfo%5B"+jid+"%5D%5Btime%5D=1594868734&cvinfo%5B"+jid+"%5D%5Bpass%5D=1"
                rd=HtmlReader(sturl,cookie=self.cl_cookieStr)
                rd.run()
                js = json.loads(rd.outdata.decode("gbk")[41:-1])
                for k,v in js['html'].items() :
                    dt = pq(v)
                    status = dt("label:last").text()
                jid = re.findall('\d{5,}',ju)[0]
                res[jid]={"jn":jn,"ju":ju,"holders":holders,"jid":jid,"status":status,"cn":cn,"cu":cu}
                print jn,cn,"\n",status,holders
        self.resume_status = res
        return res
        print "finish url"
        for r in res.values() :
            print r['jn'],r['cn'],"\n",r['status'],r['holders']





    def getRecentCmpanys(self,number=5):
        url="https://i.51job.com/userset/resume_browsed.php?lang=c"
        rd=HtmlReader(url,cookie=self.cl_cookieStr)
        rd.run()
        soup=BeautifulSoup(rd.outdata.decode("gbk"),features="html5lib")
        cmpnyTag=soup.findAll("div",{"class":"txt"})[0]
        atag = cmpnyTag.findAll("a")[0]
        cmpname , cmpurl =  atag.get("title"),atag.get("href")
        #print "cmpname=",cmpname
        lastTm = cmpnyTag.findAll("span",{"class":"c_orange"})[0].get_text()
        if len(self.cl_viewd_cmps["hs"])==0 or self.cl_viewd_cmps["hs"][-1]["time"] != lastTm :
            self.cl_viewd_cmps["hs"].append({"name":cmpname,"url":cmpurl,"time":lastTm})
            with open("viewed_companys.hist","w") as f :
                f.write(json.dumps(self.cl_viewd_cmps,indent=2,ensure_ascii=False))
        return {"hs":self.cl_viewd_cmps["hs"][-number:]}

_51loger = CookieLogin51()

def timerUpdateRecentCmpanys():
    try :
        _51loger.getRecentCmpanys()
        #print "timerUpdateRecentCmpanys cur cmpny=",len(_51loger.cl_viewd_cmps["hs"])
    except Exception,ex:
        print "timerUpdateRecentCmpanys e=",ex
    h=time.localtime().tm_hour
    sleepcnt = 120 if h>=8 and h<=20 else 1800
    threading.Timer(sleepcnt,timerUpdateRecentCmpanys).start()

if __name__=="__main__" :
    _51loger.getResumeStates()
    pass


from django.shortcuts import render
# Create your views here.
from django.http import HttpResponse
from django.template import Context, loader
from django.http import HttpResponseRedirect
from jobfind.models import Job,JobL,JobCompanyScore
from django.db.models import Q

sys.path.append(os.path.join(os.path.dirname(__file__),"../sh"))
from m import Job51Adder
from jobdb import mergeTable,getCompanyList

from django import forms
#from django.utils import simplejson as json

JobDbView=Job #Lesson : varable can point to a class instead of object , like macro in c++
jobAdder=Job51Adder()

JobLocalDbView=JobL


class Login51(LoginBroser):
    def hasLogin(self):
        url='http://www.51job.com/default.php'
        r=self.br.open(url)
        self.getCharsetFromResponse(r) 
        html = r.read()
        #soup=BeautifulSoup(html,fromEncoding="gbk",features="html5lib")
        soup=BeautifulSoup(html,features="html5lib")
        loginTag=soup.findAll("span",{"id":"sign_btn"})
        print("login tag cnt=",len(loginTag))
        return len(loginTag)==0
    def getLoginVerifyImg(self):
        url="https://login.51job.com/login.php?lang=c"
        html = self.Login1getPage(url)
        soup=BeautifulSoup(html,fromEncoding="gbk")
        imgTag=soup.findAll("img",{"id":"verifyPic_img"})[0]
        imgurl = imgTag.get("src")
        print("login verify img=",imgurl)
        return imgurl
    def Login(self,kvs):
        print("login uname=",kvs.get("uname"))
        form = {"loginname":kvs["uname"],
                "password":kvs["pswd"],
                "verifycode":kvs["vc"]
               }
        r = self.Login2submit(0,form)
        #print r.read().decode("gbk")

        #print r.read()

def index(request):
    if not request.is_ajax(): 
        print "index in..."
        template = loader.get_template('jobfind/b.html')
        total=JobDbView.objects.count()
        if total>0:
            start=JobDbView.objects.all()[0].id
        else:
            start=0
        print("index start=%d total=%d" %(start,total))
        context = Context({
                'start_id': start,
                'total_rcd':total,
                    })
        return HttpResponse(template.render(context))
    cmd=request.POST['cmd']
    if cmd=="CMD_UPDATA_WG":
        wc=JobDbView.objects.filter(Q(state='watch')).count()
        gc=JobDbView.objects.filter(Q(state='get')).count()
        return HttpResponse(json.dumps({"wc":wc,"gc":gc}))

def login51(request):
    haslogin = 1 if _51loger.hasLogin() else 0
    print "login51 in 2 , ajax=",request.is_ajax(),"logined=",haslogin,"l=",_51loger
    vcurl = ""
    if haslogin and not _51loger._gtimerUpdateRecentCmpanys :
        threading.Timer(120,timerUpdateRecentCmpanys).start()
        _51loger._gtimerUpdateRecentCmpanys = True

    if not request.is_ajax(): 
        if haslogin==0 :
            vcurl = _51loger.getLoginVerifyImg()
        template = loader.get_template('jobfind/login51.html')
        #context = Context({"loged":haslogin,"vcurl":urllib.quote(vcurl)})
        context = Context({"loged":haslogin,"vcurl":vcurl})
        return HttpResponse(template.render(context))

    #called by login51.html ajax
    #def login51job(request):
    #print "login51job post1 data=%s" %(request.POST)
    wktype=request.POST['type']
    if wktype=="login":
        _51loger.Login(request.POST)
        haslogin = 1 if _51loger.hasLogin() else 0
        return HttpResponse(json.dumps({"logRes":haslogin}))
    elif wktype=="updateImg":
        vcurl = _51loger.getLoginVerifyImg()
        return HttpResponse(json.dumps({"src":vcurl}))
    elif wktype=="updateCookie":
        #print "updateCookie cc=",request.POST['cookie']
        _51loger.cl_cookieStr = request.POST['cookie']
        haslogin = 1 if _51loger.hasLogin() else 0
        return HttpResponse(json.dumps({"haslogin":haslogin}))
    elif wktype=="getRecentCmpanys":
        return HttpResponse(json.dumps(_51loger.getRecentCmpanys(int(request.POST['num']))))

def detail(request, poll_id):
    print "detail in..."
    try:
        j=JobDbView.objects.get(id=int(poll_id))
        if j!=None: 
            jdict=model2dict(j)
            jdict['jobsCnt']=JobDbView.objects.count()
            css="-1"
            cs=None
            try:
                cs=JobCompanyScore.objects.get(coname=j.coname)
            except Exception,ex:
                print "company score not scan yet!"
            if(cs!=None):
                css=cs.score
            jdict['compScore']=css
            res= "%s" %dict2json(jdict)
        return HttpResponse("%s" %res)
    except Exception,ex: 
        print Exception,':',ex
        print traceback.print_exc()
   

def modify(request,rcdid):
    print "modify(%s) in..." %rcdid
    try:
        def changeStatus(db,request):
            j=db.objects.get(id=int(rcdid))
            modifystatus=request.POST.get('status')
            print "modifystatus=%s" %(modifystatus)
            #print "detail(%d)" %(int(poll_id))
            if modifystatus != None and len(modifystatus)>0:#modify the id status
                j.state=modifystatus
                j.save()

            wc=db.objects.filter(Q(state='watch')).count()
            gc=db.objects.filter(Q(state='get')).count()
            return HttpResponse(json.dumps({"watch":wc,"get":gc}))

        def updateSendDate(db,request):
            job=db.objects.filter(Q(id=request.POST.get("id")))[0]
            job.sendate=request.POST['sendate']
            job.sendcnt+=1
            job.save()
            return HttpResponse(json.dumps({"res":1,"sendcnt":job.sendcnt}))
        if request.POST.get('db')=='db_get' :
            db=Job
        elif request.POST.get('db')=='db_local' :
            db=JobLocalDbView
        if(request.POST.get('cmd')=="CMD_CHANGE_STATUS"):
            return changeStatus(db,request)
        if(request.POST.get('cmd')=="CMD_UPDATE_SENDDATA"):
            return updateSendDate(db,request)

    except Exception,ex: 
        print Exception,':',ex
        print traceback.print_exc()
        return HttpResponse(json.dumps({"code":1}))
    return HttpResponse(json.dumps({"code":1}))

class QuerryForm(forms.Form):
    searchkey = forms.CharField(required=True)
    locate = forms.CharField(required=True)
    publishday = forms.IntegerField()

def querry(request):
    print "querry in..."
    if not request.is_ajax(): 
        template = loader.get_template('jobfind/q.html')
        context = Context({
                'start_id': 0,
                'total_rcd':0,
                    })
        return HttpResponse(template.render(context))
    else: #ajax
        form = QuerryForm(request.POST)
        print "post data=%s" %(request.POST)
        keyword=request.POST.get('searchkey')
        if keyword=="STOP":
            jobAdder.userStopped=True
            return HttpResponse(json.dumps({"code":"STOP"}))
        if request.POST.get('extracmd')=="LIST_HIGH_COMPANY":
            lstr=getCompanyList(int(keyword))
            return HttpResponse(json.dumps({"code":"LIST_HIGH_COMPANY","res":lstr}))
        jobarea=request.POST.get('workarea')
        issuedate=request.POST.get('publishday') 
        jobAdder.setQuerryDict(request.POST)
        if form.is_valid():
            searchkey=request.POST.get('searchkey')
            print "searchkey=%s" %searchkey
            return HttpResponse(json.dumps({"code":0}))
        try:
            #raise Exception("test")
            jobAdder.addJob(keyword,jobarea,issuedate,1,-1)
            jobAdder.userStopped=False
        except Exception,ex: 
            print Exception,':',ex
            print traceback.print_exc()
        return HttpResponse(json.dumps({"code":jobAdder.mFinishReason}))
        

def submitstatus(request):
    try:
        mergeTable() 
        return HttpResponseRedirect("index")
    except Exception,ex:
        print Exception,':',ex
        print traceback.print_exc()
    #if request.is_ajax():
        
def dbg(msg):
    print msg
def viewljobs(request):
    try:
        vlj=ViewLocalJobs()
        if request.method == 'POST':
            return vlj.getPostResponse(request)
        dbg("viewljobs Get")
        return vlj.getGetResponst(request)
    except Exception,ex:
        print Exception,':',ex



class ViewLocalJobs():
    def getLocalList(self):
        locations=(JobLocalDbView.objects.values_list('local').distinct()) #lesson django orm:select on column and distinct
        utflocals=[]
        for l in locations:
            l=list(l)[0].encode('utf8')
            l=l[:l.find('-')]
            if l not in utflocals:
                utflocals.append(l)
        return utflocals      
    def getStatusList(self):
        jobstatus=JobLocalDbView.objects.values_list('state').distinct()
        utfstatus=[]
        for l in jobstatus:
            l=list(l)[0].encode('utf8')
            if l not in utfstatus:
                utfstatus.append(l)
        return utfstatus
   
    def getGetResponst(self,request):
        template = loader.get_template('jobfind/viewljobs.html')
        jobs=JobLocalDbView.objects.filter(Q(state='watch')|Q(state='get')).order_by("-udate").order_by("coname") #Lesson django,orm querry whith OR
        #use order_by(-column) to desc sort
        #jobs=JobL.objects.filter(state='watch')
        dbg("ViewLocalJobs getGetResponst jobs")
        context = Context({
                'jobstatus':self.getStatusList(),
                'joblocals':self.getLocalList(),
                'joblist': jobs,
                'cnt':jobs.count(),
                    })
        return HttpResponse(template.render(context))
    def getPostResponse(self,request):
        template = loader.get_template('jobfind/viewljobs_table.html')
        print request.POST
        if(request.POST.get('cmd')=="UPDATE_JOB"):
            _51loger.getResumeStates()
            return self.updateJob(request)
        if(request.POST.get('cmd')=="UPDATE_SENDDATA"):
            return self.updateSendDate(request)
        if(request.POST.get('cmd')=="UPDATE_STATUS"):
            return self.updateStatus(request)

        jobs=JobLocalDbView.objects.order_by("coname")
        #SHOW_JOBS
        if(request.POST.get('cmd')=="SHOW_JOBS"):
            local=request.POST.get('local')
            if len(local)>0:
                jobs=jobs.filter(local__contains=local)  #Lesson django orm:querry with sql like :colum__xxx

            status=request.POST.get('status')
            if len(status)>0:
                jobs=jobs.filter(state__exact=status)
        
        if(request.POST.get('cmd')=="SEARCH_COMP"):
            coname=request.POST.get('coname')
            if len(coname)>0:
                jobs=jobs.filter(coname__contains=coname)  #Lesson django orm:querry with sql like :colum__xxx
        print(request.POST.get('cmd'),"total=",jobs.count())

        context = Context({
                'jobstatus':self.getStatusList(),
                'joblocals':self.getLocalList(),
                'joblist': jobs,
                'cnt':jobs.count(),
                    })

        return HttpResponse(template.render(context))

    def updateSendDate(self,request):
        job=JobLocalDbView.objects.filter(Q(id=request.POST.get("id")))[0]
        job.sendate=request.POST['sendate']
        job.sendcnt+=1
        job.save()
        return HttpResponse(json.dumps({"res":1,"sendcnt":job.sendcnt}))

    def updateStatus(self,request):
        job=JobLocalDbView.objects.filter(Q(id=request.POST.get("id")))[0]
        job.state=request.POST['status']
        job.save()
        return HttpResponse(json.dumps({"res":1,"status":job.state}))

    def updateJob(self,request):
        job=JobLocalDbView.objects.filter(Q(id=request.POST.get("id")))[0] #Lesson django,orm querry whith OR
        qd={'filterkeys':'linux','keywordtype':'100','serverActionType':55}
        jobAdder.setQuerryDict(qd)
        update=jobAdder.getUpdate(job.jobu)
        updateres="not_update"
        #updateres="updated"
        if update!=job.udate:
            job.udate=update
            job.save()
            updateres="updated"
        rsmSt = ""
        jid = re.findall('\d{5,}',job.jobu)[0]
        print jid,job.jobu,job.job,jid in _51loger.resume_status
        if jid in _51loger.resume_status.keys() :
            rsmSt = _51loger.resume_status[jid]['status']+_51loger.resume_status[jid]['holders']
            print "======================",rsmSt,jid
        return HttpResponse(json.dumps({"res":updateres,"newDate":update,"rs":rsmSt}))
        #jobs=JobLocalDbView.objects.filter(Q(state='watch')|Q(state='get')) #Lesson django,orm querry whith OR
        #return HttpResponse(json.dumps({"code":"post local"}))
  









