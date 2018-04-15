#-*-coding:utf-8-*-
import sys,os
name=os.path.dirname(os.path.dirname(os.path.realpath(__file__)))
sys.path.append(name)
import preWork,urlConstruct
import requests
import json
import time
import random
import urllib.request
import urllib.parse
import http.cookiejar


class Downloader:
    def __init__(self):
        self.base_url="https://www.lagou.com/jobs/positionAjax.json"
        self.jobs=preWork.getIndexPageJob()
        time.sleep(10)
        self.cities=preWork.getAllCity()
        time.sleep(10)
        self.headers={
            'Accept':'application/json, text/javascript, */*; q=0.01',
            'Accept-Language':'zh-CN,zh;q=0.8,zh-TW;q=0.7,zh-HK;q=0.5,en-US;q=0.3,en;q=0.2',
            'Cache-Control':'max-age=0',
            'Content-Length':23,
            'Content-Type':'application/x-www-form-urlencoded; charset=UTF-8',
            'Host':'www.lagou.com',
            'Referer':'https://www.lagou.com/jobs/list_Java?px=default&city=%E5%8C%97%E4%BA%AC',
            'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:59.0) Gecko/20100101 Firefox/59.0',
            'X-Anit-Forge-Code':0,
            'X-Anit-Forge-Token':'None',
            'X-Requested-With':'XMLHttpRequest'
            }
        self.user_agent=[
                'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:59.0) Gecko/20100101 Firefox/59.0',
                'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/535.1 (KHTML, like Gecko) Chrome/14.0.835.163 Safari/535.1',
                'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:6.0) Gecko/20100101 Firefox/6.0',
                'Opera/9.80 (Windows NT 6.1; U; zh-cn) Presto/2.9.168 Version/11.50',
                'Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 6.1; WOW64; Trident/5.0; SLCC2; .NET CLR 2.0.50727; .NET CLR 3.5.30729; .NET CLR 3.0.30729; Media Center PC 6.0; InfoPath.3; .NET4.0C; .NET4.0E; SE 2.X MetaSr 1.0)',
                'Mozilla/5.0 (Windows; U; Windows NT 6.1; en-US) AppleWebKit/534.3 (KHTML, like Gecko) Chrome/6.0.472.33 Safari/534.3 SE 2.X MetaSr 1.0 ',
                'Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.1; WOW64; Trident/5.0; SLCC2; .NET CLR 2.0.50727; .NET CLR 3.5.30729; .NET CLR 3.0.30729; Media Center PC 6.0; InfoPath.3; .NET4.0C; .NET4.0E)',
                'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/535.1 (KHTML, like Gecko) Chrome/13.0.782.41 Safari/535.1 QQBrowser/6.9.11079.201',
                'Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 6.1; WOW64; Trident/5.0; SLCC2; .NET CLR 2.0.50727; .NET CLR 3.5.30729; .NET CLR 3.0.30729; Media Center PC 6.0; InfoPath.3; .NET4.0C; .NET4.0E) QQBrowser/6.9.11079.201',
                ]

    #获取json数据
    def getJsonData(self,communication_q):
        counter=0   #请求计数器
        index=0     #user_agent列表索引
        #通过对各个城市的遍历，然后依次获取每个工作的招聘信息
        for city in self.cities:
            url=urlConstruct.urlConstruct(city)
            for job in self.jobs:
                self.headers["Referer"]="https://www.lagou.com/jobs/list_%s?px=default&city=%s"%(job,city)
                page=1
                data={'first':'true','kd':'java','pn':1}
                cookie=http.cookiejar.CookieJar()
                opener=urllib.request.build_opener(urllib.request.HTTPCookieProcessor(cookie))
                while True:
                    data['pn']=page
                    postdata=urllib.parse.urlencode(data).encode(encoding='utf-8')
                    req=urllib.request.Request(url,postdata,self.headers)
                    res=opener.open(req)
                    counter+=1
                    html=res.read().decode('utf-8')
                    json_data=json.loads(html)
                    print(json_data["success"],page)
                    print(len(json_data["content"]["positionResult"]["result"]))
                    print(cookie)
                    for item in cookie:
                        print("Name: %s"%item.name)
                        print("Value: %s"%item.value)
                    print("+******************************************************************************+")
                    #开始将json_data传送给cleanprocess
                    if res.code==200 and json_data["success"]==True and len(json_data["content"]["positionResult"]["result"])>0:
                        json_data['category']=job
                        print("sending information to celan process...")
                        communication_q.put(json_data,True,10)

                        #开始对下一次请求的组件及参数进行更新
                        page+=1
                        if counter==3:
                            counter=0
                            index+=1
                            if index>=9:
                                index=0
                            self.headers['User-Agent']=self.user_agent[index]
                            cookie=http.cookiejar.CookieJar()
                            opener=urllib.request.build_opener(urllib.request.HTTPCookieProcessor(cookie))
                        time.sleep(random.randint(7,12))
                        continue
                    else:
                        break
        print("start to inform clean process to stop communicating...")
        communication_q.put('end')
        sys.exit(0)
