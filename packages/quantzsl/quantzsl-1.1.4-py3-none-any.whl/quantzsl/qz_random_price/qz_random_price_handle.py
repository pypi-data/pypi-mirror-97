# -*- coding: utf-8 -*-
"""
Created on Thu Oct  1 13:54:45 2020

@author: ZSL
"""

# -*- coding: utf-8 -*-
"""
Created on Sat Sep  5 21:45:08 2020

@author: ZSL
"""

import pandas as pd
import numpy as np 
import tushare as ts 
import QUANTAXIS as QA
import time
import datetime
import threading
import talib
import warnings
import json
import copy
import pymongo
from QUANTAXIS.QAARP.QAUser import QA_User
from QUANTAXIS.QAFetch.QATdx_adv import QA_Tdx_Executor
from QAPUBSUB.consumer import subscriber_routing,subscriber_topic
from QAPUBSUB.producer import publisher_routing,publisher_topic
from QUANTAXIS.QAData.data_resample import QA_data_tick_resample
from QUANTAXIS.QAUtil import (
    QA_util_get_next_day,
    QA_util_get_real_date,
    QA_util_get_last_day,
    QA_util_if_tradetime,
    QA_util_to_json_from_pandas,
    MARKET_TYPE,
    FREQUENCE
                )
warnings.filterwarnings("ignore")
import quantzsl as qz
from quantzsl import qz_realtime_tick_tdx
from quantzsl import qz_random_price

#self=qz_realtime_tick()
#self.get_ticks()
#    get_ticks.subscribe('000001')
#    self.subscribe('000002')
#    self.subscribe('000005')
class qz_realtime_handle():
    def __init__(self, username='ziyu', password='ziyu',
                 code=['000001'],
                 frequence=['1min','5min','15min','30min','60min','day'],
                 time_update=3,timeout=0.5,                
                 source='tdx',model='real'):
        pass
        self.user = QA_User(username=username, password=password)
        if source=='tdx':
            self.get_tick=qz_realtime_tick_tdx()
            self.get_tick.QA_Tdx_Executor.timeout=float(timeout)
            self.get_tick.user=self.user                        
        self.data={}
        self.time_update=time_update
        self.STOCK_CN=QA.QAUtil.QAParameter.MARKET_TYPE.STOCK_CN
        self.INDEX_CN=QA.QAUtil.QAParameter.MARKET_TYPE.STOCK_CN    
        for i in code:
            self.subscribe(i)
        self.frequence=frequence
        self.model=model
        for i in frequence:
            pass
            if i in ['day', 'd', 'D', 'DAY', 'Day']:
                self.pub_day=publisher_topic(exchange='qz_realtime_day', )
            if i in ['w', 'W', 'Week', 'week']:
                self.pub_week=publisher_topic(exchange='qz_realtime_week', )
            if i in ['1', '1m', '1min', 'one']:
                self.pub_1min=publisher_topic(exchange='qz_realtime_1min', )
            if i in ['5', '5m', '5min', 'five']:
                self.pub_5min=publisher_topic(exchange='qz_realtime_5min', )
            if i in ['15', '15m', '15min', 'fifteen']:
                self.pub_15min=publisher_topic(exchange='qz_realtime_15min', )
            if i in ['30', '30m', '30min', 'half']:
                self.pub_30min=publisher_topic(exchange='qz_realtime_30min', )
            if i in ['60', '60m', '60min', '1h']:
                self.pub_60min=publisher_topic(exchange='qz_realtime_60min', )
          
        self.pub_tick=publisher_topic(exchange='qz_realtime_tick', )  
          
        #pymongo.MongoClient().qa.drop_collection('REALTIMEPRO_FIX')
        self.db = pymongo.MongoClient().quantzsl.realtime

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
    def subscribe(self, code):
        """继续订阅
        Arguments:
            code {[type]} -- [description]
        """
        self.user.sub_code(code)

    def unsubscribe(self, code):        
        self.user.unsub_code(code)    

    def run_realtime_hand(self):
        print("{} 启动实时tick采集。".format(datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")))        
        while 1:
            t1=time.time()
            if self.model=='test' or self.model=='random':
                if_tradetime=True
            else:
                if_tradetime=QA_util_if_tradetime()
            if if_tradetime:            
                try:
                    self.realtime_hand()                                           
                except Exception as ex:
                    lastEx = ex     
                    print("{}  {}。".format(datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"),lastEx))
                time.sleep(max(0.01,self.time_update-(time.time()-t1)))
            else:
                print("{} run_realtime_hand函数发生错误：非交易时间。".format(datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")))            
                time.sleep(60)        
    def realtime_hand(self,if_random=False): 
        '''
        读取5当数据，并转换为实时tick
        '''
        t=time.time()   
        retry = 20
        for _ in range(retry):
            try:
                res=self.get_tick.get_ticks()
                #print(res)
                #res=pd.read_hdf(download_path+'/realtime.h5').drop_duplicates()  #此处应获取全市场的tick，否则将卖股票不再监控之列的话，就无法获取当时价格，还有以后如果进行全市场实时情绪分析等也需要全市场的实时tick    
                self.tick_this_=res[res['open']!=0]
                self.tick_this=self.tick_this_     
                try:
                    df = self.tick_this[['code','close']]
                    df=df.assign(change=self.tick_this['close']-self.tick_last['close'])
                    self.tick_last = self.tick_this
                    #print('success')
                except:#第一次         
                    df = self.tick_this[['code','close']]
                    self.tick_last = self.tick_this.copy(deep=True)
                    df=df.assign(change=self.tick_this['close']-self.tick_last['close'])
                tick_columns=['code','servertime','updatetime','open','high','low','close','vol','cur_vol','amount']
                dfa=self.tick_this_[tick_columns].sort_values(by="code" )
                df=dfa.assign(change=self.tick_this['close']-self.tick_last['close'])
                df= df.assign(type= df['change'].map(lambda x: np.where(x>=0, '买入', '卖出'))).set_index('code')
                self.data[self.STOCK_CN+'_tick']=df.T        
                code=self.user.subscribed_code[MARKET_TYPE.STOCK_CN]
                df2=df[df.index.isin(code)]    #code 为监控股票池 除self.tick包含全部股票外 其他实时1、5min，日线均为监控股票数据      
                time_=df.servertime.values[0][:8]
                date_=datetime.date.today().strftime("%Y-%m-%d")
                datetime_=date_+' '+time_
                #datetime_=datetime.datetime.strptime(datetime__,"%Y-%m-%d %H:%M:%S")
                
                stock_data_tick_real1={}
                tick_columns_=['open','high','low','close','vol','cur_vol','amount']
                for i in tick_columns_:
                    pass
                    stock_data_tick_real1[i]=df[[i]].T.assign(datetime=datetime_).set_index(['datetime'])          
                try:  #判断是否存在某变量    第一次运行  
                    for i in tick_columns_:
                        pass
                        self.data[self.STOCK_CN+'_tick_real'][i]=pd.concat([self.data[self.STOCK_CN+'_tick_real'][i],stock_data_tick_real1[i]],axis=0)
                        #IsDuplicated =stock_data_realtime[i].duplicated()  #判断是否重复
                        #stock_data_realtime[i]= stock_data_realtime[i].drop_duplicates()    #去重复                 
                        delta = datetime.timedelta(minutes=2,seconds=datetime_.second)       #此处只选择近2min的tick 合成分钟数据时就不需要再做处理了         
                        self.data[self.STOCK_CN+'_tick_real'][i]=self.data[self.STOCK_CN+'_tick_real'][i].loc[slice(datetime_-delta, datetime_), :]
                except:
                    self.data[self.STOCK_CN+'_tick_real']={}     
                    for i in tick_columns_:    
                        pass
                        self.data[self.STOCK_CN+'_tick_real'][i]=stock_data_tick_real1[i].T.reset_index().drop_duplicates().set_index('code').T   
                break
            except Exception as ex:
                lastEx = ex 
                if len(self.user.subscribed_code[MARKET_TYPE.STOCK_CN])>0:
                    print("{}  realtime_hand函数发生错误：通达信可用ip数量为：{}，下载数据失败，重试中：{}。".format(datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"),self.get_tick.QA_Tdx_Executor._queue.qsize(),lastEx))
                else:
                    print("{}  realtime_hand函数发生错误：订阅股票数为0，请增加订阅".format(datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")))
            time.sleep(1) 
    def updata_1min(self):
        #本着把矛盾集中在一个点的原则，仅将1min数据进行在线合成和更新，
        #其余5min等数据，在合并后的1min数据的基础上进行重采样和更新
        self.data[self.STOCK_CN+'_1min_real']=qz.qz_data_tick_resample_1min(self.data[self.STOCK_CN+'_tick_real']) 

        try:
            bar_1min=self.data[self.STOCK_CN+'_1min']           
        except:#第一次 
            self.data[self.STOCK_CN+'_1min']={}       
            bar_1min=self.data[self.STOCK_CN+'_1min_real']
            
        for i in bar_1min:
            pass
            #bar_1min[i].update(self.data[self.STOCK_CN+'_1min_real'][i])
            res1=bar_1min[i][bar_1min[i].index<self.data[self.STOCK_CN+'_1min_real'][i].index.values[0]]
            res2=self.data[self.STOCK_CN+'_1min_real'][i]
            bar_1min[i]=pd.concat([res1,res2],axis=0)[-240:] #去后240行 防止隔天收集数据太大 仅在1min这里截断就可以

        self.data[self.STOCK_CN+'_1min']=bar_1min

      

    def updata_nmin(self,n=5):
        kdata=self.data[self.STOCK_CN+'_1min']
        self.data[self.STOCK_CN+'_'+str(n)+'min_real']=qz.qz_data_1min_resample_nmin(kdata,n)        
        try:
            bar_n_min=self.data[self.STOCK_CN+'_'+str(n)+'min']
            for i in bar_n_min:
                pass
                #bar_n_min[i].update(self.data[self.STOCK_CN+'_'+str(n)+'min_real'][i]) 
                res1=bar_n_min[i](bar_n_min[i].index<self.data[self.STOCK_CN+'_'+str(n)+'min_real'][i].index.values[0])
                res2=self.data[self.STOCK_CN+'_'+str(n)+'min_real'][i]
                bar_n_min[i]=pd.concat([res1,res2],axis=0)
        except:#第一次 
            self.data[self.STOCK_CN+'_'+str(n)+'min']={} 
            for i in kdata:
                self.data[self.STOCK_CN+'_'+str(n)+'min'][i]=self.data[self.STOCK_CN+'_'+str(n)+'min_real'][i]                
            bar_n_min=self.data[self.STOCK_CN+'_'+str(n)+'min']   
            
        self.data[self.STOCK_CN+'_'+str(n)+'min']=bar_n_min 
        
        for i in self.data[self.STOCK_CN+'_'+str(n)+'min']:
            pass
            new_index=self.data[self.STOCK_CN+'_'+str(n)+'min'][i].reset_index().datetime.astype(str)
            self.data[self.STOCK_CN+'_'+str(n)+'min'][i]=self.data[self.STOCK_CN+'_'+str(n)+'min'][i].reset_index().assign(datetime=new_index
                                                    ).set_index('datetime')           
    def updata_day(self):  #将实时数据合并到日线数据里
        kdata=self.data[self.STOCK_CN+'_1min']
        self.data[self.STOCK_CN+'_day']=qz.qz_data_min_resample_day(kdata)        

    def update_data_(self,n=5):
        if n==1:
            #1分钟不需要更新所以pass即可
            data_str=self.STOCK_CN+'_'+str(n)+'min'      
        elif n=='day':
            self.updata_day()
            data_str=self.STOCK_CN+'_day'
        else:
            self.updata_nmin(n)
            data_str=self.STOCK_CN+'_'+str(n)+'min'
        data=copy.deepcopy(self.data[data_str])
        data2=copy.deepcopy(self.data[data_str])
        data3=copy.deepcopy(self.data[data_str])   
        for i in data:
            pass
            new_index=data[i].reset_index().datetime.astype(str)
            data[i]=data[i].reset_index().assign(datetime=new_index).set_index('datetime')
            data2[i]=data[i][-1:].to_dict() 
            data3[i]=data[i][-1:]
        bar=[]
        data4=pd.DataFrame()
        for i in data3:    
            pass
            aa=pd.DataFrame(data3[i].stack())
            aa.columns=[i]
            data4=pd.concat([data4,aa],axis=1)
        data4=data4.reset_index()
        if n=='day':
            data4=data4.assign(frequence='day')   
        else:
            data4=data4.assign(frequence=str(n)+'min')     
        return data2,data4

    def updata_data(self):
    
        try:
            self.updata_1min()
            for i in self.frequence:
                pass
                if i in ['5', '5m', '5min', 'five']:
                    data,data2=self.update_data_(5)
                    self.pub_5min.pub(json.dumps(data), routing_key='000001.SZ.000300.000050')
                    self.db.update(
                        {
                            'portfolio_cookie': self.portfolio_cookie,
                            'user_cookie': self.user_cookie
                        },
                        {'$set': self.message},
                        upsert=True
                        )
                    self.db.insert_many(QA_util_to_json_from_pandas(data2))
                elif i in ['15', '15m', '15min', 'fifteen']:
                    data,data2=self.update_data_(15)
                    self.pub_15min.pub(json.dumps(data), routing_key='000001.SZ.000300.000050')
                                          
                elif i in ['30', '30m', '30min', 'half']:
                    data,data2=self.update_data_(30)
                    self.pub_30min.pub(json.dumps(data), routing_key='000001.SZ.000300.000050') 
                    
                elif i in ['60', '60m', '60min', '1h']:
                    data,data2=self.update_data_(60)
                    self.pub_60min.pub(json.dumps(data), routing_key='000001.SZ.000300.000050') 
                                     
                elif i in ['1', '1m', '1min', 'one']:
                    data,data2=self.update_data_(1)
                    self.pub_1min.pub(json.dumps(data2), routing_key='000001.SZ.000300.000050')
                                                                    
                elif i in ['day', 'd', 'D', 'DAY', 'Day']: 
                    data,data2=self.update_data_('day')         
                    self.pub_day.pub(json.dumps(data2), routing_key='000001.SZ.000300.000050')
                                                           
        except Exception as ex:
            lastEx = ex     
            print("{} updata_data函数发生错误： {}。".format(datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"),lastEx))
       
    def updata_data_random_price(self):

        self.updata_data()

       
    def updata_data_realtime(self):
        t1=time.time()
        while 1:            
            if len(self.data)>1:
                time.sleep(max(0.01,self.time_update-(time.time()-t1))) #此处不能变，原因是tick收集和resample是两个线程，没有此处当self.data>1时
                #会立即执行此处代码 tick_real还没有准备好 会发生错误
                t1=time.time()
                if self.model=='test' or self.model=='random':
                    if_tradetime=True
                else:
                    if_tradetime=QA_util_if_tradetime()
                if if_tradetime: 
                    self.updata_data()
                else:
                    time.sleep(60)
                    print("resample:{}  非交易时间。".format(datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")))                          
     
                    
    def run(self):
        threading.Thread(target=self.run_realtime_hand).start()  
        threading.Thread(target=self.updata_data_realtime).start() 
        
    def get_random_price(self):
                
        random_price=qz_random_price(code=self.user.subscribed_code[MARKET_TYPE.STOCK_CN],
                                     start_day='2020-01-03',
                                     end_day='2020-01-03',
                                     freq='3min',
                                     price=1,
                                     mu=2,  #目标值  即最后价格为初始价格的n倍
                                     sigma=2,  #回归过程中的扰动大小   
                                     theta=0.1, #回归速度
                                     dt=0.01
                                     ) 
        random_price=random_price.get_random_price()
        return random_price#.plot()

    def run_random_price_hand(self):
        random_price=self.get_random_price()
        
        for i in random_price.index:
            pass
            #i=random_price.index[2]
            t1=time.time()            
            try:  
                t2=time.time()
                tick=random_price.loc[[i],:]
                self.random_price_hand(tick) 
                self.updata_data_random_price() 
                print(str(round(time.time()-t2,3))+'   '+i)                                       
            except Exception as ex:
                lastEx = ex     
                print("{}  {}。".format(datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"),lastEx))
                
            time.sleep(max(0.5,1-(time.time()-t1)))           
        
    def random_price_hand(self,tick): 
        '''
        读取random_price数据，并转换为实时tick
        '''
        t=time.time()   
        retry = 20
        for _ in range(retry):
            try:   
                tick_columns_=['close']
                i='close'
                stock_data_tick_real1={}
                tick.columns.name='code'
                stock_data_tick_real1['close']=tick
                try:  #判断是否存在某变量    第一次运行  
                    for i in tick_columns_:
                        pass
                        self.data[self.STOCK_CN+'_tick_real'][i]=pd.concat([self.data[self.STOCK_CN+'_tick_real'][i],stock_data_tick_real1[i]],axis=0)
                        #IsDuplicated =stock_data_realtime[i].duplicated()  #判断是否重复
                        #stock_data_realtime[i]= stock_data_realtime[i].drop_duplicates()    #去重复                 
                        delta = datetime.timedelta(minutes=2,seconds=datetime_.second)       #此处只选择近2min的tick 合成分钟数据时就不需要再做处理了         
                        self.data[self.STOCK_CN+'_tick_real'][i]=self.data[self.STOCK_CN+'_tick_real'][i].loc[slice(datetime_-delta, datetime_), :]
                except:
                    self.data[self.STOCK_CN+'_tick_real']={}     
                    for i in tick_columns_:    
                        pass
                        self.data[self.STOCK_CN+'_tick_real'][i]=stock_data_tick_real1[i].T.reset_index().drop_duplicates().set_index('code').T   
                break
            except Exception as ex:
                lastEx = ex 
                if len(self.user.subscribed_code[MARKET_TYPE.STOCK_CN])>0:
                    print("{}  错误：{}。".format(datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"),lastEx))
                else:
                    print("{}  订阅股票数为0，请增加订阅".format(datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")))
            time.sleep(1)       
  
    
if __name__=='__main__':
    self=qz_realtime_handle(model='test')      
    data=self.data      
    #self.run()
    codelist=QA.QA_fetch_stock_list().code.tolist()
    for i in codelist[:3]:
        self.subscribe(i)    

    #self.run_random_price_hand() #仿真数据
    #self.run() #实盘数据
    self.realtime_hand()      

