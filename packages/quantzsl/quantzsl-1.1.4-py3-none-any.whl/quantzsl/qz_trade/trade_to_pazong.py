# -*- coding: utf-8 -*-
"""
Created on Wed Feb 10 11:08:02 2021

@author: ZSL
"""

import datetime
import pymongo
import pandas as pd
import numpy as np
import QUANTAXIS as QA
from QUANTAXIS.QAData import (
    QA_DataStruct_Stock_min
)
#mg = pymongo.MongoClient('mongodb://localhost:27017')
mg = pymongo.MongoClient('mgdb')
stock_list=QA.QA_fetch_stock_list().code.to_list()[:2]


delta=5
freq='15min'
end=datetime.datetime.now().strftime("%Y-%m-%d")
start=(datetime.date.today() - datetime.timedelta(days=delta)).strftime("%Y-%m-%d")
data_old=QA.QA_fetch_stock_min_adv(code=stock_list,start=start,end=end,frequence=freq)


def fetch_get_realtime_hexo(code=['000001'],type_='5min'):
    '''
    从数据库中读取hexo存储的数据
    '''
    code2=[QA.get_stock_market(str(x))+str(x) for x in code] #将6位代码转换为hexo存储的8位格式
    res=mg.qa.REALTIMEPRO_FIX.find(
        {'code': {'$in': code2},
         'frequence': type_},
        {"_id": 0},
        batch_size=10000)
    res=pd.DataFrame([i for i in res])
    res = res.assign(
            code2=res['code'].apply(
                lambda x: x[2:]
                )
            )
    res = res.loc[:,
                  [
                      'code2',
                      'open',
                      'high',
                      'low',
                      'close',
                      'volume',
                      'datetime',
                      'frequence'
                  ]]
    res['amount']=0
    res=res.rename(columns={"code2": "code", "frequence":"type" })
    return res

res=fetch_get_realtime_hexo(code=stock_list,type_=freq)
data_new=QA_DataStruct_Stock_min(res.set_index(['datetime', 'code'], drop=True))

data_new=data_old.__add__(data_new)
a1=data_new.data
