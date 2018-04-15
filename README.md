这个爬虫针对拉钩网的所有技术岗位进行爬取   

![image](https://github.com/lrtxpra/lagouCrawler/raw/master/pics/lagou.PNG)

爬虫采用分布式架构，ControlNode为主控节点，SpiderNode为爬虫节点

![image](https://github.com/lrtxpra/lagouCrawler/blob/master/pics/controltree.PNG?raw=true)
![image](https://github.com/lrtxpra/lagouCrawler/blob/master/pics/spidertree.PNG?raw=true)   

其中主控节点主要包括两个部分，一个是控制调度器 ControlNode.py ,一个是存储控制器 DataStoreManager.py
爬虫节点分为三部分，爬虫调度器 SpiderNode.py , 下载器 Downloader.py  数据清洗器 DtaClean.py

result_q为爬虫节点中的数据清洗器向主控节点数据存储器传数据的队列

下载器和数据清洗器之间通过communication_q进行获取到的json数据传输

下载器中设置了多个User-Agent定时进行更换，同时cookie也每三次请求更换一次

第一次运行爬虫，顺利爬取了9375条数据，但是没有预料到的是突然就抛出异常
![image](https://github.com/lrtxpra/lagouCrawler/raw/master/pics/spider.PNG)

异常
![image](https://github.com/lrtxpra/lagouCrawler/raw/master/pics/error.PNG)
> ssl.SSLEOFError: EOF occurred in violation of protocol (_ssl.c:777)   
> urllib.error.URLError: urlopen error EOF occurred in violation of protocol (_ssl.c:777)    

我查了一下，仍然没有弄明白和两个错误发生的原因。后续会继续更新此文档

 2018/4/15
