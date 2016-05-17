#from django.shortcuts import render

# Create your views here.
#coding=utf-8

import os

from django.shortcuts import render,render_to_response
from django.http import HttpResponseRedirect
from login.models import User
from login.models import FileUpload
from django import forms
from login import util
import configparser

group_choices = ()


#定义表单模型
class UserForm(forms.Form):
    username = forms.CharField(label='用户名：',max_length=100,required=True)
    password = forms.CharField(label='密码：',widget=forms.PasswordInput())
#定义上传文件表达模型
class FileUploadForm(forms.Form):
    title = forms.CharField(label='标题',required=True)
    file = forms.FileField(label='选择文件',required=True)
#分析
class AnalysisForm(forms.Form):
    #must option

    group_files_ori = forms.ModelChoiceField(label='group文件',required=True,queryset=FileUpload.objects.all())
    raw_data_file = forms.CharField(label="原始文件路径",required=True,widget=forms.Textarea)
    job_id = forms.CharField(label="sge任务名称",required=True)
    data_type = forms.CharField(label='类型:',required=True)
    work_dir = forms.CharField(label='工作目录:',required=True)
    #group_files = forms.CharField(label="分组文件",required=True)
    #alpha_group_file = forms.CharField(label="alpha的分组文件",required=True)
    #raw_data_dir = forms.CharField(label="原始序列目录",required=True)
    #fq_for_merge = forms.CharField(label="原始序列文件",required=True)
    #name_list = forms.CharField(label="样品名称文件",required=True)
    require = forms.IntegerField(label="数据量",required=True)
    #pipeline_shell = forms.CharField(label="脚本目录",required=True)
    #sequence_platform is miseq or hiseq
    sequence_platform = forms.CharField(label="测序平台",required=True)
#    [project]
    #must option
    project_name = forms.CharField(label="项目名称",required=True)
    customer_name = forms.CharField(label="客户名称",required=True)
    project_num = forms.CharField(label="项目编号",required=True)
    sample_source = forms.CharField(label="样品来源",required=True)
    sample_type = forms.CharField(label="样品类型",required=True)
    note_information = forms.CharField(label="备注信息",required=True)
    project_contacts = forms.CharField(label="项目联系人",required=True)
    phone = forms.IntegerField(label="联系电话",required=True)
    email = forms.EmailField(label="邮箱",required=True)
    enterprise_name = forms.CharField(label="单位名称",required=True)
    enterprise_address = forms.CharField(label="单位地址",required=True)
    salesman = forms.CharField(label="科技代表",required=True)
    sale_phone = forms.IntegerField(label="联系电话",required=True)
    sale_email = forms.EmailField(label="邮箱",required=True)







#登录
def login(request):
    if request.method == 'POST':
        uf = UserForm(request.POST)
        if uf.is_valid():
            #获取表单用户密码
            username = uf.cleaned_data['username']
            password = uf.cleaned_data['password']
            #获取的表单数据与数据库进行比较
            user = User.objects.filter(username__exact = username,password__exact = password)
            if user:
                request.session['username'] = username
                request.session['password'] = password
                return render_to_response('success.html',{'username':username})
            else:
                return HttpResponseRedirect('/login/')
    else:
        uf = UserForm()
    return render_to_response('login.html',{'uf':uf})
#添加gourp
def addgroup(request):
    username = (request.session['username'])

    if request.method == 'POST':
        fform = FileUploadForm(request.POST, request.FILES)
        if fform.is_valid():
            title = fform.cleaned_data['title']
            filename = util.handle_uploaded_file(request.FILES['file'])
            if filename == "error :file size >10M can't upload":
                return HttpResponseRedirect('/addgroup/?error=y')
            else:
                FileUpload.objects.create(title = title,username = username,file = filename)
                return HttpResponseRedirect('/addgroup/?error=n')

    else:
        error = request.GET.get('error')
        fform = FileUploadForm()
        if error:
            return render_to_response("addgroup.html",{'fform':fform,'error':error,'username':username})
    return render_to_response("addgroup.html",{'fform':fform,'username':username})
#分析
def analysis(request):
    username = (request.session['username'])
    group_choices = ((x.file,x.title) for x in FileUpload.objects.filter(username=username))
    if request.method == 'POST':
        af = AnalysisForm(request.POST)
        if af.is_valid():
            work_dir = af.cleaned_data['work_dir']
            cf = configparser.ConfigParser()
            util.setSelf(cf,af,'params','job_id')
            util.setSelf(cf,af,'params','data_type')
            util.setSelf(cf,af,'params','work_dir')
            util.setSelf(cf,af,'params','require')
            util.setSelf(cf,af,'params','sequence_platform')
            util.setSelf(cf,af,'project','project_name')
            util.setSelf(cf,af,'project','customer_name')
            util.setSelf(cf,af,'project','project_num')
            util.setSelf(cf,af,'project','sample_source')
            util.setSelf(cf,af,'project','sample_type')
            util.setSelf(cf,af,'project','note_information')
            util.setSelf(cf,af,'project','project_contacts')
            util.setSelf(cf,af,'project','phone')
            util.setSelf(cf,af,'project','email')
            util.setSelf(cf,af,'project','enterprise_name')
            util.setSelf(cf,af,'project','enterprise_address')
            util.setSelf(cf,af,'project','salesman')
            util.setSelf(cf,af,'project','sale_phone')
            util.setSelf(cf,af,'project','sale_email')
            util.setSelf(cf,af,'params','group_files_ori')
            cf.set('params','pipeline_shell','%s/pipeline.sh'% work_dir)
            raw_data_file = ''
            tabs = af.cleaned_data['raw_data_file'].strip().split("\n")
            for t in tabs:
                t = t.strip()
                raw_data_file = '%s %s' % (raw_data_file,t)
            cf.set('params','fq_for_merge',raw_data_file)
            #raw_data_dir =af.cleaed_data['raw_data_dir']
            #fq_for_merge =af.cleaed_data['fq_for_merge']
            #name_list =af.cleaed_data['name_list']
            #pipeline_shell =af.cleaed_data['pipeline_shell']

            os.popen('mkdir %s' % work_dir)
            os.popen('mkdir %s/group/' % work_dir)
            os.popen('mkdir %s/rawData' % work_dir)
            cf.write(open("%s/work_pre.cfg" % work_dir, "w"))
            return render_to_response('success.html',{'username':username})
    else:
        af = AnalysisForm({'groupfile':group_choices})
    return render_to_response("analysis.html",{'af':af,'username':username})
#下载结果
def download(request):
    username = (request.session['username'])
    pass
