# -*- coding: utf-8 -*-
"""
Created on Sat Nov  7 23:30:07 2020

@author: ZSL
"""
import datetime
import time
import json
import pymongo
import pandas as pd
import numpy as np

from quantzsl.qz_fench.qz_eastmoney import (
                                            qz_fetch_get_block_eastmoney,
                                            qz_fetch_get_block_stock_eastmoney,
                                            qz_fetch_get_block_day_eastmoney
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
    QA_util_date_stamp
)

client = qz_mongo().quantzsl

def now_time():
    return str(QA_util_get_real_date(str(datetime.date.today() - datetime.timedelta(days=1)), trade_date_sse, -1)) + \
           ' 17:00:00' if datetime.datetime.now().hour < 15 else str(QA_util_get_real_date(
        str(datetime.date.today()), trade_date_sse, -1)) + ' 15:00:00'
                   
def qz_save_block_stock_eastmoney():
    '''
    板块包含的个股信息，因变动频率不高，每3天存一次即可
    '''
    coll_block = client.stock_block_eastmoney
    coll_block.create_index(
        [
         ("date_stamp",
          pymongo.ASCENDING)]
    )
    err = []
    block_list=['概念板块','地域板块','行业板块']
    def __saving_work(block_name='地域板块'):
        try:
            print(
                '{} 正在储存{}数据(eastmoney)'.format(
                        datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                 block_name)
            )        
    
            ref = coll_block.find({'fenlei':block_name})
            end_date = str(now_time())[0:10]
            
            if ref.count() > 0:

                # 接着上次获取的日期继续更新
                start_date = ref[ref.count() - 1]['date']
                
                timedelta=datetime.datetime.strptime(end_date, '%Y-%m-%d')-datetime.datetime.strptime(start_date, '%Y-%m-%d')
                if datetime.timedelta(3)<timedelta:
                    res=qz_fetch_get_block_stock_eastmoney(block_name)
                    res=res.assign(date=end_date)
                    res=res.assign(fenlei=block_name)
                    res=res.assign(date_stamp=res['date'].apply(
                                    lambda x: QA_util_date_stamp(str(x)[0:10])
                                    ))
                            
                   
                    coll_block.insert_many(
                       QA_util_to_json_from_pandas(res
                        )
                    )                    
                    print(
                        '{}  储存{}数据完成'
                        .format(
                                 datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                                 block_name)
                    )                
                else:
                    print(
                        '{} 间隔未到3天，{}数据无需储存'.format(
                                datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                                block_name
                         )
                    )                    
                
            else:
                res=qz_fetch_get_block_stock_eastmoney(block_name)
                res=res.assign(date=end_date)
                res=res.assign(fenlei=block_name)
                res=res.assign(date_stamp=res['date'].apply(
                                lambda x: QA_util_date_stamp(str(x)[0:10])
                                ))
                        
               
                coll_block.insert_many(
                   QA_util_to_json_from_pandas(res
                    )
                )                    
                print(
                    '{}  首次储存{}数据完成'
                    .format(
                             datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                             block_name)
                )                  

            # 当前数据库中没有这个代码的股票数据， 从1990-01-01 开始下载所有的数据

        except Exception as error0:
            print(error0)
            err.append(str(block_name))
    block_list=['概念板块','地域板块','行业板块']
    code_list=block_list
    t=time.time()
    for item in range(len(code_list)):
        pass
        print('{} The {} of Total {}, {}'.format(
                datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                item+1, 
                len(code_list),
                str(float((item+1) / len(code_list) * 100))[0:4] + '%'),
                )

        __saving_work(code_list[item])
    t1=time.time()
    if len(err) < 1:
        print('{} 成功更新全部板块数据 ^_^ 耗时：{}S'.format(
                datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                str(round(t1-t,2))
                )
            )
    else:
        print('{} 错误代码{}'.format(
                datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                str(err)
                ))


def qz_save_block_day_eastmoney():
    '''
    保存板块日线数据
    '''
    res=qz_fetch_get_block_eastmoney()
    aa=pd.concat([res['概念板块'],res['地域板块']],axis=0)
    aaa=pd.concat([aa,res['行业板块']],axis=0)
    code_list=aaa['code'].to_list()
    coll_block_day = client.stock_block_day_eastmoney
    coll_block_day.create_index(
        [("code",
          pymongo.ASCENDING),
         ("date_stamp",
          pymongo.ASCENDING)]
    )
    err = []

    def __saving_work(code='BK0713'):
        try:
            print(
                '{} 正在储存板块日线数据(eastmoney)==== {}'.format(
                        datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                 str(code))
            )

            # 首选查找数据库 是否 有 这个代码的数据
            ref = coll_block_day.find({'code': str(code)[0:6]})
            end_date = str(now_time())[0:10]

            # 当前数据库已经包含了这个代码的数据， 继续增量更新
            # 加入这个判断的原因是因为如果股票是刚上市的 数据库会没有数据 所以会有负索引问题出现
            if ref.count() > 0:

                # 接着上次获取的日期继续更新
                start_date = ref[ref.count() - 1]['date']

                print(
                    '{}  Trying updating {} from {} to {}'
                    .format(
                             datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                             code,
                            start_date,
                            end_date)
                )
                if start_date != end_date:
                    coll_block_day.insert_many(
                       QA_util_to_json_from_pandas(
                            qz_fetch_get_block_day_eastmoney(
                                    str(code),
                                    start_date,
                                    end_date
                                    )
                        )
                    )

            # 当前数据库中没有这个代码的股票数据， 从1990-01-01 开始下载所有的数据
            else:
                start_date = '2000-01-01'
                print(
                    '{} Trying updating {} from {} to {}'
                    .format(
                             datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                             code,
                            start_date,
                            end_date)
                )
                if start_date != end_date:
                    coll_block_day.insert_many(
                        QA_util_to_json_from_pandas(
                            qz_fetch_get_block_day_eastmoney(
                                    str(code),
                                    start_date,
                                    end_date
                                    )
                        )
                    )
        except Exception as error0:
            print(error0)
            err.append(str(code))
    t=time.time()
    for item in range(len(code_list)):
        pass
        print('{} The {} of Total {}, {}'.format(
                datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                item+1, 
                len(code_list),
                str(float((item+1) / len(code_list) * 100))[0:4] + '%'),
                )

        __saving_work(code_list[item])
    t1=time.time()
    if len(err) < 1:
        print('{} 成功更新全部板块日线数据 ^_^ 耗时：{}S'.format(
                datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                str(round(t1-t,2))
                )
            )
    else:
        print('{} 错误代码{}'.format(
                datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                str(err)
                ))
if __name__=='__main__':
    qz_save_block_day_eastmoney() 
    qz_save_block_stock_eastmoney()
