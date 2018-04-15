#-*-coding:utf-8-*-
import requests
from lxml import etree
import json
import urllib.parse

#获取首页的工作分类
def getIndexPageJob():
    url="https://www.lagou.com/"
    header={'User-Agent':"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/65.0.3325.146 Safari/537.36"}
    proxies={"http":"http://127.0.0.1:50157"}
    html=requests.get(url,headers=header,proxies=proxies)

    jobs=[]
    if html.status_code==200:
        html_parser=etree.HTML(html.text)
        menu_sub=html_parser.xpath('//*[@id="sidebar"]/div/div[1]/div[2]')[0]

        dls=menu_sub.xpath('./dl')
        for dl in dls:
            info=dl.xpath('./dd/a/text()')
            jobs.extend(info)
    print(jobs)
    return jobs

#获取全部的热点城市
def getAllCity():
    url="https://www.lagou.com/"
    url_zhaopin="https://www.lagou.com/jobs/list_C%2B%2B?px=default&city=%E5%85%A8%E5%9B%BD#filterBox"
    header={'User-Agent':'Mozilla/5.0(Macintosh;U;IntelMacOSX10_6_8;en-us)AppleWebKit/534.50(KHTML,likeGecko)Version/5.1Safari/534.50',

            'Host': 'www.lagou.com',
            'Referer': 'https://www.lagou.com/',

    }
    session=requests.Session()
    session.get(url,headers=header)
    proxies={"http":"http://127.0.0.1:50157"}
    html=session.get(url_zhaopin,headers=header,proxies=proxies)

    if html.status_code==200:
        html_parser=etree.HTML(html.text)
        hot=html_parser.xpath('//li[@class="hot"]/a[@class="more-city-name"]/text()')
        other=html_parser.xpath('//li[@class="other"]/a[@class="more-city-name"]/text()')
        cities=hot+other
        print(cities)
        for i in range(len(cities)):
            cities[i]=urllib.parse.quote(cities[i])
        return cities

"""if __name__=='__main__':
    cities=getAllCity()
    print(cities)"""
