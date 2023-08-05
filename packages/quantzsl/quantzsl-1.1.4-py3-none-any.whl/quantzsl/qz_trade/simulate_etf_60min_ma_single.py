# -*- coding: utf-8 -*-
"""
Created on Mon Feb 17 14:10:18 2020

@author: ZSL
"""

import pandas as pd
import numpy as np 
import tushare as ts 
import QUANTAXIS as QA
import quantzsl as qz
import time
import os
import glob
import datetime as dt
import threading
import talib
import warnings
from QUANTAXIS.QAUtil.QADate_trade import (QA_util_get_real_date,QA_util_get_last_day,
                                          QA_util_get_next_day,QA_util_format_date2str)
from QUANTAXIS.QAUtil.QARandom import QA_util_random_with_topic
from QUANTAXIS.QAUtil.QADate import (QA_util_datetime_to_strdate,QA_util_pands_timestamp_to_date,
                                    QA_util_pands_timestamp_to_datetime,QA_util_datetime_to_strdatetime)
from QUANTAXIS.QAUtil.QADate_trade import (QA_util_if_tradetime,QA_util_if_trade)
from QUANTAXIS.QAUtil import DATABASE
from QUANTAXIS.QAARP.QAAccount import QA_Account
warnings.filterwarnings("ignore")
STOCK_CN=QA.QAUtil.QAParameter.MARKET_TYPE.STOCK_CN
INDEX_CN=QA.QAUtil.QAParameter.MARKET_TYPE.INDEX_CN
frequence_day_=[QA.FREQUENCE.YEAR,QA.FREQUENCE.MONTH,QA.FREQUENCE.WEEK,QA.FREQUENCE.DAY]
frequence_min_=[QA.FREQUENCE.ONE_MIN,QA.FREQUENCE.FIVE_MIN,QA.FREQUENCE.FIFTEEN_MIN,
                QA.FREQUENCE.THIRTY_MIN,QA.FREQUENCE.SIXTY_MIN]

from QUANTAXIS.QAIndicator.base import *

        
class simple_simulate_eft_api():
    def __init__(self,
                portfolio_cookie='simulate',
                account_cookie='default',
                code=['000001'],
                start='2018-01-01',
                end='2019-01-01', 
                data=None,
                frequence=QA.FREQUENCE.DAY,
                market_type=QA.QAUtil.QAParameter.MARKET_TYPE.STOCK_CN,
                max_hold=1,
                para=[5,20,30],
                model='backtest'         
                ):
        pass
        self.portfolio_cookie=portfolio_cookie
        self.account_cookie=account_cookie
        self.data=data
        self.broker=QA.QA_BacktestBroker()
        self.max_hold=max_hold
        self.para=para
        self.frequence=frequence
        self.code=code
        self.start_date=start
        self.end_date=end
        self.model=model
        self.signal_收盘=1
        self.buy={}
        self.sell={}
    def cal_signal(self):
        data=self.data
        para=self.para


        def cal_signal_buy(DataFrame,*args,**kwargs):
            #DataFrame=data.select_code(i).data
            CLOSE = DataFrame['close']
            ma=MA(CLOSE, para[0])
            ind=QA.CROSS(CLOSE,ma)
            buy=ma[ind==1]
            return buy   
        def cal_signal_sell(DataFrame,*args,**kwargs):
            #DataFrame=data.select_code(i).data
            CLOSE = DataFrame['close']
            ma=MA(CLOSE, para[0])
            ind=QA.CROSS(ma,CLOSE)
            sell=ma[ind==1]
            return sell 
        buy= data.add_func(cal_signal_buy).reset_index()
        sell= data.add_func(cal_signal_sell).reset_index()       

        if self.frequence in frequence_day_:
            buy=buy[['date','code']]
            sell=sell[['date','code']]
        if self.frequence in frequence_min_:
            buy=buy[['datetime','code']]
            sell=sell[['datetime','code']]
        data.code.to_list()
        self.buy=buy
        self.sell=sell
        
    def on_bar(self):  #单周期 onbar模板（单股票、多股票）
        buy=self.buy
        sell=self.sell
        data=self.data  
        
        
        index_last_all=self.data.data.index.levels[0][-1]        
        index_last_buy=buy['datetime'].tolist()[-1]        
        index_last_sell=sell['datetime'].tolist()[-1]
        

        if index_last_buy==index_last_all:
            code_to_buy=buy[buy['datetime']==index_last_buy].code.tolist()
            
            title ='下单提醒，策略:{}'.format(self.account_cookie) #消息标题，最长为256，必填。
            #消息内容，最长64Kb，可空，支持MarkDown。
            content = "下单提醒，策略:{}:{}买入{}".format(
                                        self.account_cookie,
                                        index_last_buy,
                                        code_to_buy
                                        )
            data_ = {"title":title,"text":content}
            data = {"msgtype": "markdown","markdown": data_}    
            qz.qz_send_dingding(data)
        
        if index_last_sell==index_last_all:
            code_to_sell=sell[sell['datetime']==index_last_sell].code.tolist()
            
            title ='下单提醒，策略:{}'.format(self.account_cookie) #消息标题，最长为256，必填。
            #消息内容，最长64Kb，可空，支持MarkDown。
            content = "下单提醒，策略:{}:{}买入{}".format(
                                        self.account_cookie,
                                        index_last_sell,
                                        code_to_sell
                                        )
            data_ = {"title":title,"text":content}
            data = {"msgtype": "markdown","markdown": data_}    
            qz.qz_send_dingding(data)


        
    def up_data(self):
        code=self.code
        #code='159915'
        self.end_date=QA_util_get_real_date(dt.date.today().strftime("%Y-%m-%d"), towards=-1)
        self.start_date=QA_util_get_last_day(self.end_date,30) #得到上一个(n)交易日        
        @QA.QDS_StockMinWarpper
        def data_():
            res=pd.DataFrame()
            for i in code:
                res_=QA.QAFetch.QATdx.QA_fetch_get_index_min(i,self.start_date,self.end_date,self.frequence)
                res=pd.concat([res,res_],axis=0)
            return res       
        self.data=data_() 
    def hold(self):
        buy=self.buy
        sell=self.sell        
        if int(dt.datetime.now().strftime("%H%M"))==1500 and self.signal_hold==1:
            try:    
                res=[]
                for i in self.code:
                    pass
                    if sell[sell['code']==i]['datetime'].tolist()[-1]<buy[buy['code']==i]['datetime'].tolist()[-1]:
                        res.append('持仓')
                    else:
                        res.append('空仓')                        
                title ='持仓，策略:{}'.format(self.account_cookie) #消息标题，最长为256，必填。
                #消息内容，最长64Kb，可空，支持MarkDown。
                content = "{}持仓情况分别为{}".format(self.code,res)
                data_ = {"title":title,"text":content}
                data = {"msgtype": "markdown","markdown": data_}    
                qz.qz_send_dingding(data)
                self.signal_hold=self.signal_hold-1  
            except:
                pass                 
    def run_(self):
        self.up_data() #更新数据
        self.simulate_settle()

        time_list=[1024,1124,1354,1454]

        print(dt.datetime.now().strftime("%Y-%m-%d %H:%M:%S")+'程序开始运行：'+self.account_cookie)        
        while True:
            time.sleep(60)             
            self.signal_open_close('open')
            if self.is_trade_time():
                #print(dt.datetime.now().strftime("%H%M"))
                if int(dt.datetime.now().strftime("%H%M")) in time_list:                    
                    print(dt.datetime.now().strftime("%Y-%m-%d %H:%M:%S")+'程序运行中')                    
                    self.up_data()
                    self.cal_signal()   
                    data=self.data 
                    self.on_bar()
            else:
                pass
                #print(dt.datetime.now().strftime("%H:%M")+'非交易时间') 
            self.signal_open_close('close')
            self.hold()
            
    def run(self):            
        tt=QA_util_random_with_topic('simulate' )
        tt=threading.Thread(target=self.run_)
        tt.start()
                                    
    def is_trade_time(self):
        _time=dt.datetime.now()
        _time = dt.datetime.strptime(str(_time)[0:19], '%Y-%m-%d %H:%M:%S')
        if QA_util_if_trade(str(_time.date())[0:10]):
            if _time.hour in [10, 13, 14]:
                return True
            elif _time.hour in [
                    9
            ] and _time.minute >= 15:  # 修改成9:15 加入 9:15-9:30的盘前竞价时间
                return True
            elif _time.hour in [11] and _time.minute <= 30:
                return True
            else:
                return False
        else:
            return False
        
    def signal_open_close(self,aa):
        if aa=='open':
            if int(dt.datetime.now().strftime("%H%M"))==930 and self.signal_开盘==1:
                try:               
                    title ='开盘提醒，策略:{}'.format(self.account_cookie) #消息标题，最长为256，必填。
                    #消息内容，最长64Kb，可空，支持MarkDown。
                    content = "开盘啦"
                    data_ = {"title":title,"text":content}
                    data = {"msgtype": "markdown","markdown": data_}    
                    qz.qz_send_dingding(data)
                    self.signal_开盘=self.signal_开盘-1  
                    print(dt.datetime.now().strftime("%Y-%m-%d %H:%M:%S")+'开盘啦')
                except:
                    pass 
        elif aa=='close':
            if int(dt.datetime.now().strftime("%H%M"))==1500 and self.signal_收盘==1:
                try: 
                    title ='收盘提醒，策略:{}'.format(self.account_cookie) #消息标题，最长为256，必填。
                    #消息内容，最长64Kb，可空，支持MarkDown。
                    content = "收盘啦"
                    data_ = {"title":title,"text":content}
                    data = {"msgtype": "markdown","markdown": data_}    
                    qz.qz_send_dingding(data)  
                    print(dt.datetime.now().strftime("%Y-%m-%d %H:%M:%S")+'收盘啦')
                    self.signal_收盘=self.signal_收盘-1
                except:
                    pass#
               
        if int(dt.datetime.now().strftime("%H%M"))==1600: 
            self.simulate_settle()
            
    def simulate_settle(self):
        self.signal_onbar_1=1
        self.signal_onbar_2=1
        self.signal_onbar_3=1        
        self.signal_开盘=1
        self.signal_收盘=1
        self.signal_hold=1
    

if __name__=='__main__':
    #上证指数 000001
    #上证50  000016
    #中证500 399905
    #沪深300 000300
    #创业板  399006

    etf_list=QA.QA_fetch_etf_list()
    etf_list[etf_list.name.str.contains('创业板')]
    list_etf=['50ETF','300ETF','500ETF','创业板','800ETF']
    #code=etf_list[etf_list.name.isin(list_etf)].code.tolist()[0] 
    name='ETF'#etf_list[etf_list.name==aa].name.tolist()[0]
    list_etf_code=['510050','510300','510500','159915','515800']

    #end_date=QA_util_get_real_date(dt.date.today().strftime("%Y-%m-%d"), towards=-1)
    #start_date='2016-01-01'#QA_util_get_last_day(end_date,700) #得到上一个(n)交易日
    #data = QA.QA_fetch_index_min_adv(code, start_date, end_date,frequence='60min')#.to_qfq()
    self=simple_simulate_eft_api(
                portfolio_cookie='etf_sim_60min_ma_single',
                account_cookie=name+'_'+'60min_ma_single',#QA_util_random_with_topic('hs300_')    
                market_type=QA.QAUtil.QAParameter.MARKET_TYPE.INDEX_CN,
                frequence=QA.FREQUENCE.SIXTY_MIN,
                code=list_etf_code,
                model='simulate',
                #start=start_date,
                #end=end_date,
                #data=data,
                para=[5]  
                )
    self.run()
#            portfolio_cookie='etf_60min_ema_single'
#            user_cookie=QA.QA_User(username='quantaxis', password='quantaxis').user_cookie
#            DATABASE.portfolio.delete_many({
#                                          'user_cookie':user_cookie,
#                                         
#                                          'portfolio_cookie':portfolio_cookie,
#                                          })
#            DATABASE.account.delete_many({
#                                          'user_cookie':user_cookie,
#                                         
#                                          'portfolio_cookie':portfolio_cookie,
#                                          })
#            DATABASE.risk.delete_many({
#                                            'user_cookie':user_cookie,                                      
#                                          'portfolio_cookie':portfolio_cookie,
#                                      })
#    
#            re=DATABASE.account.find({
#                                            'user_cookie':user_cookie,                                         
#                                          'portfolio_cookie':portfolio_cookie,
#                                              })
#            aa=pd.DataFrame([i for i in re]) 

#AC.start_='2020-01-01'       
#AC.end_=QA_util_format_date2str(data.data.index.levels[0][-1])   
#r = QA.QA_Risk(AC,if_fq=False,market_data=data.select_time(AC.start_date,AC.end_date).select_code(AC.code))
#r.plot_assets_curve()
#
#        
#
#        
#
#list_1=list(np.arange(1)+5)

