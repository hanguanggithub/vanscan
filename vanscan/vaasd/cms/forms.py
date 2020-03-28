# ! usr/bin/env python
#  -*- coding: utf-8 -*-
# @Author  : Y4er
# @File    : forms.py

from django import forms


class DomainForm(forms.Form):
    domain = forms.CharField(label="域名",initial="http://test.vulnweb.com/")
    


class PortForm(forms.Form):
    ip = forms.CharField(label="IP",initial="127.0.0.1")
    num = forms.CharField(label="线程数",initial="5")
    timeout = forms.CharField(label="超时数",initial="5")


class OtherdomainForm(forms.Form):
    domain = forms.CharField(label="请输入你要查询的IP或域名",initial="http://test.vulnweb.com/")


class FuckcmsForm(forms.Form):
    domain = forms.CharField(label="请输入IP或域名",initial="http://test.vulnweb.com/")
