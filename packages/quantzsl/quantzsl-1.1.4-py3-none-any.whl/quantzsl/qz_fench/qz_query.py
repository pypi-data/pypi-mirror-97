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
from quantzsl.qz_database.qz_mongo import (
                                                qz_mongo
                                            )
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
client = qz_mongo().quantzsl

def qz_fetch_block_stock_day_eastmoney(
    code='BK0713',
    start='2020-01-01',
    end='2020-10-10',
    format='pd',
    frequence='day'
):
    """'获取板块日线'

    """
    if len(start)==8:
        start=start[:4]+'-'+start[4:6]+'-'+start[6:]
    #start=start.replace('-', '')
    if len(end)==8:
        end=end[:4]+'-'+end[4:6]+'-'+end[6:]
    #end=end.replace('-', '')    
    #code= [code] if isinstance(code,str) else code

    # code checking
    code = QA_util_code_tolist(code)
    collections = client.stock_block_day_eastmoney
    if QA_util_date_valid(end):

        cursor = collections.find(
            {
                'code': {
                    '$in': code
                },
                "date_stamp":
                    {
                        "$lte": QA_util_date_stamp(end),
                        "$gte": QA_util_date_stamp(start)
                    }
            },
            {"_id": 0},
            batch_size=10000
        )

        #res=[QA_util_dict_remove_key(data, '_id') for data in cursor]

        res = pd.DataFrame([item for item in cursor])
        try:
            res = res.assign(
                volume=res.vol,
                date=pd.to_datetime(res.date)
            ).drop_duplicates((['date',
                                'code'])).query('volume>1').set_index(
                                    'date',
                                    drop=False
                                )
            res = res.loc[:,
                          [
                              'code',
                              'name',
                              'open',
                              'high',
                              'low',
                              'close',
                              'volume',
                              'amount',
                              'date'
                              
                          ]]
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
                "Error  format parameter %s is none of  \"P, p, pandas, pd , json, dict , n, N, numpy, list, l, L, !\" "
                % format
            )
            return None
    else:
        print(
            ' Error data parameter start=%s end=%s is not right'
            % (start,
               end)
        )
def qz_fetch_block_stock_eastmoney(date='20201231',format='pd'):
    """'获取板块日线'

    """
    if len(date)==8:
        date=date[:4]+'-'+date[4:6]+'-'+date[6:]
    #date=date.replace('-', '')

    collections = client.stock_block_eastmoney
    if QA_util_date_valid(date):
        # cursor = collections.find(  #此种方法也可以
        #     {
        #         'date': {
        #             '$in': [date]
        #         }
        #     },
        #     {"_id": 0},
        #     batch_size=10000
        # )
        cursor = collections.find(
            {
                "date_stamp":
                    {
                        "$lte": QA_util_date_stamp(date),
                        "$gte": QA_util_date_stamp(date)
                    }
            },
            {"_id": 0},
            batch_size=10000
        )
        cursor.count()    
        #res=[QA_util_dict_remove_key(data, '_id') for data in cursor]

        res = pd.DataFrame([item for item in cursor])
        try:
            res = res.drop_duplicates().set_index(
                                    'date',
                                    drop=False
                                   
                                )
            res = res.loc[:,
                          [
                              'fenlei',
                              'block',
                              'block_code',
                              'name',
                              'code'
                          ]]
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
                "Error  format parameter %s is none of  \"P, p, pandas, pd , json, dict , n, N, numpy, list, l, L, !\" "
                % format
            )
            return None
    else:
        print(
            ' Error data parameter date=%s  is not right'
            % (date)
        )

def qz_fetch_stock_day_tushare(code=['000001','000002','000004','000005'],start='2019-01-01',end='2019-01-05',frequence='day',data='*',format='pd'):
    '''
    获取股票日线数据
    '''
    if frequence=='day':
        name_biao='stock_day_tushare'
    elif frequence=='5min':
        name_biao='stock_5min'
    t=time.time()
    client2=client[name_biao] 
#    cursor = client2.find({
#        'code': {'$in': code}, "date": {
#            "$lte": end,
#            "$gte": start}}, {"_id": 0}, batch_size=10000) 
#    dir(cursor) 
    t=time.time()
    if data=='*':       
        cursor = client2.find({
            'code': {'$in': code}, "date_stamp": {
                "$lte": QA_util_date_stamp(end),
                "$gte": QA_util_date_stamp(start)}}, {"_id": 0}, batch_size=10000)
    else:
        pass
        a_=''
        for i in data:
            a_=a_+",'{}':1 ".format(i)
        aa={'code': {'$in': code}, "date_stamp": {
                "$lte": QA_util_date_stamp(end),
                "$gte": QA_util_date_stamp(start)}}
        aaa='client2.find('+str(aa)+', {"_id": 0 '+ a_+'}, batch_size=10000)'
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
                 volume=res.vol,
                 date=pd.to_datetime(res.date)
             ).drop_duplicates((['date',
                                 'code'])).query('volume>1').set_index(
                                     'date',
                                     drop=False
                                 )
             res = res.loc[:,
                           [
                               'code',
                               'open',
                               'high',
                               'low',
                               'close',
                               'volume',
                               'amount',
                               'change',
                               'pct_chg',
                               'date'
                           ]]  
             
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

def qz_fetch_stock_daily_basic_tushare(code=['000001','000002','000004','000005'],start='2019-01-01',end='2019-01-05',data='*',format='pd'):
    '''
    获取股票日线级别基本面数据
    '''
    name_biao='stock_daily_basic_tushare'
    t=time.time()
    client2=client[name_biao] 
#    cursor = client2.find({
#        'code': {'$in': code}, "date": {
#            "$lte": end,
#            "$gte": start}}, {"_id": 0}, batch_size=10000) 
#    dir(cursor) 
    t=time.time()
    if data=='*':       
        cursor = client2.find({
            'code': {'$in': code}, "date_stamp": {
                "$lte": QA_util_date_stamp(end),
                "$gte": QA_util_date_stamp(start)}}, {"_id": 0}, batch_size=10000)
    else:
        pass
        a_=''
        for i in data:
            a_=a_+",'{}':1 ".format(i)
        aa={'code': {'$in': code}, "date_stamp": {
                "$lte": QA_util_date_stamp(end),
                "$gte": QA_util_date_stamp(start)}}
        aaa='client2.find('+str(aa)+', {"_id": 0 '+ a_+'}, batch_size=10000)'
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
                                     'date'
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
def qz_fetch_stock_list_tushare():
    #name='stocklist'
    name_biao='stock_list_tushare'
    t=time.time()
    client2=client[name_biao] 
    cursor = client2.find(batch_size=10000)
    res = pd.DataFrame([item for item in cursor])
    if len(res)==0:
        print('数据库没有股票列表数据，请检查数据库数据')
    else:
        #res.drop(["date_stamp"],axis=1, inplace=True)
        res=res.drop_duplicates().drop(['_id'],axis=1)                    
    return res 


if __name__=='__main__':
    date1=qz_fetch_block_stock_day_eastmoney(code='BK0713',start='2020-01-01',end='2020-10-10',format='pd')
    date2=qz_fench_block_eastmoney(date='20201231')
    date3=qz_fetch_stock_day_tushare()
    date4=qz_fetch_stock_list_tushare()

    