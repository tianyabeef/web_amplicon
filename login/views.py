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

TOPIC_CHOICES = (
    ('leve1', '差评'),
    ('leve2', '中评'),
    ('leve3', '好评'),
)
class AnalysisForm(forms.Form):
    #must option
    groupfile = forms.ChoiceField(label='group文件',required=True,choices=TOPIC_CHOICES)
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
                fu = FileUpload(filename)
                fu.save()
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
    if request.method == 'POST':
        af = AnalysisForm(request.POST)
        if af.is_valid():
            job_id = af.cleaned_data['job_id']
            data_type = af.cleaed_data['data_type']
            work_dir = af.cleaed_data['work_dir']
            #group_files = af.cleaed_data['group_files']
            #alpha_group_file = af.cleaed_data['alpha_group_file']
            #raw_data_dir =af.cleaed_data['raw_data_dir']
            #fq_for_merge =af.cleaed_data['fq_for_merge']
            #name_list =af.cleaed_data['name_list']
            require =af.cleaed_data['require']
            #pipeline_shell =af.cleaed_data['pipeline_shell']
            sequence_platform =af.cleaed_data['sequence_platform']
            project_name =af.cleaed_data['project_name']
            customer_name =af.cleaed_data['customer_name']
            project_num =af.cleaed_data['project_num']
            sample_source =af.cleaed_data['sample_source']
            sample_type =af.cleaed_data['sample_type']
            note_information =af.cleaed_data['note_information']
            project_contacts =af.cleaed_data['project_contacts']
            phone =af.cleaed_data['phone']
            email =af.cleaed_data['email']
            enterprise_name =af.cleaed_data['enterprise_name']
            enterprise_address =af.cleaed_data['enterprise_address']
            salesman =af.cleaed_data['salesman']
            sale_phone =af.cleaed_data['sale_phone']
            sale_email =af.cleaed_data['sale_email']
            os.popen('mkdir %s' % work_dir)
            os.popen('mkdir %s/group/' % work_dir)
            os.popen('mkdir %s/rawData' % work_dir)
            return render_to_response('success.html')
    else:
        af = AnalysisForm()
    return render_to_response("analysis.html",{'af':af})
#下载结果
def download(request):
    pass