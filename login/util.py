#!/usr/bin/env python
# -*- coding: utf-8 -*- #
__author__ = "huangy"
__copyright__ = "Copyright 2016, The metagenome Project"
__version__ = "1.0.0-dev"
import  os
import  time


def handle_uploaded_file(f):
    file_name = ""

    try:
        path = "media/editor" + time.strftime('/%Y/%m/%d/%H/%M/%S/')
        if not os.path.exists(path):
            if f.size/(1024*1024)>10:
                return "error :file size >10M can't upload"
            else:
                os.makedirs(path)
                file_name = path + f.name
                destination = open(file_name, 'wb+')
                for chunk in f.chunks():
                    destination.write(chunk)
                destination.close()
    except Exception as e:
        print(e)

    return file_name
def setSelf(cf,af,sectionName,name):
    if not sectionName in cf.sections():
        cf.add_section(sectionName)
    value = af.cleaned_data[name]
    cf.set(sectionName,name,str(value))
