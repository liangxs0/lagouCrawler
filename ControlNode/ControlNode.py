#-*-coding:utf-8-*-

import DataStoreManager
from multiprocessing import Queue,Process
from multiprocessing.managers import BaseManager
import sys
import time

class ControlNode(object):
    def __init__(self,host='',port=8000,authkey=b''):
        self.host=host
        self.port=port
        self.authkey=authkey


    def startManager(self,result_q):
        BaseManager.register('get_result_q',callable=lambda:result_q)
        manager=BaseManager(address=(self.host,self.port),authkey=self.authkey)
        print("server on %s:%s"%(self.host,self.port))
        return manager


def store_proc(result_q):
    dataManager=DataStoreManager.DataStoreManager()
    while True:
        if not result_q.empty():
            print("start receiving data from spider node...")
            data=result_q.get(True)
            if data=="end":
                print("Spider running out...")
                dataManager.closeConnection()
                sys.exit(0)
            else:
                dataManager.storeToDatabase(data)
                continue
        else:
            time.sleep(10)

if __name__=='__main__':
    result_q=Queue()
    controler=ControlNode(authkey=b"lagou")
    manager=controler.startManager(result_q)
    dataManager=DataStoreManager.DataStoreManager()

    proc_datastore=Process(target=store_proc,args=(result_q,))

    proc_datastore.start()

    manager.get_server().serve_forever()
