#!/usr/bin/env python
# -*- coding: utf-8 -*- #
__author__ = "huangy"
__copyright__ = "Copyright 2016, The metagenome Project"
__version__ = "1.0.0-dev"

from django.conf.urls import patterns, url
from login import views


urlpatterns = patterns('',
    url(r'^$', views.login, name='login'),
    url(r'^$', views.login, name='addgroup'),
    url(r'^$', views.login, name='analysis'),
    url(r'^$', views.login, name='download'),

)