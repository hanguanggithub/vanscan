# ! usr/bin/env python
#  -*- coding: utf-8 -*-
# @Author  : Y4er
# @File    : otherdomain.py
import requests, json, socket
API = 'http://www.webscan.cc/?action=query'



def getip(domain):
    #domain=("http://test.vulnweb.com/")
    if "http" in domain:
        domain = domain.split("://")[1]
    if "/" in domain:
        domain=domain.split("/")[0]
    try:
        ip = socket.gethostbyname(domain)
        return ip
    except Exception as e:
        print(e)
        pass


def cduan(ip):
    cduaninfo = []
    a = ".".join(ip.split(".")[0:-1]) + "."
    for i in range(1, 10):
        ip = a + str(i)
        print("runip:",ip)
        cduaninfo.append(ip+run(ip))
        print(cduaninfo)
    return cduaninfo


def ipfancha(ip): #IP反查域名
    data = {
        'ip': ip,
    }
    try:
        req = requests.get(API, params=data).text
        if req.startswith(u'\ufeff'):
            req = req.encode('utf8')[3:].decode('utf8')
        info = json.loads(req)
        return info
    except:
        return None

def run(domain): #IP反查域名
    ip = getip(domain)
    info=ipfancha(ip)
    return ip,info

run("http://test.vulnweb.com/")