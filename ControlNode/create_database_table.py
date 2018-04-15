from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column,String,Integer
import pymysql

pymysql.install_as_MySQLdb()

engine=create_engine('mysql://root:root@localhost:3306/lagou?charset=utf8')
Base=declarative_base()

class JobDetails(Base):
    __tablename__='jobdetails'

    id=Column(Integer,primary_key=True)
    category=Column(String(20))
    jobName=Column(String(50))
    workYear=Column(String(20))
    company=Column(String(50))
    city=Column(String(20))
    salary=Column(String(30))
    advantage=Column(String(100))
    district=Column(String(20))
    companyScale=Column(String(20))
    financeStage=Column(String(30))
    firstType=Column(String(30))
    secondType=Column(String(30))

#创建表
Base.metadata.create_all(engine)
