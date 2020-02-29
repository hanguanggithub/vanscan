# ! usr/bin/env python
#  -*- coding: utf-8 -*-
import requests, json
import requests.packages.urllib3.exceptions
import time
from django.shortcuts import render, HttpResponse, redirect
from django.views.decorators.csrf import csrf_exempt
requests.packages.urllib3.disable_warnings()
Auth = "抓包获取auth"
API = 'https://ip:port/api/v1'
headers = {
    'X-Auth': Auth,
    'content-type': 'application/json'
}
cookie={
    "ui_session":Auth

}
proxies={
    'http':'http://127.0.0.1:8080',
    'https':'https://127.0.0.1:8080'
}

def gettarget():
    # 获取全部目标
    req = requests.get(API + '/targets', headers=headers,cookies=cookie, verify=False)
    infos = json.loads(req.text)
    print(infos)
    targets = []
    for info in infos['targets']:
        print(info['target_id'], info['address'], info['description'], info['last_scan_date'])


def getscans():
    try:
        req = requests.get(API + '/scans', headers=headers,cookies=cookie, verify=False,timeout=10)#,proxies=proxies)
        scans = json.loads(req.text)
        scan_list = []
        for scan in scans['scans']:
            scanid = scan['scan_id']
            address = scan['target']['address']
            description = scan['target']['description']
            status = scan['current_session']['status'].replace('aborted', '已取消').replace('processing', '进行中').replace('completed','已完成').replace('queued','就绪中')
            scan_dict = {'scanid': scanid, 'address': address, 'description': description, 'status': status}
            scan_list.append(scan_dict)
        return scan_list
    except Exception as e:
        print(e)
        return None


def scan_del(scan_id):
    req = requests.delete(API + '/scans/' + scan_id,cookies=cookie, headers=headers, verify=False)
    if req.status_code == 204:
        return True
    else:
        return False

#停止扫描
def scan_stop(scan_id):
    req = requests.post(API + '/scans/' + scan_id + '/abort' ,headers=headers,cookies=cookie,
                            verify=False)
    print(req.text)
    if req.status_code == 204:
        return True
    else:
        return False
#添加扫描
def scan_add(target):
    data = {'address': target, 'description': '', 'criticality': 10}
    r = requests.post(url=API + '/targets', timeout=10,
                      verify=False, headers=headers, cookies=cookie,data=json.dumps(data))
    if r.status_code == 201:
        target_id =  json.loads(r.text)['target_id']
        data = {'target_id': target_id, 'profile_id': "11111111-1111-1111-1111-111111111111",
                'schedule': {'disable': False, 'start_date': None, 'time_sensitive': False}}
        try:
            r = requests.post(url=API + '/scans', timeout=10,
                              verify=False, cookies=cookie,headers=headers, data=json.dumps(data))
            if r.status_code == 201:
                print('[-] OK, 扫描任务已经启动...')
                return True
            else:
                return False
        except Exception as e:
            print(e)

#生成
def bg(scanid):
    #生成报告
    try:
        data = {'template_id': '11111111-1111-1111-1111-111111111115',
                'source': {'list_type': 'scans', 'id_list': [scanid]}}
        r = requests.post(url=API + '/reports', timeout=10,
                          verify=False, headers=headers,cookies=cookie, data=json.dumps(data))

        if r.status_code == 201:
            download(r.headers['Location'])
            return True
        else:
            return False
    except Exception as e:
        print(e)

def download(path):
    # 下载报告
    try:
        r = requests.get(url=API.replace('/api/v1', '') + path,
                         timeout=10, verify=False, headers=headers,cookies=cookie)
        response = json.loads(r.text)
        report_id = response['report_id']
        target = response['source']['description']
        print('[-] 报告生成中...')
        # 等待报告生成
        while True:
            time.sleep(5)
            _r = requests.get(API+'/reports/' + report_id,headers=headers,cookies=cookie,
                             verify=False)
            name = json.loads(_r.text)['source']['description'].replace(';','')
            if json.loads(_r.text)['status'] == 'completed':
                downurl=(json.loads(_r.text)['download'][1])   #0=html ,1=pdf
                print("报告下载链接:",API.replace('/api/v1', '')+downurl)
                res = requests.get(API.replace('/api/v1', '')+downurl, verify=False, timeout=10, headers=headers,cookies=cookie)
                if res.status_code == 200:
                    print('[-] OK, 报告下载成功.')
                    name = name.replace(':','_').replace('/','_')
                    with open('报告'+'/'+name + '.pdf', 'wb') as f:
                        f.write(res.content)
                    break
    except Exception as e:
        print(e)

def request(path):
    try:
        return requests.get(url=API + path, timeout=10,headers=headers,cookies=cookie,
                            verify=False)
    except Exception as e:
        print(e)

def api_getsessionid(scan_id):
    r = requests.get(API+'/scans/'+scan_id, headers=headers,cookies=cookie,verify=False)
    req = json.loads(r.text)
    return req['current_session']['scan_session_id']


def api_getvulns(scan_id,scan_session_id):
    r = requests.get(API+"/scans/"+scan_id+"/results/"+scan_session_id+"/vulnerabilities",headers=headers,cookies=cookie,verify=False)# ,proxies=proxies)
    req = json.loads(r.text)

    if not req['pagination']["next_cursor"] ==None:    #漏洞数量超过100
        next_cursor=req['pagination']["next_cursor"]
        reqmax=req['vulnerabilities']
        while next_cursor and next_cursor>0:
            url=API+"/scans/"+scan_id+"/results/"+scan_session_id+"/vulnerabilities?c={}".format(next_cursor)
            rnext = requests.get(url,headers=headers,cookies=cookie,verify=False)# ,proxies=proxies)
            reqnext = json.loads(rnext.text)
            next_cursor=reqnext['pagination']["next_cursor"]
            reqmax+=reqnext['vulnerabilities']
        return reqmax
    return req['vulnerabilities']


@csrf_exempt
def del_scan(request):
    if request.method == 'POST':
        if scan_del(scan_id=request.POST['scanid']):
            print("删除成功")
            return HttpResponse(1)
    else:
        print("删除失败")
        return HttpResponse(0)

@csrf_exempt
def stop_scan(request):
    if request.method == 'POST':
        if scan_stop(scan_id=request.POST['scanid']):
            print("停止成功")
            return HttpResponse(1)
        else:
            print("停止失败")
            return HttpResponse(0)

@csrf_exempt
def add_scan(request):
    if request.method == 'POST':
        target= request.POST['target']
        print(target)
        if scan_add(target):
            print("添加成功")
            return HttpResponse(1)
    else:
        print("添加失败")
        return HttpResponse(0)

@csrf_exempt
def Presentation(request):
    if request.method == 'POST':
        scan_id = request.POST['scanid']
        print(scan_id)
        if bg(scan_id):
            print("导出成功")
            return HttpResponse(1)
        else:
            print("导出失败")
            return HttpResponse(0)

@csrf_exempt
def get_vluns(request):
    if request.method == 'POST':
        scan_id = request.POST['scanid']
        session_id = api_getsessionid(scan_id)
        vulns = api_getvulns(scan_id,session_id)
        return HttpResponse(json.dumps(vulns))

