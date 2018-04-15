#-*-coding:utf-8-*-

import pymysql
import sys
class DataStoreManager:
    def __init__(self):
        self.conn=pymysql.connect(host='127.0.0.1',port=3306,user='root',passwd='root',db='lagou',charset='utf8')
        self.cursor=self.conn.cursor()


    #存储数据到数据库
    def storeToDatabase(self,data):
        try:
            sql="insert into jobdetails(category,jobName,workYear,company,city,salary,advantage,district,companyScale,financeStage,firstType,secondType) values(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"
            self.cursor.execute(sql,data)
            self.conn.commit()
            print("saved one record to database...")
        except Exception:
            pass    #如果execute执行错误，忽略掉，

    #关闭数据库连接
    def closeConnection(self):
        self.cursor.close()
        self.conn.close()

if __name__=='__main__':
    d=DataStoreManager()
