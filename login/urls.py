#!/usr/bin/env python
# -*- coding: utf-8 -*- #
__author__ = "huangy"
__copyright__ = "Copyright 2016, The metagenome Project"
__version__ = "1.0.0-dev"

from django.conf.urls import patterns, url
from login import views


urlpatterns = patterns('',
    url(r'^$', views.login, name='login'),
)