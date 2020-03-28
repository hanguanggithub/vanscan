from django.shortcuts import render, HttpResponse, redirect
from django.views.generic import View
from django.views.decorators.csrf import csrf_exempt
from .forms import DomainForm, PortForm, OtherdomainForm, FuckcmsForm
from script import portscan, otherdomain,whatweb
import requests
import json, os
from poc.main import *
import script.awvs12 as awvs12
import script.awvs13 as awvs13


def index(request):
    return render(request, 'awvs13.html')

class Whatweb(View):
    form = DomainForm()
    def get(self, request):
        return render(request, 'whatweb.html', context={'form': self.form})
    def post(self, request):
        domain = request.POST['domain']
        info = whatweb.bugscanerapi(domain)
        info2= whatweb.bugscanerapi2(domain)
        yun = whatweb.yunsee(domain)
        msg = '查询失败，请检查域名是否有效，如果是第一次查询请等两分钟后再查下试试'
        return render(request, 'whatweb.html', context={'form': self.form,'msg':domain ,'info': info,'info2': info2,"yun":yun})
# cms识别
class Whatcms(View):
    form = DomainForm()
    proxies={
    'http':'http://127.0.0.1:8080',
    'https':'https://127.0.0.1:8080'
}
    def get(self, request):
        return render(request, 'whatcms.html', context={'form': self.form})

    def post(self, request):
        domain = request.POST['domain']
        info = self.cmsinfo(domain)
        msg = '查询失败，请检查域名是否有效，如果是第一次查询请等两分钟后再查下试试'
        if type(info) == dict:
            return render(request, 'whatcms.html', context={'form': self.form, 'info': info})
        else:
            return render(request, 'whatcms.html', context={'form': self.form, 'msg': msg})

    def cmsinfo(self, url):
        #API = 'http://api.yunsee.cn/[自行修改此处]'
        #payload = {'level': '2', 'url': url}
        API=  'http://www.yunsee.cn/home/getInfo'
        data={"type":"webinfo","url":url}
        try:
            req = requests.post(API, data=data, timeout=30,verify=False)#,proxies=proxies)
            print(req.text)
            code = json.loads(req.text)['code']
            print("code======",code)
            if code == 1:
                #info = json.loads(req.text)['data']
                info = json.loads(req.text)['res']
                print("info=====",info)
                return info
            if code ==0 :
                mess=json.loads(req.text)['mess']
                print(msg)
                return mess
        except Exception as e:
            print(e)
            return None


# 端口扫描
class Portscan(View):
    form = PortForm()

    def get(self, request):
        return render(request, 'portscan.html', context={'form': self.form})

    def post(self, request):
        ip = request.POST['ip']
        num = request.POST['num']
        timeout = request.POST['timeout']
        ports = portscan.run(num, ip, timeout)
        return render(request, 'portscan.html', context={'form': self.form, 'ports': ports})


class Otherdomain(View):
    form = OtherdomainForm()

    def get(self, request):
        return render(request, 'otherdomain.html', context={'form': self.form})

    def post(self, request):
        domain = request.POST['domain']
        ip,info = otherdomain.run(domain)
        return render(request, 'otherdomain.html',
                      context={'form': self.form, 'domain': domain, 'info': info, 'ip': ip})


class Fuckcms(View):
    def get(self, request):
        data = json.dumps(list(poclist.keys()))
        print(data)
        return render(request, 'fuckcms.html', context={'data': data})

    def post(self, request):
        return render(request, 'fuckcms.html')


@csrf_exempt
def api_cms(request):
    if request.method == 'POST':
        url = request.POST['url']
        type = request.POST['type']
        print(url, type)
        result = list(poclist.values())[int(type)](url).run()
        if '[+]' in result:
            status = 1
            return HttpResponse(json.dumps({"status": status, "pocresult": result}))
        else:
            result = '[-]没洞'
            status = 0
            return HttpResponse(json.dumps({"status": status, "pocresult": result}))


class Awvs(View):
    def get(self, request):
        scan_list = awvs12.getscans()
        return render(request, 'awvs12.html', context={'scan_list': scan_list})

    def post(self, request):
        return render(request, 'awvs12.html')


class Awvs13(View):
    def get(self, request):
        scan_list = awvs13.getscans()
        groups=awvs13.getgroups()
        return render(request, 'awvs13.html', context={'scan_list': scan_list,'groups':groups})

    def post(self, request):
        scan_list = awvs13.getscans()
        groups=awvs13.getgroups()
        print('AWVS13',request.POST.getlist('groups'))
        return render(request, 'awvs13.html', context={'scan_list': scan_list,'groups':groups})

