#-*-coding:utf-8-*-
import sys
import time


class DataClean:
    def __init__(self,result_q):
        self.result_q=result_q

    def cleanJsonData(self,communication_q):
        while True:
            #取出传过来的json数据
            if not communication_q.empty():
                json_data=communication_q.get(True,10)
            else:
                time.sleep(2)
                continue
            if json_data=='end':
                break
            job_info={}
            category=json_data['category']

            results=json_data['content']['positionResult']['result']
            for result in results:
                jobName=result['positionName']
                workYear=result['workYear']
                company=result['companyShortName']
                city=result['city']
                salary=result['salary']
                advantage=result['positionAdvantage']
                district=result['district']
                companyScale=result['companySize']
                financeStage=result['financeStage']
                firstType=result['firstType']
                secondType=result['secondType']
                #job_info={'category':category,'jobName':jobName,'workYear':workYear,'company':company,'city':city,'salary':salary,'advantage':advantage,'district':district,'companyScale':companyScale,'financeStage':financeStage,'firstType':firstType,'secondType':secondType}
                job_info=[category,jobName,workYear,company,city,salary,advantage,district,companyScale,financeStage,firstType,secondType]
                print("Start sending jobinfo to controler....")
                self.result_q.put(job_info,True,10)
        print("Data process work finish,start to inform controler to exit....")
        self.result_q.put('end',True,10)
        sys.exit(0)
