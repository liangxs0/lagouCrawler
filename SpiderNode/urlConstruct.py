#-*-coding:utf-8-*-



def urlConstruct(city):
    base_url="https://www.lagou.com/jobs/positionAjax.json?"
    pk="default"
    needAddtionalResult="false"
    url=base_url+"pk=default&"+"city="+city+"&needAddtionalResult=false"
    return url
