from django.shortcuts import render
import os
# Create your views here.
from django.http import HttpResponse
from django.template import Context, loader
from django.http import HttpResponseRedirect
from jobfind.models import Job,JobL
from django.db.models import Q
import sys,traceback
sys.path.append("/home/sin/wkspace/soft/python/pub/utility/")
from uty import *
sys.path.append("/home/sin/wkspace/webserver/django/mysite/sh")
from m import Job51Adder
from jobdb import mergeTable

from django import forms
from django.utils import simplejson as json

JobDbView=Job #Lesson : varable can point to a class instead of object , like macro in c++
jobAdder=Job51Adder()
def index(request):
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


def detail(request, poll_id):
    print "detail in..."
    try:
        j=JobDbView.objects.get(id=int(poll_id))
        if j!=None: 
            jdict=model2dict(j)
            jdict['jobsCnt']=JobDbView.objects.count()
            res= "%s" %dict2json(jdict)
        return HttpResponse("%s" %res)
    except Exception,ex: 
        print Exception,':',ex
        print traceback.print_exc()
   

def modify(request,rcdid):
    print "modify(%s) in..." %rcdid
    try:
        j=Job.objects.get(id=int(rcdid))
        modifystatus=request.POST.get('status')
        print "modifystatus=%s" %(modifystatus)
        #print "detail(%d)" %(int(poll_id))
        if modifystatus != None and len(modifystatus)>0:#modify the id status
            j.state=modifystatus
            j.save()
        return HttpResponse(json.dumps({"code":0}))
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
            return HttpResponse(json.dumps({"code":"stopped"}))

        jobarea=request.POST.get('workarea')
        issuedate=request.POST.get('publishday') 
        if form.is_valid():
            searchkey=request.POST.get('searchkey')
            print "searchkey=%s" %searchkey
            return HttpResponse(json.dumps({"code":0}))
        try:
            jobAdder.addJob(keyword,jobarea,issuedate,1,50)
            jobAdder.userStopped=False
        except Exception,ex: 
            print Exception,':',ex
            print traceback.print_exc()
        return HttpResponse(json.dumps({"code":"load job finished"}))
        

def submitstatus(request):
    try:
        mergeTable() 
        return HttpResponseRedirect("index")
    except Exception,ex:
        print Exception,':',ex
        print traceback.print_exc()
    #if request.is_ajax():
        
def viewljobs(request):
    template = loader.get_template('jobfind/viewljobs.html')
    jobs=JobL.objects.filter(Q(state='watch')|Q(state='get')) #Lesson django,orm querry whith OR
    #jobs=JobL.objects.filter(state='watch')
    context = Context({
            'joblist': jobs,
                })
    return HttpResponse(template.render(context))
   
