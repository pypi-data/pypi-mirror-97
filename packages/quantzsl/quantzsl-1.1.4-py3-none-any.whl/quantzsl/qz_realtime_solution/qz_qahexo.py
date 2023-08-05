import json
import click
import pymongo
from QAPUBSUB.consumer import subscriber_topic
from QUANTAXIS.QAEngine import QA_Thread
import datetime
import threading
import time
import inspect
import ctypes
from QUANTAXIS.QAUtil import (
                              QA_util_if_tradetime,
                              QA_util_if_trade

                              ) 
from multiprocessing import Pool, Process
from qaenv import mongo_ip, mongo_uri
class sub_realtime(QA_Thread):
    def __init__(self, host='www.yutiansut.com', port=5678):
        super().__init__()
        self.subscriber = subscriber_topic(
            host=host,
            port=port,
            exchange='QARealtimePro_FIX',
            durable=False,
            vhost='/',
            routing_key='*')
        #pymongo.MongoClient().qa.drop_collection('REALTIMEPRO_FIX')
        self.db = pymongo.MongoClient(mongo_uri).qa[
            'realtime_{}'.format(datetime.date.today())]

        self.db.create_index(
            [
                ('code',
                 pymongo.ASCENDING),
                ('datetime',
                 pymongo.ASCENDING),
                ('frequence',
                 pymongo.ASCENDING),
            ]
        )
        # self.subscriber.callback = self.callback
        # self.subscriber.start()
    def callback(self, a, b, c, data):
        """这里是订阅处理逻辑

        Arguments:
            a {[type]} -- [description]
            b {[type]} -- [description]
            c {[type]} -- [description]
            data {[type]} -- [description]
        """
        res = json.loads(data, encoding='utf-8')
#        print('{}正在储存数据,code:{},frequence:{}'.format(
#        datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
#        str(res[0]['code']),
#        str(res[0]['frequence'])
#                    ))
#        print('dd')
        self.data=res
        self.on_fixdata(res)

    def on_fixdata(self, data):
        self.db.insert_many(data)


    def run(self):
        
        self.subscriber.callback = self.callback
        t=threading.Thread(target=self.subscriber.start)
        t.start()
        #self.subscriber.start()

def _async_raise(tid, exctype):
    """raises the exception, performs cleanup if needed"""
    tid = ctypes.c_long(tid)
    if not inspect.isclass(exctype):
        exctype = type(exctype)
    res = ctypes.pythonapi.PyThreadState_SetAsyncExc(tid, ctypes.py_object(exctype))
    if res == 0:
        raise ValueError("invalid thread id")
    elif res != 1:
        # """if it returns a number greater than one, you're in trouble,
        # and you should call it again with exc=NULL to revert the effect"""
        ctypes.pythonapi.PyThreadState_SetAsyncExc(tid, None)
        raise SystemError("PyThreadState_SetAsyncExc failed")
 
 
def stop_thread(thread):
    _async_raise(thread.ident, SystemExit)

def qarealtime_fix(a=3):
    sub_realtime().start()
    #print("{},马上开盘，hexo开始工作".format(datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"))  )    

def run():
    pass
    count=0
    self=sub_realtime()
    while 1:
        date=datetime.datetime.now().strftime("%Y-%m-%d")
        mini=datetime.datetime.now().strftime("%H%M")
        time_=datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        if QA_util_if_trade(date):
            if mini=='0915' and count==0:
                self.subscriber.callback = self.callback
                t = threading.Thread(target=self.subscriber.start)
                t.start()  
                count+=1
                print("{},马上开盘，hexo开始工作".format(datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"))  )    
            elif mini=='1133' and count==1:
                stop_thread(t)
                print("{},午盘休息，hexo停止工作".format(datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")))
                count-=1
            elif mini=='1259' and count==0:
                self.subscriber.callback = self.callback
                t = threading.Thread(target=self.subscriber.start)
                t.start()  
                count+=1
                print("{},马上开盘，hexo开始工作".format(datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")))                 
            elif mini=='1133' and count==1:
                stop_thread(t)
                print("{},全天结束，hexo停止工作".format(datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")))
                count-=1  
        else:
            pass
        time.sleep(10)  
  
if __name__ == '__main__':
#    self=sub_realtime()
#    self.subscriber.callback = self.callback
#    t = threading.Thread(target=self.subscriber.start)
#    t.start() 
#    if t.is_alive:
#        print('8')
#    import sys
#    mini_=datetime.datetime.now().strftime("%H%M")
#    while 1:
#        print("{},hexo正在工作".format(datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")))        
#        time.sleep(30)
#        date=datetime.datetime.now().strftime("%Y-%m-%d")
#        mini=datetime.datetime.now().strftime("%H%M")
#        time_=datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
#        if mini==str(int(mini_)+2):
#            print("要停止了")
#            #exit()
#            sys.exit()
    import sys 
    date=datetime.datetime.now().strftime("%Y-%m-%d")
    mini=datetime.datetime.now().strftime("%H%M")
    time_=datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")      
    if QA_util_if_trade(date): 
        
        p = Process(target=qarealtime_fix)
        p.start() 
        print("{},hexo启动完成。。".format(datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")))        
        time.sleep(100)         
        while 1:
            time.sleep(60)         
            date=datetime.datetime.now().strftime("%Y-%m-%d")
            mini=datetime.datetime.now().strftime("%H%M")
            time_=datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
           
            if p.is_alive:
                pass
            else:
                p = Process(target=qarealtime_fix)
                p.start()  
                
            if str(mini)[-1:]=='0' :           
                print("{},hexo正在工作".format(datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")))
    
            if mini=='1133' or mini=='1503':
                p.terminate()
                p.join()
                sys.exit()
#    while 1:
#        date=datetime.datetime.now().strftime("%Y-%m-%d")
#        mini=datetime.datetime.now().strftime("%H%M")
#        time_=datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
#        if QA_util_if_trade(date):
#            if mini>'0929' and mini<'1130':
#                if signal_am_open==0: #第一次启动
#                    try:
#                        p = Process(target=qarealtime_fix)
#                        p.start() 
#                        signal_am_open+=1
#                        signal_am_close=0
#                        print("{},马上开盘，hexo开始工作".format(datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"))  )                        
#                    except:
#                        pass                
#                try:    
#                    if p.is_alive:
#                        pass
#                    else:
#                        p = Process(target=qarealtime_fix)
#                        p.start() 
#                except:
#                    pass                        
#                            
#
#            elif mini>'1130' and mini<'1141':
#                try:
#                    if p.is_alive:
#                        # stop a process gracefully
#                        p.terminate()
#                        p.join()                     
#                        print("{},午盘休息，hexo停止工作".format(datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")))
#                        signal_am_close+=1
#                        signal_am_open=0
#                except:
#                    pass                    
#
#            elif mini>'1259'and mini<'1500':
#                if signal_pm_open==0: #第一次启动
#                    try:
#                        p = Process(target=qarealtime_fix)
#                        p.start() 
#                        signal_pm_open+=1
#                        print("{},马上开盘，hexo开始工作".format(datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"))  )                        
#                    except:
#                        pass                
#                try:    
#                    if p.is_alive:
#                        pass
#                    else:
#                        p = Process(target=qarealtime_fix)
#                        p.start() 
#                except:
#                    pass  
#            elif mini>'1500' and mini<'1503':
#                try:
#                    if p.is_alive:
#                        # stop a process gracefully
#                        p.terminate()
#                        p.join() 
#                        print("{},全天结束，hexo停止工作".format(datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")))
#                        signal_pm_close+=1
#                        signal_pm_open=0
#                except:
#                    pass                 
#            time.sleep(10)
#            if signal_am_open==1 or signal_pm_open==1:
#                pass
#                print("{},hexo正在工作".format(datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")))
#                time.sleep(50)
##            if mini=='1510':
##                signal_am_open=0 
##                signal_pm_close=0
#           
#        else:
#            pass
#            print("{},非交易日期，hexo不工作".format(datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")))
#            time.sleep(3600*3)

#    
#    signal_am_open=0
#    signal_am_close=0
#    signal_pm_open=0
#    signal_pm_close=0
#    try:
#        p = Process(target=qarealtime_fix)
#        p.start() 
#        signal_am_open+=1
#        signal_am_close=0
#        print("{},马上开盘，hexo开始工作".format(datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"))  )                        
#        print(p)
#    except:
#        pass
#    print('启动成功  '+str(signal_am_open))  
#    for i in range(4):    
#        time.sleep(10)
#        print(p)
#        print(str(i))
#    try:
#        if p.is_alive:
#            # stop a process gracefully
#            p.terminate()
#            p.join()
#            print(p)
#        else:
#            print('启动失败  '+str(signal_am_open))                    
#        print("{},午盘休息，hexo停止工作".format(datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")))
#        signal_am_close+=1
#        signal_am_open=0
#        print(p)
#    except:
#        pass                    
#    for i in range(4):    
#        time.sleep(10)
#        print(p)
#        print(str(i))  
#    self=sub_realtime()
#    signal_am_open=0
#    signal_am_close=0
#    signal_pm_open=0
#    signal_pm_close=0
#    while 1:
#        date=datetime.datetime.now().strftime("%Y-%m-%d")
#        mini=datetime.datetime.now().strftime("%H%M")
#        time_=datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
#        if QA_util_if_trade(date):
#            if mini>'0915' and mini<'1130' and signal_am_open==0:
#                try:
#                    p = Process(target=qarealtime_fix)
#                    p.start() 
#                    signal_am_open+=1
#                    signal_am_close=0
#                    print("{},马上开盘，hexo开始工作".format(datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"))  )                        
#                except:
#                    pass
#            elif mini>'1130' and mini<'1141' and signal_am_close==0:
#                try:
#                    if p.is_alive:
#                        # stop a process gracefully
#                        p.terminate()
#                        p.join()                     
#                    print("{},午盘休息，hexo停止工作".format(datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")))
#                    signal_am_close+=1
#                    signal_am_open=0
#                except:
#                    pass                    
#
#            elif mini>'1259'and mini<'1500' and signal_pm_open==0:
#                try:
#                    p = Process(target=qarealtime_fix)
#                    p.start()  
#                    signal_pm_open+=1
#                    signal_pm_close=0
#                    print("{},马上开盘，hexo开始工作".format(datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"))  )                        
#                except:
#                    pass                    
#            elif mini>'1500' and mini<'1503' and signal_pm_close==0:
#                try:
#                    if p.is_alive:
#                        # stop a process gracefully
#                        p.terminate()
#                        p.join() 
#                    print("{},全天结束，hexo停止工作".format(datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")))
#                    signal_pm_close+=1
#                    signal_pm_open=0
#                except:
#                    pass                 
#            time.sleep(10)
#            if signal_am_open==1 or signal_pm_open==1:
#                pass
#                print("{},hexo正在工作".format(datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")))
#                time.sleep(50)
#            if signal_am_close==1:
#                pass
#                print("{},hexo正在工作".format(datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")))
#                time.sleep(50)               
#        else:
#            pass
#            print("{},非交易日期，hexo不工作".format(datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")))
#            time.sleep(3600*3)
    # self=sub_realtime()
    # #self.start() 
    # QA_util_if_tradetime
    # self.subscriber.callback = self.callback
    # t = threading.Thread(target=self.subscriber.start)
    # t.start()
    # time.sleep(0.001)
    # stop_thread(t)
    # print("stoped")
    # while 1:
    #     time.sleep(1)
    #     pass