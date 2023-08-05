# -*- coding: utf-8 -*-
"""
Created on Wed Oct  7 17:54:13 2020

@author: ZSL
"""

import concurrent
from concurrent.futures import ProcessPoolExecutor, ThreadPoolExecutor

import datetime
import time
import json
import pymongo
import pandas as pd
import numpy as np

from quantzsl.qz_fench.qz_tushare import (
                                            qz_fetch_get_stock_list_tushare,
                                            qz_fetch_get_stock_trade_cal_tushare,
                                            qz_fetch_get_stock_day_tushare,
                                            qz_fetch_get_stock_daily_basic_tushare,
                                            qz_fetch_get_index_list_tushare
                                        )
from quantzsl.qz_database.qz_mongo import (
                                                qz_mongo
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

def qz_save_stock_list_tushare():
    '''
    储存股票列表到数据库monggo
    
    '''
    db=client.stock_list_tushare
    t=time.time()   
    stock_list=qz_fetch_get_stock_list_tushare()#.code.unique().tolist()
    db.create_index(
    [("code",
      pymongo.ASCENDING)]
        ) 
    
    try:
        client.drop_collection('stock_list_tushare')
    except Exception as e:        
        pass
    try:     
        json_data = json.loads(stock_list.reset_index().to_json(orient='records')) 
        db.insert_many(json_data)
    except Exception as e:        
        print(e)  
    t1=time.time()
    print('{} 储存股票列表完成,耗时{}S'.format(
                     datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                     str(round(t1-t,2))
                     )
                ) 

def qz_find_last_trade_date(table,para2=None): 
    '''
    查询数据库中最近的交易日期
    para1一般为'date'，即交易日期
    table为表名字：stock_day or stock_5min
    para2为可选项，一般为代码名称 '000001'
    '''
    #para1='date_stamp'
    #table='stock_daily_basic_tushare'
    #para2='600602'
    client2 = client[table]
    #exec("coll= client."+table)
    if para2==None:
        #date_=client2.distinct(para1)
        
            ref = client2.find({'code': '600601'},{"_id": 0,"date": 1})      #选x个股票进行验证 如果都停牌则gg       
            if ref.count()>0:
                start_date1 = str(ref[ref.count() - 1]['date'])
            else:
                start_date1=0
            ref = client2.find({'code': '601857'},{"_id": 0,"date": 1})            
            if ref.count()>0:
                start_date2 = str(ref[ref.count() - 1]['date'])
            else:
                start_date2=0  
            ref = client2.find({'code': '000001'},{"_id": 0,"date": 1})            
            if ref.count()>0:
                start_date3 = str(ref[ref.count() - 1]['date'])
            else:
                start_date3=0                
            start_date=max(str(start_date1),str(start_date2),str(start_date3))          
    else:
        #cursor=client2.find({'code': {'$in': para2}}).distinct(para1)
        #client2.distinct(para1,{'code': {'$in': para2}})          
        ref=client2.find({'code':  para2},{"_id": 0,"date": 1})
        if ref.count()>0:
            start_date = str(ref[ref.count() - 1]['date'])
        else:
            start_date=0              
    return start_date     

def qz_save_stock_day_tushare():
    '''
    保存股票日线数据到monggo
    '''
    stock_list=qz_fetch_get_stock_list_tushare('all').code.unique().tolist()
    coll_stock_day = client.stock_day_tushare
    coll_stock_day.create_index(
        [("code",
          pymongo.ASCENDING),
         ("date_stamp",
          pymongo.ASCENDING)]
    )
    err = []
    t0=time.time()
    end_date=datetime.datetime.now().strftime("%Y-%m-%d")
    try: 
        start_date_=qz_find_last_trade_date('stock_day_tushare')
        if start_date_=='0':
            start_date='1990-12-19'  #第一次下载  
        else:                              
            start_date=QA_util_get_next_day(QA_util_get_real_date(start_date_),1) #返回下一个交易日              
    except:        
        pass        
    if isinstance(start_date,int):  #兼容设置，防止输入为整数型  20001024
        start_date=QA_util_date_int2str(start_date)
    elif len(start_date)==8:
        start_date=start_date[0:4]+'-'+start_date[4:6]+'-'+start_date[6:8]

    if  start_date>end_date: #start_date==end_date or
        t1=time.time() 
        print(
            '{} 股票日线数据无需更新(tushare)，耗时：{}S'.format(
                    datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            str(round(t1-t0,2))
            )
            )                 
    else:
        trade_date=QA_util_get_trade_range(start_date,end_date) 
        trade_date2=list(set(trade_date))
        trade_date2.sort()  
        
        for item in range(len(trade_date2)):
            pass
            
            try:
                t=time.time()
                coll_stock_day.insert_many(
                       QA_util_to_json_from_pandas(
                            qz_fetch_get_stock_day_tushare(
                                    trade_date=trade_date2[item]
                                    )
                        )
                    )
                t1=time.time()             
                print('{} 储存股票日线数据:{},{}/{},{},耗时{}S'.format(
                    datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                    trade_date2[item],
                    item+1, 
                    len(trade_date2),
                    str(float((item+1) / len(trade_date2) * 100))[0:4] + '%',
                    str(round(t1-t,2))
                    )
                    )        
                
            except Exception as e:
                print(e)
                err.append(str(trade_date2[item]))
    

        t1=time.time()
        if len(err) < 1:
            print('{} 成功更新全部股票日线数据 ^_^ 耗时：{}S'.format(
                    datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                    str(round(t1-t0,2))
                    )
                )
        else:
            print('{} 错误日期{}'.format(
                    datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                    str(err)
                    ))  

def qz_save_stock_daily_basic_tushare():
    '''
    保存股票daily_basic数据到monggo
    '''
    stock_list=qz_fetch_get_stock_list_tushare('all').code.unique().tolist()
    coll_stock_day = client.stock_daily_basic_tushare
    coll_stock_day.create_index(
        [("code",
          pymongo.ASCENDING),
         ("date_stamp",
          pymongo.ASCENDING)]
    )
    err = []
    t0=time.time()
    end_date=datetime.datetime.now().strftime("%Y-%m-%d")
    try: 
        start_date_=qz_find_last_trade_date('stock_daily_basic_tushare')
        if start_date_=='0':
            start_date='1990-12-19'  #第一次下载  
        else:                              
            start_date=QA_util_get_next_day(QA_util_get_real_date(start_date_),1) #返回下一个交易日              
    except:        
        pass        
    if isinstance(start_date,int):  #兼容设置，防止输入为整数型  20001024
        start_date=QA_util_date_int2str(start_date)
    elif len(start_date)==8:
        start_date=start_date[0:4]+'-'+start_date[4:6]+'-'+start_date[6:8]

    if  start_date>end_date: #start_date==end_date or
        t1=time.time() 
        print(
            '{} 股票daily_basic数据无需更新(tushare)，耗时：{}S'.format(
                    datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            str(round(t1-t0,2))
            )
            )                 
    else:
        trade_date=QA_util_get_trade_range(start_date,end_date) 
        trade_date2=list(set(trade_date))
        trade_date2.sort()  
        
        for item in range(len(trade_date2)):
            pass
            
            try:
                t=time.time()
                coll_stock_day.insert_many(
                       QA_util_to_json_from_pandas(
                            qz_fetch_get_stock_daily_basic_tushare(
                                    trade_date=trade_date2[item]
                                    )
                        )
                    )
                t1=time.time()             
                print('{} 储存股票daily_basic数据:{},{}/{},{},耗时{}S'.format(
                    datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                    trade_date2[item],
                    item+1, 
                    len(trade_date2),
                    str(float((item+1) / len(trade_date2) * 100))[0:4] + '%',
                    str(round(t1-t,2))
                    )
                    )        
                
            except Exception as e:
                print(e)
                err.append(str(trade_date2[item]))
    

        t1=time.time()
        if len(err) < 1:
            print('{} 成功更新全部股票daily_basic数据 ^_^ 耗时：{}S'.format(
                    datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                    str(round(t1-t0,2))
                    )
                )
        else:
            print('{} 错误日期{}'.format(
                    datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                    str(err)
                    ))             
if __name__=='__main__':
    pass

#
#
#
#def qz_save_stock_day(client=DATABASE, ui_log=None, ui_progress=None):
#    '''
#     save stock_day
#    '''
#    stock_list = QA_fetch_get_stock_list().code.unique().tolist()
#    coll_stock_day = client.stock_day
#    coll_stock_day.create_index(
#        [("code",
#          pymongo.ASCENDING),
#         ("date_stamp",
#          pymongo.ASCENDING)]
#    )
#    err = []
#
#    def __saving_work(code, coll_stock_day):
#        try:
#            QA_util_log_info(
#                '##JOB01 Now Saving STOCK_DAY==== {}'.format(str(code)),
#                ui_log
#            )
#
#            # 首选查找数据库 是否 有 这个代码的数据
#            ref = coll_stock_day.find({'code': str(code)[0:6]})
#            end_date = str(now_time())[0:10]
#
#            # 当前数据库已经包含了这个代码的数据， 继续增量更新
#            # 加入这个判断的原因是因为如果股票是刚上市的 数据库会没有数据 所以会有负索引问题出现
#            if ref.count() > 0:
#
#                # 接着上次获取的日期继续更新
#                start_date = ref[ref.count() - 1]['date']
#
#                QA_util_log_info(
#                    'UPDATE_STOCK_DAY \n Trying updating {} from {} to {}'
#                    .format(code,
#                            start_date,
#                            end_date),
#                    ui_log
#                )
#                if start_date != end_date:
#                    coll_stock_day.insert_many(
#                        QA_util_to_json_from_pandas(
#                            QA_fetch_get_stock_day(
#                                str(code),
#                                QA_util_get_next_day(start_date),
#                                end_date,
#                                '00'
#                            )
#                        )
#                    )
#
#            # 当前数据库中没有这个代码的股票数据， 从1990-01-01 开始下载所有的数据
#            else:
#                start_date = '1990-01-01'
#                QA_util_log_info(
#                    'UPDATE_STOCK_DAY \n Trying updating {} from {} to {}'
#                    .format(code,
#                            start_date,
#                            end_date),
#                    ui_log
#                )
#                if start_date != end_date:
#                    coll_stock_day.insert_many(
#                        QA_util_to_json_from_pandas(
#                            QA_fetch_get_stock_day(
#                                str(code),
#                                start_date,
#                                end_date,
#                                '00'
#                            )
#                        )
#                    )
#        except Exception as error0:
#            print(error0)
#            err.append(str(code))
#
#    for item in range(len(stock_list)):
#        QA_util_log_info('The {} of Total {}'.format(item, len(stock_list)))
#
#        strProgressToLog = 'DOWNLOAD PROGRESS {} {}'.format(
#            str(float(item / len(stock_list) * 100))[0:4] + '%',
#            ui_log
#        )
#        intProgressToLog = int(float(item / len(stock_list) * 100))
#        QA_util_log_info(
#            strProgressToLog,
#            ui_log=ui_log,
#            ui_progress=ui_progress,
#            ui_progress_int_value=intProgressToLog
#        )
#
#        __saving_work(stock_list[item], coll_stock_day)
#
#    if len(err) < 1:
#        QA_util_log_info('SUCCESS save stock day ^_^', ui_log)
#    else:
#        QA_util_log_info('ERROR CODE \n ', ui_log)
#        QA_util_log_info(err, ui_log)