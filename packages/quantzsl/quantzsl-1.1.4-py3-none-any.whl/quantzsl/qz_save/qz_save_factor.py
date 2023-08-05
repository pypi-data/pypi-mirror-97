# -*- coding: utf-8 -*-
"""
Created on Mon Feb  1 23:46:34 2021

@author: ZSL
"""

import datetime
import time
import json
import pymongo
import pandas as pd
import numpy as np
import quantzsl as qz
from quantzsl.qz_fench.qz_tushare import (
                                            qz_fetch_get_stock_list_tushare,
                                            qz_fetch_get_stock_trade_cal_tushare,
                                            qz_fetch_get_stock_day_tushare,
                                            qz_fetch_get_stock_daily_basic_tushare,
                                            qz_fetch_get_index_list_tushare
                                        )
from quantzsl.qz_factor.qz_factor import (
                                            qz_cal_macd,
                                            qz_cal_ma,
                                            factor_inf 
                                        )

from quantzsl.qz_database.qz_mongo import (
                                                qz_mongo
                                            )
from quantzsl.qz_fench.qz_query import (
                                            qz_fetch_stock_list_tushare
                                           
                                        )
from QUANTAXIS.QAUtil import (
    DATABASE,
    QA_util_get_next_day,
    QA_util_get_real_date,
    QA_util_log_info,
    QA_util_to_json_from_pandas,
    trade_date_sse,
    QA_util_date_int2str,
    QA_util_get_trade_range,
    QA_util_date_stamp
)

client = qz_mongo().quantzsl

def now_time():
    return str(QA_util_get_real_date(str(datetime.date.today() - datetime.timedelta(days=1)), trade_date_sse, -1)) + \
           ' 17:00:00' if datetime.datetime.now().hour < 15 else str(QA_util_get_real_date(
        str(datetime.date.today()), trade_date_sse, -1)) + ' 15:00:00'

def qz_find_last_date(client2,para1='MA5'): 
    '''
    查询数据库中储存的最近日期
    client2为数据库连接
    para1为可选项，为某个指标的查询项
    '''
    stock_list_=qz_fetch_stock_list_tushare()
    code=stock_list_.code.to_list()[:10]
        #date_=client2.distinct(para1)
    #ref= client2.find({'code': {'$in': code}}, {"_id": 0,para1: 1,"date": 1}, batch_size=10000) 
    ref= client2.find( {},{"_id": 0,para1: 1,"date": 1}, batch_size=10000)     
    if ref.count()>0 :
        ls=[item for item in ref] 
        count=0
        ls.reverse()
        for i in ls:
            pass
            if len(i)==2 and count==0:
                retur=i['date']
                count+=1
                
        try: 
            return retur
        except:    
            return i['date']
    else:
        return '2000-01-01'
    
        # ls=ref[ref.count() - 1]['_id']
        # ref= client2.find( {"_id":ls},{"_id": 0,"date": 1}, batch_size=10000)            
        # return ref[ref.count() - 1]['date']    

def qz_save_factor_day(name='macd',ind='MACD'):
    pass  
    client2= client.stock_factor_day
    client2.create_index(
        [("code",
          pymongo.ASCENDING),
         ("date_stamp",
          pymongo.ASCENDING)]
    )
    err = []
    t0=time.time()
    end_date=str(now_time())[0:10]
    
    stock_list_=qz.qz_fetch_stock_list_tushare()  #将股票个数防砸这里，调取数据放在计算函数里
    code=stock_list_.code.to_list()[:2]   
     
    start_date_=qz_find_last_date(client2,para1=ind)                       
    start_date=QA_util_get_next_day(QA_util_get_real_date(start_date_),1) #返回下一个交易日              

    if  start_date>end_date: #start_date==end_date or
        t1=time.time() 
        print(
            '{} 日线指标{}无需更新，耗时：{}S'.format(
                    datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                    name,
            str(round(t1-t0,2))
            )
            )                 
    else:
        t=time.time()
        res=[]
        #res_1='res=qz_cal_'+name+'(code,start_date)'
        #exec(res_1)        
        #exec('res=qz_cal_'+name+'(code,start_date)')
        if name=='macd':
            res=qz_cal_macd(stock_list=code,fren='day',date=start_date)
        elif name=='ma'   :
            pass
            res=qz_cal_ma(stock_list=code,fren='day',date=start_date)
        for i in res.index:
            pass
            res_=QA_util_to_json_from_pandas(pd.DataFrame(res.iloc[i,:]).T)[0]
            client2.update(
                {'code':res_['code'] ,'date_stamp':res_['date_stamp']},
                    {'$set': res_},
                    upsert=True
                    )  
            
        t1=time.time()             
        print('{} 储存日线指标:{}完成,耗时{}S'.format(
            datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            name, 
            str(round(t1-t,2))
            )
            )  
        
def qz_save_factor_60min(name='macd',ind='MACD'):
    pass  
    client2= client.stock_factor_60min
    client2.create_index(
        [("code",
          pymongo.ASCENDING),
         ("date_stamp",
          pymongo.ASCENDING)]
    )
    err = []
    t0=time.time()
    end_date=str(now_time())[0:10]
    
    stock_list_=qz.qz_fetch_stock_list_tushare()  #将股票个数防砸这里，调取数据放在计算函数里
    code=stock_list_.code.to_list()[:2]   
     
    start_date_=qz_find_last_date(client2,para1=ind)                       
    start_date=QA_util_get_next_day(QA_util_get_real_date(start_date_),1) #返回下一个交易日              

    if  start_date>end_date: #start_date==end_date or
        t1=time.time() 
        print(
            '{} 60min指标{}无需更新，耗时：{}S'.format(
                    datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                    name,
            str(round(t1-t0,2))
            )
            )                 
    else:
        t=time.time()
        res=[]
        #res_1='res=qz_cal_'+name+'(code,start_date)'
        #exec(res_1)        
        #exec('res=qz_cal_'+name+'(code,start_date)')
        if name=='macd':
            res=qz_cal_macd(stock_list=code,fren='60min',date=start_date)
        elif name=='ma'   :
            pass
            res=qz_cal_ma(stock_list=code,fren='60min',date=start_date)
        for i in res.index:
            pass
            res_=QA_util_to_json_from_pandas(pd.DataFrame(res.iloc[i,:]).T)[0]
            client2.update(
                {'code':res_['code'] ,'date_stamp':res_['date_stamp']},
                    {'$set': res_},
                    upsert=True
                    )  
            
        t1=time.time()             
        print('{} 储存60min指标:{}完成,耗时{}S'.format(
            datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            name, 
            str(round(t1-t,2))
            )
            )         
        
def qz_save_factor():
    pass
    for i in factor_inf:
        pass
        qz_save_factor_day(name=i,ind=factor_inf[i][0])    
    for i in factor_inf:
        pass
        qz_save_factor_60min(name=i,ind=factor_inf[i][0])
        
    
if __name__=='__main__':
    pass
    qz_save_factor()