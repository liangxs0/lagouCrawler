#-*-coding:utf-8-*-
from multiprocessing.managers import BaseManager
from multiprocessing import Process,Queue
import Downloader
import DataClean
import sys




def download_proc(communication_q):
    pass


class SpiderNode:
    def __init__(self,host='',port=8000,authkey=b''):
        self.host=host
        self.port=port
        self.authkey=authkey

        BaseManager.register('get_result_q')
        print("Connecting to server %s:%s"%(self.host,self.port))
        self.manager=BaseManager(address=(self.host,self.port),authkey=authkey)
        self.manager.connect()
        self.result_q=self.manager.get_result_q()


    #开始爬取，向主控节点发送数据
    def crawl(self):
        while True:
            #创建一个下载器和数据清洗器之间的一个通信队列
            communication_q=Queue()
            #创建下载器和数据清洗器进程
            downloader=Downloader.Downloader()
            dataclener=DataClean.DataClean(self.result_q)
            proc_downloader=Process(target=downloader.getJsonData,args=(communication_q,))
            proc_datacleaner=Process(target=dataclener.cleanJsonData,args=(communication_q,))

            proc_downloader.start()
            proc_datacleaner.start()

            proc_downloader.join()
            proc_datacleaner.join()
            print("Get ready to finish work...")
            sys.exit(0)

if __name__=='__main__':
    spider=SpiderNode(host='127.0.0.1',authkey=b"lagou")
    spider.crawl()
