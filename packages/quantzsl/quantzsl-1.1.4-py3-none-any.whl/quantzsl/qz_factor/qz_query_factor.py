# -*- coding: utf-8 -*-
"""
Created on Sun Nov  8 19:01:42 2020

@author: ZSL
"""
import datetime
import time
import json
import pymongo
import pandas as pd
import numpy as np
import quantzsl as qz

from QUANTAXIS.QAUtil import (
    QA_util_get_next_day,
    QA_util_get_real_date,
    QA_util_log_info,
    trade_date_sse,
    QA_util_date_stamp,
    QA_util_code_tolist,
    QA_util_to_json_from_pandas,
     QA_util_date_valid
)
from quantzsl.qz_database.qz_mongo import (
                                                qz_mongo
                                            )
from quantzsl.qz_factor.qz_factor import (
                                            factor_inf 
                                        )

from quantzsl.qz_util.qz_date import (qz_util_get_next_day,
                                      qz_util_get_last_day)
client = qz_mongo().quantzsl

def qz_fetch_stock_factor_day(code=['000001','000002','000004','000005'],start='2019-01-01',end='2019-01-15',data='*',format='pd'):
    '''
    获取股票日线因子数据
    '''
    t=time.time()
    client2=client.stock_factor_day
    t=time.time()
    if data=='*':       
        cursor = client2.find({
            'code': {'$in': code}, "date_stamp": {
                "$lte": QA_util_date_stamp(end),
                "$gte": QA_util_date_stamp(start)}}, {"_id": 0,"date_stamp": 0}, batch_size=10000)
    else:
        data_=[]
        for i in data:
            pass
            data_=data_+factor_inf[i] 
        a_=''
        for i in data_:
            a_=a_+",'{}':1 ".format(i)
        aa={'code': {'$in': code}, "date_stamp": {
                "$lte": QA_util_date_stamp(end),
                "$gte": QA_util_date_stamp(start)}}
        aaa='client2.find('+str(aa)+', {"_id": 0 ,"date_stamp": 0'+ a_+'}, batch_size=10000)'
        cursor=eval(aaa)
        #cursor=eval(aaa)
#        data=['open','close','low']
#        para_= '{"_id": 0'
#        for i in data:
#            pass
#            para_=para_+", '"+i+"': 1"
#        para_=para_+'}'
#        list(para_)                
#        cursor = client2.find({
#            'code': {'$in': code}, "date_stamp": {
#                "$lte": QA.QAUtil.QADate.QA_util_date_stamp(end),
#                "$gte": QA.QAUtil.QADate.QA_util_date_stamp(start)}}, para_, batch_size=10000)        
    #cursor.count()
    res = pd.DataFrame([item for item in cursor])
    if len(res)==0:
        print('数据库没有符合条件数据，请检查查询条件或数据库数据')
    else:
         try:            
             res=res.drop_duplicates() 
             res = res.assign(
                 date=pd.to_datetime(res.date)
             ).drop_duplicates((['date',
                                 'code'])).set_index(
                                     'date',
                                     drop=False
                                 )
             
         except:
             res = None
         if format in ['P', 'p', 'pandas', 'pd']:
             return res
         elif format in ['json', 'dict']:
             return QA_util_to_json_from_pandas(res)
         # 多种数据格式
         elif format in ['n', 'N', 'numpy']:
             return np.asarray(res)
         elif format in ['list', 'l', 'L']:
             return np.asarray(res).tolist()
         else:
             print(
                 "QZ Error qz_fetch_stock_day format parameter %s is none of  \"P, p, pandas, pd , json, dict , n, N, numpy, list, l, L, !\" "
                 % format
             )
             return None            
    return res     
def qz_fetch_stock_factor_min(code=['000001','000002','000004','000005'],start='2019-01-01',end='2019-01-15',frequence='60min',data='*',format='pd'):
    '''
    获取股票60min因子数据
    '''
    t=time.time()
    client2=client.stock_factor_60min
    t=time.time()
    end=qz_util_get_next_day(end)
    if data=='*':       
        cursor = client2.find({
            'code': {'$in': code}, "date_stamp": {
                "$lte": QA_util_date_stamp(end),
                "$gte": QA_util_date_stamp(start)}}, {"_id": 0,"date_stamp": 0}, batch_size=10000)
    else:
        data_=[]
        for i in data:
            pass
            data_=data_+factor_inf[i] 
        a_=''
        for i in data_:
            a_=a_+",'{}':1 ".format(i)
        aa={'code': {'$in': code}, "date_stamp": {
                "$lte": QA_util_date_stamp(end),
                "$gte": QA_util_date_stamp(start)}}
        aaa='client2.find('+str(aa)+', {"_id": 0 ,"date_stamp": 0'+ a_+'}, batch_size=10000)'
        cursor=eval(aaa)
        #cursor=eval(aaa)
#        data=['open','close','low']
#        para_= '{"_id": 0'
#        for i in data:
#            pass
#            para_=para_+", '"+i+"': 1"
#        para_=para_+'}'
#        list(para_)                
#        cursor = client2.find({
#            'code': {'$in': code}, "date_stamp": {
#                "$lte": QA.QAUtil.QADate.QA_util_date_stamp(end),
#                "$gte": QA.QAUtil.QADate.QA_util_date_stamp(start)}}, para_, batch_size=10000)        
    #cursor.count()
    res = pd.DataFrame([item for item in cursor])
    if len(res)==0:
        print('数据库没有符合条件数据，请检查查询条件或数据库数据')
    else:
         try:            
             res=res.drop_duplicates() 
             res = res.assign(
                 date=pd.to_datetime(res.date)
             ).drop_duplicates((['date',
                                 'code'])).set_index(
                                     'date',
                                     drop=False
                                 )
             
         except:
             res = None
         if format in ['P', 'p', 'pandas', 'pd']:
             return res
         elif format in ['json', 'dict']:
             return QA_util_to_json_from_pandas(res)
         # 多种数据格式
         elif format in ['n', 'N', 'numpy']:
             return np.asarray(res)
         elif format in ['list', 'l', 'L']:
             return np.asarray(res).tolist()
         else:
             print(
                 "QZ Error qz_fetch_stock_day format parameter %s is none of  \"P, p, pandas, pd , json, dict , n, N, numpy, list, l, L, !\" "
                 % format
             )
             return None            
    return res     


if __name__=='__main__':
    date1=qz_fetch_stock_factor_day()
    date2=qz_fetch_stock_factor_min()
    