# -*- coding: utf-8 -*-
"""
Created on Tue Feb 16 15:01:59 2021

@author: ZSL
"""


import pandas as pd
import numpy as np 
import tushare as ts 
import QUANTAXIS as QA
import time
import datetime
import os
import glob
import datetime as dt
import threading
#import talib
import warnings

from QUANTAXIS.QAUtil import (
                              QA_util_get_real_date,
                              QA_util_get_last_day,
                              QA_util_get_next_day,
                              QA_util_format_date2str,
                              QA_util_random_with_topic,
                              ORDER_STATUS,
                              DATABASE,
                              trade_date_sse,
                              QA_util_get_trade_range
                              )

from QUANTAXIS.QAUtil.QARandom import QA_util_random_with_topic
from QUANTAXIS.QAUtil.QADate import (
                                     QA_util_datetime_to_strdate,
                                     QA_util_datetime_to_strdatetime,
                                     QA_util_pands_timestamp_to_date,
                                     QA_util_pands_timestamp_to_datetime,
                                     )
from QUANTAXIS.QAARP.QAAccount import QA_Account
warnings.filterwarnings("ignore")
from QUANTAXIS.QAUtil.QAParameter import (FREQUENCE, MARKET_TYPE,
                                          OUTPUT_FORMAT)
STOCK_CN=MARKET_TYPE.STOCK_CN
INDEX_CN=MARKET_TYPE.INDEX_CN
frequence_day_=[FREQUENCE.YEAR,FREQUENCE.MONTH,FREQUENCE.WEEK,FREQUENCE.DAY]
frequence_min_=[FREQUENCE.ONE_MIN,FREQUENCE.FIVE_MIN,FREQUENCE.FIFTEEN_MIN,
                FREQUENCE.THIRTY_MIN,FREQUENCE.SIXTY_MIN]

from quantzsl import stock_backtest_base

class stock_min_backtest_base(stock_backtest_base):
    '''
    分钟回测基类，支持股票、指数、etf的单标的和多标的
    设置此基类是因为某些小周期的全市场回测 比如1min，5min，由于设备内存原因 无法一次性读取回测区间内全部数据
    只能在回测期间不停从数据库读入某一段时间的数据，比如一次读入一天数据
    直接继承然后修改cal_signal函数即可，如有需要也可以修改on_bar函数
    '''
    def __init__(self):
        pass
            
    def run(self): 
        datelist=QA_util_get_trade_range(self.start, self.end)       
        data=self.data
        if data==None:
            self.load_data() 
        data=self.data    
        self.load_account()
        self.cal_signal()        
        AC=self.account
       
        index_=datelist
        date_=index_[0] #用来判断是否是第二天了  设置一个初始值
        
        for i in index_: #每一天循环
            pass
            self.frequence='5min'
            if self.frequence in frequence_day_:
                self.on_bar(i)
                AC.settle()                 
            if self.frequence in frequence_min_:
                data_new= QA.QA_quotation(self.code.upper(),
                                    i, 
                                    i, 
                                    source=QA.DATASOURCE.MONGO,
                                    frequence=self.frequence, 
                                    market=self.market_type, 
                                    output=QA.OUTPUT_FORMAT.DATASTRUCT)
                try:
                    self.data_new=data_new.to_qfq()
                except:
                    self.data_new=data_new
    
                self.data=self.data.__add__(self.data_new)
                self.data.data=self.data.data[250]  #取前250行 为了防止每天堆积数据 太多过卡
                data=self.data
                if i != date_: #第二天早上settle 也是一样的
                   AC.settle()
                   date_=i
                self.on_bar(i)
            if self.real_save: #实时保存回测结果
                try: #防止第一天没有交易的容错
                    AC.save()
                    #aa=AC.history_table
                    if self.frequence in frequence_day_:
                        #aa=AC.history_table
                        r = QA.QA_Risk(AC,if_fq=False,market_data=data.select_time(AC.start_date,AC.end_date).select_code(AC.code))
                        r.save() 
                        r.plot_assets_curve()               
                    if self.frequence in frequence_min_:
                        if self.market_type==STOCK_CN:
                            market_data=QA.QA_fetch_stock_day_adv(AC.code, AC.start_datee, AC.end_date)          
                        elif self.market_type==INDEX_CN:                
                            market_data=QA.QA_fetch_index_day_adv(AC.code, AC.start_datee, AC.end_date)
                        r = QA.QA_Risk(AC,if_fq=False,market_data=market_data)
                        r.save() 
                    self.risk=r
                except:
                    pass
        try: #防止第一天没有交易的容错
            AC.save()
            #aa=AC.history_table
            if self.frequence in frequence_day_:
                #aa=AC.history_table
                r = QA.QA_Risk(AC,if_fq=False,market_data=data.select_time(AC.start_date,AC.end_date).select_code(AC.code))
                r.save() 
                r.plot_assets_curve()               
            if self.frequence in frequence_min_:
                if self.market_type==STOCK_CN:
                    market_data=QA.QA_fetch_stock_day_adv(AC.code, AC.start_datee, AC.end_date)          
                elif self.market_type==INDEX_CN:                
                    market_data=QA.QA_fetch_index_day_adv(AC.code, AC.start_datee, AC.end_date)
                r = QA.QA_Risk(AC,if_fq=False,market_data=market_data)
                r.save() 
                r.plot_assets_curve()
            self.risk=r                
        except:
            pass 

if __name__=='__main__':
    #上证指数 000001
    #上证50  000016
    #中证500 399905
    #沪深300 000300
    #创业板  399006
    
    etf_list=QA.QA_fetch_index_list()
    etf_list[etf_list.name.str.contains('创业板')]
    list_etf=['50ETF','300ETF','500ETF','创业板','800ETF']    
    code='000005'#etf_list[etf_list.name=='50ETF'].code.tolist()[0]
    end_date=QA_util_get_real_date(dt.date.today().strftime("%Y-%m-%d"), towards=-1)
    start_date='2019-01-01'    
    self=stock_backtest_base(
                portfolio_cookie='etf_day_ma_double',
                account_cookie='test',#QA_util_random_with_topic('hs300_')    
                market_type=STOCK_CN,#INDEX_CN,
                code=code,
                start=start_date,
                end=end_date,
                para=[5,10]  
                )
    #self.run()    



#dir(self.account)
#dir(self.risk)
#amessage=self.account.message  #存入数据库部分
#ahistory_table=self.account.history_table#交易列表
#acash_table=self.account.cash_table #资金列表
#atrade_range=self.account.trade_range #交易日期列表
#atrade=self.account.trade # 交易切面表
#adaily_hold=self.account.daily_hold #持仓切面表
#adaily_cash=self.account.daily_cash #持仓切面表
#adaily_frozen=self.account.daily_frozen

