# -*- coding: utf-8 -*-
"""
Created on Thu Mar 21 11:05:01 2019

@author: Administrator
"""

import pandas as pd
import numpy as np
import datetime
import pymongo
import json
import QUANTZSL as QZ
import time


t=time.time()
client=QZ.QZ_cilent_mg()
client2=client.sm_account
cursor = client2.find(batch_size=10000)
if cursor.count()>0:    
    res = pd.DataFrame([item for item in cursor])
    res___=pd.DataFrame()
    for i in res['account_cookie']:
        pass
        res_=res[res['account_cookie']==i]
        mx=[]
        colu=[]
        for j in res_.chicangmingxi.values[0]:
            pass
            mx.append(j[1])
            colu.append(j[0])
               
        chicang1=pd.DataFrame(mx).T
        chicang0=pd.DataFrame(colu).T
        chicang=pd.concat([chicang0,chicang1],axis=0)
        
        mx=['持仓明细','如下']
        colu=['策略',i]
        for k in res_.zongming.values[0]:
            pass
            mx.append(k[1])
            colu.append(k[0])
            
            
        zongmingxi1=pd.DataFrame(mx).T
        zongmingxi0=pd.DataFrame(colu).T
        zongmingxi=pd.concat([zongmingxi0,zongmingxi1])
    
        res__=pd.concat([zongmingxi,chicang],axis=0)    
        res___=pd.concat([res___,res__],axis=0)
    
        
#    print(zongmingxi1.总盈亏.values[0])
#
#ma_and_macd=res[res['account_cookie']=='ma_and_macd']
#
#mx=[]
#colu=[]
#for i in ma_and_macd.chicangmingxi.values[0]:
#    pass
#    mx.append(i[1])
#    colu.append(i[0])
#    
#    
#chicang1=pd.DataFrame(mx).T
#chicang1.columns=colu
#
#mx=[]
#colu=[]
#for i in ma_and_macd.zongming.values[0]:
#    pass
#    mx.append(i[1])
#    colu.append(i[0])
#    
#    
#zongmingxi1=pd.DataFrame(mx).T
#zongmingxi1.columns=colu
#    
#print(zongmingxi1.总盈亏.values[0])
#
#
#ma_and_macd=res[res['account_cookie']=='ma_day_5min']
#mx=[]
#colu=[]
#for i in ma_and_macd.chicangmingxi.values[0]:
#    pass
#    mx.append(i[1])
#    colu.append(i[0])
#    
#    
#chicang1=pd.DataFrame(mx).T
#chicang1.columns=colu
#
#mx=[]
#colu=[]
#for i in ma_and_macd.zongming.values[0]:
#    pass
#    mx.append(i[1])
#    colu.append(i[0])
#    
#    
#zongmingxi2=pd.DataFrame(mx).T
#zongmingxi2.columns=colu
#    
#print(zongmingxi2.总盈亏.values[0])