# -*- coding: utf-8 -*-
"""
Created on Thu Jan 21 22:34:51 2021

@author: ZSL
"""

import QUANTAXIS as QA
import quantzsl as qz
import tushare as ts
import numpy as np
import pandas as pd
#import talib
import time
import datetime
from QUANTAXIS.QAUtil.QAParameter import (DATASOURCE, FREQUENCE, MARKET_TYPE, OUTPUT_FORMAT)
import matplotlib.patches as mpatches
import matplotlib.pyplot as plt                                         
import matplotlib.ticker as ticker
#import matplotlib.finance as mpf
#from mpl_finance import candlestick_ochl
from matplotlib.pylab import date2num
from QUANTAXIS.QAData import (
    QA_DataStruct_Stock_day
)
from QUANTAXIS.QAUtil import (
                              QA_util_get_real_date,
                              QA_util_get_last_day,
                              QA_util_get_next_day,
                              QA_util_date_stamp,
                              QA_util_time_stamp
                              ) 

from quantzsl.qz_fench.qz_query import (
                                            qz_fetch_stock_list_tushare
                                           
                                        )
try:#当第一次用数据库中没有stock_list时 会出错 兼容一下
    ##获取股票列表
    stock_list_=qz_fetch_stock_list_tushare()
    stock_list_all=stock_list_.code.to_list()
    stock_list_kcb=stock_list_[stock_list_['market']=='科创板'].code.to_list()
    stock_list=sorted(list(set(stock_list_all).difference(set(stock_list_kcb))))[:10]
    ##获取日线数据
except:
    pass

def qz_cal_macd(stock_list,fren='day',date='2020-01-03'):
    '''
    计算macd因子
    
    Parameters
    ----------
    data : ds格式
        ds格式的日期数据
    date : str
        起始日期（不含）

    Returns
    -------
    df格式的结果

    '''
    if fren=='day':
        delta=40
        end=datetime.datetime.now().strftime("%Y-%m-%d")
        start=(datetime.datetime.strptime(date, "%Y-%m-%d") - datetime.timedelta(days=delta)).strftime("%Y-%m-%d")
        stock_data=qz.qz_fetch_stock_day_tushare(code=stock_list,start=start,end=end)
        data=QA_DataStruct_Stock_day(stock_data.set_index(['date', 'code'], drop=True)).to_qfq()  
    elif fren=='60min':
        delta=40/4*(7/5)
        end=datetime.datetime.now().strftime("%Y-%m-%d")
        start=(datetime.datetime.strptime(date, "%Y-%m-%d") - datetime.timedelta(days=delta)).strftime("%Y-%m-%d")
        data=QA.QA_fetch_stock_min_adv(code=stock_list,start=start,end=end,frequence='60min').to_qfq()
        aa=data.data
    def MACD_JCSC(dataframe, SHORT=12, LONG=26, M=9):
        """
        1.DIF向上突破DEA，买入信号参考。
        2.DIF向下跌破DEA，卖出信号参考。
        """
        CLOSE = dataframe.close
        DIFF = QA.EMA(CLOSE, SHORT) - QA.EMA(CLOSE, LONG)
        DEA = QA.EMA(DIFF, M)
        MACD = 2*(DIFF-DEA)
    
        CROSS_JC = QA.CROSS(DIFF, DEA)
        CROSS_SC = QA.CROSS(DEA, DIFF)
        CROSS_JC_STATUS = QA.CROSS_STATUS(DIFF, DEA)
        CROSS_SC_STATUS = QA.CROSS_STATUS(DEA, DIFF)        
        ZERO = 0
        return pd.DataFrame({'DIFF': DIFF, 
                             'DEA': DEA, 
                             'MACD': MACD, 
                             'MACD_JC': CROSS_JC, 
                             'MACD_SC': CROSS_SC, 
                             'MACD_JC_STATUS': CROSS_JC_STATUS, 
                             'MACD_SC_STATUS': CROSS_SC_STATUS,                             
                             })
    ind=data.add_func(MACD_JCSC).dropna().reset_index() #采用默认参数计算macd    
    if 'datetime' in ind.columns:
        ind['date']=ind.datetime
        ind = ind.assign(
                date_stamp=ind['date'].apply(
                    lambda x: QA_util_time_stamp(str(x))
                    )
                )    
    else:
        ind = ind.assign(
                date_stamp=ind['date'].apply(
                    lambda x: QA_util_date_stamp(str(x))
                    )
                )         
    return ind

def qz_cal_ma(stock_list,fren='day',date='2020-01-03'):
    '''
    计算均线因子 从3-60
    
    Parameters
    ----------
    data : ds格式
        ds格式的日期数据
    date : str
        起始日期（不含）

    Returns
    -------
    df格式的结果

    '''
    if fren=='day':
        delta=80  #每5天停2天
        end=datetime.datetime.now().strftime("%Y-%m-%d")
        start=(datetime.datetime.strptime(date, "%Y-%m-%d") - datetime.timedelta(days=delta)).strftime("%Y-%m-%d")
        stock_data=qz.qz_fetch_stock_day_tushare(code=stock_list,start=start,end=end)
        data=QA_DataStruct_Stock_day(stock_data.set_index(['date', 'code'], drop=True)).to_qfq()   
    elif fren=='60min':
        delta=80/4*(7/5)
        end=datetime.datetime.now().strftime("%Y-%m-%d")
        start=(datetime.datetime.strptime(date, "%Y-%m-%d") - datetime.timedelta(days=delta)).strftime("%Y-%m-%d")
        data=QA.QA_fetch_stock_min_adv(code=stock_list,start=start,end=end,frequence='60min').to_qfq()
        aa=data.data    

    aa=data.data
    ind =data.add_func(QA.QA_indicator_MA, 2,  3,  4,  5,  6,  7,  8,  9, 10, 
                       11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 
                       25, 26, 27, 28, 29, 30, 31, 32, 33, 34, 35, 36, 37, 38, 
                       39, 40, 41, 42, 43, 44, 45, 46, 47, 48, 49, 50, 51, 52, 
                       53, 54, 55, 56, 57, 58, 59,60).dropna().reset_index()      
    if 'datetime' in ind.columns:
        ind['date']=ind.datetime
        ind = ind.assign(
                date_stamp=ind['date'].apply(
                    lambda x: QA_util_time_stamp(str(x))
                    )
                )    
    else:
        ind = ind.assign(
                date_stamp=ind['date'].apply(
                    lambda x: QA_util_date_stamp(str(x))
                    )
                )    
    
    return ind
    
    
ma_=[]
for i in range(2,60):
    ma_.append('MA'+str(i))
macd_=['DIFF','DEA','MACD','MACD_JC','MACD_SC','MACD_JC_STATUS','MACD_SC_STATUS']   
    
factor_inf={
    "macd":macd_,
    'ma':ma_,
    }
factor_name=['macd','ma']
factor_ind=['MACD','MA5']