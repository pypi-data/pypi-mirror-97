# -*- coding: utf-8 -*-
"""
Created on Wed Sep  2 23:39:44 2020

@author: ZSL
"""

# -*- coding: utf-8 -*-
"""
Created on Sat Aug 29 21:43:55 2020

@author: ZSL
"""

from QUANTAXIS.QAFetch.QATdx_adv import QA_Tdx_Executor
from QUANTAXIS.QAEngine.QAThreadEngine import QA_Thread
from QUANTAXIS.QAARP.QAUser import QA_User
import threading
import QAPUBSUB
import QUANTAXIS as QA
from QAPUBSUB.consumer import subscriber_routing,subscriber_topic
from QAPUBSUB.producer import publisher_routing,publisher_topic
from QUANTAXIS.QAUtil.QAParameter import MARKET_TYPE, FREQUENCE
from QUANTAXIS.QAUtil.QADate_trade import QA_util_if_tradetime
import time
import json
import pandas as pd
import numpy as np

class qz_realtime_tick():
    def __init__(self, username='ziyu', password='ziyu',if_pub=False,time_get_tick=3):
        self.user = QA_User(username=username, password=password)
#        self.type=_type
        self.if_pub=if_pub
        self.QA_Tdx_Executor=QA_Tdx_Executor()
        self.QA_Tdx_Executor.timeout=float(5)
        self.time_get_tick=time_get_tick
        if self.if_pub:
            self.pub_tick=publisher_topic(exchange='qz_realtime_tick', )  
    def __repr__(self):
        return 'qz_realtime_tick'
    def subscribe(self, code):
        """继续订阅
        Arguments:
            code {[type]} -- [description]
        """
        self.user.sub_code(code)

    def unsubscribe(self, code):
        self.user.unsub_code(code)

    def get_ticks(self):

        aa=self.QA_Tdx_Executor._queue.qsize()#用来主动更新股票池
        if aa>0:                
            data = self.QA_Tdx_Executor.get_realtime_concurrent(self.user.subscribed_code[MARKET_TYPE.STOCK_CN])
    #                    print('Connection Pool NOW LEFT {} Available IP'.format(
    #                        self._queue.qsize()))
            print(data)
            data_=data[0]
            data_['updatetime']=data[1]
            
            data2=data_
            data=data2[['code','servertime','updatetime','open','price','last_close','high','low','vol','cur_vol','amount',
                        'bid_vol1','bid1','bid_vol2','bid2','bid_vol3','bid3','bid_vol4','bid4','bid_vol5','bid5',
                        'ask_vol1','ask1','ask_vol2','ask2','ask_vol3','ask3','ask_vol4','ask4','ask_vol5','ask5',
                        's_vol', 'b_vol'
                       ]]
            clom =['code','servertime','updatetime','open','close','last_close','high','low','vol','cur_vol','amount',
                         'b1_v', 'b1_p', 'b2_v', 'b2_p', 'b3_v', 'b3_p', 'b4_v', 'b4_p', 'b5_v', 'b5_p',
                         'a1_v', 'a1_p', 'a2_v', 'a2_p', 'a3_v', 'a3_p', 'a4_v', 'a4_p', 'a5_v', 'a5_p',
                        's_vol', 'b_vol'
                       ] 
            data.columns=clom 
            #data.rename(columns={'price': 'close'}, inplace=True)
            if self.if_pub:
                self.pub_tick.pub(json.dumps(data.to_dict()), routing_key='000001.SZ.000300.000050')
            #print(data)
            return data 
    def get_ticks_continue(self):
        while 1:
            try:
                #if QA_util_if_tradetime()==True: 
                data=self.get_ticks()
            except:
                pass
            time.sleep(self.time_get_tick*(1+np.random.random()))
        return data                          
    def run(self):
        threading.Thread(target=self.get_ticks).start()    
                   

if __name__ == "__main__":
#    z1 = subscriber_topic(exchange='qz_realtime_tick', routing_key='000001.#')
#    z1.callback = lambda a, b, c, x: print('tick订阅数据{}'.format(x))
#    threading.Thread(target=z1.start).start()
    
    self = qz_realtime_tick()
    self.subscribe('000001')
    
#    self.subscribe('000002')
#    self.subscribe('000005')
#    codelist=QA.QA_fetch_stock_list().code.tolist()
#    for i in codelist[:2000]:
#        self.subscribe(i)
#    self.start()
    
    
