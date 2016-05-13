#from django.shortcuts import render

# Create your views here.
#coding=utf-8
from django.shortcuts import render,render_to_response
from django.http import HttpResponseRedirect
from login.models import User
from django import forms
from login import util


#定义表单模型
class UserForm(forms.Form):
    username = forms.CharField(label='用户名：',max_length=100,required=True)
    password = forms.CharField(label='密码：',widget=forms.PasswordInput())
#定义上传文件表达模型
class FileUploadForm(forms.Form):
    title = forms.CharField(max_length=50)
    file = forms.FileField()
#登录
def login(request):
    if request.method == 'POST':
        uf = UserForm(request.POST)
        if uf.is_valid():
            #获取表单用户密码
            username = uf.cleaned_data['username']
            password = uf.cleaned_data['password']
            print(username)
            print(password)
            #获取的表单数据与数据库进行比较
            user = User.objects.filter(username__exact = username,password__exact = password)
            if user:
                return render_to_response('success.html',{'username':username})
            else:

                return HttpResponseRedirect('/login/')
    else:
        uf = UserForm()
    return render_to_response('login.html',{'uf':uf})
#添加gourp
def addgroup(request):
    if request.method == 'POST':
        form = FileUploadForm(request.POST, request.FILES)
        if form.is_valid():
            filename = util.handle_uploaded_file(request.FILES['file'])
            print(filename)
            if filename == "error :file size >10M can't upload":
                return HttpResponseRedirect('/addgroup/?error=y')
            else:
                return HttpResponseRedirect('/addgroup/?error=n')
    else:
        error = request.GET.get('error')
        form = FileUploadForm()
    if error:
        return render_to_response("addgroup.html",{'form':form,'error':error})
    else:
        return render_to_response("addgroup.html",{'form':form})
#分析
def analysis(request):
    pass
#下载结果
def download(request):
    pass