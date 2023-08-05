# -*- coding: utf-8 -*-
"""
Created on Fri Feb 12 15:42:22 2021

@author: ZSL
"""

import pandas as pd
import numpy as np 
import tushare as ts 
import QUANTAXIS as QA
import quantzsl as qz
import time
import json
import pymongo
import os
import glob
import datetime
import threading
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
from QUANTAXIS.QAUtil.QAParameter import (FREQUENCE, MARKET_TYPE,
                                          OUTPUT_FORMAT)
STOCK_CN=MARKET_TYPE.STOCK_CN
INDEX_CN=MARKET_TYPE.INDEX_CN
frequence_day_=[FREQUENCE.YEAR,FREQUENCE.MONTH,FREQUENCE.WEEK,FREQUENCE.DAY]
frequence_min_=[FREQUENCE.ONE_MIN,FREQUENCE.FIVE_MIN,FREQUENCE.FIFTEEN_MIN,
                FREQUENCE.THIRTY_MIN,FREQUENCE.SIXTY_MIN]
from QUANTAXIS.QAData import (
                                QA_DataStruct_Stock_min,
                                QA_DataStruct_Stock_day,
                                    QA_DataStruct_Index_day,
                                    QA_DataStruct_Index_min,
                                )
from QUANTAXIS.QAData.data_resample import (
    QA_data_day_resample,#day  to  week
    QA_data_min_to_day,#min to day
    QA_data_min_resample,#min to min
)
from QUANTAXIS.QAIndicator.base import *
import tushare as ts
from quantzsl.qz_util.qz_util import (qz_util_change_len,
                                      )
from quantzsl.qz_trade.stock_trade_base import (stock_trade_base
                                      )
import puppet


class etf_macd_60min(stock_trade_base):
    pass
    def cal_signal(self):
        data=self.data
        para=self.para
        frequence=self.frequence
        def MACD_JCSC(dataframe, SHORT=para[0], LONG=para[1], M=para[2]):
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
            ZERO = 0
            return pd.DataFrame({'DIFF': DIFF, 'DEA': DEA, 'MACD': MACD, 'CROSS_JC': CROSS_JC, 'CROSS_SC': CROSS_SC, 'ZERO': ZERO})



        
        ind_macd = data.add_func(MACD_JCSC)
        buy=ind_macd[ind_macd['CROSS_JC']==1].reset_index()
        #buy.date=buy.date.apply(lambda x :pd.to_datetime(QA_util_get_next_day(x, 1))) #将交易日期错后一天 既第二天开盘价买入
        sell=ind_macd[ind_macd['CROSS_SC']==1].reset_index() 
        #sell.date=buy.date.apply(lambda x :pd.to_datetime(QA_util_get_next_day(x, 1))) #将交易           
        #sell=ind[QA.CROSS(ind[ind.columns[0]], data.data.close)==1].reset_index()
        #buy=pd.merge(buy_mavol,buy_macd,on=['date','code']) #买入取交集
        #sell=pd.merge(sell_mavol,sell_macd,on=['date','code'], how='outer')  #卖出取并集
        if self.frequence in frequence_day_:
            buy=buy[['date','code']]
            sell=sell[['date','code']]
        if self.frequence in frequence_min_:
            buy=buy[['datetime','code']]
            sell=sell[['datetime','code']]
        
        self.buy=buy
        self.sell=sell 
        
    def select_code(self):
        pass
    def load_account(self):
        '''
        盘前进行账号确认
        '''
        self.account = puppet.Account(title='')  
    def on_bar(self):
        self.cal_signal()
        i=self.data.data.index.levels[0][-1] 
        buy=self.buy
        sell=self.sell
        max_hold=self.max_hold
        acc=self.account
        data=self.data
        #print(i)        
        if self.frequence in frequence_day_:
            date_='date'
            str_i=QA_util_datetime_to_strdate(QA_util_pands_timestamp_to_date(i))
        if self.frequence in frequence_min_:
            date_='datetime'
            str_i=QA_util_datetime_to_strdatetime(QA_util_pands_timestamp_to_datetime(i))
        position=acc.query('position')   
        for code in buy[buy[date_]==i][:max_hold].code:
            pass
            try:
                price=round(data.select_day(str_i).select_code(code).close.values[0],2)
                oder2=acc.buy('000001', price+0.02, 200)
                aa=oder['puppet'][0]
                
            except Exception as ex:
                lastEx = ex     
                print("{}  {}。".format(datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"),lastEx))                        
        
        for code in sell[sell[date_]==i].code:
            pass        
            if AC.sell_available.get(code, 0) > 0:
                try :
                    price=round(data.select_day(str_i).select_code(code).open.values[0],2)
                    order = AC.send_order(
                            code=code, time=str_i, amount=AC.sell_available.get(code, 0), 
                            towards=QA.ORDER_DIRECTION.SELL, price=price, 
                            order_model=QA.ORDER_MODEL.LIMIT, #市价单 成交价为bar的最高价和最低价平均
                            amount_model=QA.AMOUNT_MODEL.BY_AMOUNT
                        )
                    if order:
                        Broker.market_data=data.select_day(str_i).select_code(code).data
                        order = Broker.warp(order)
                        order.trade('unknownTrade', order.price,order.amount, order.datetime) 
                except Exception as ex:
                    lastEx = ex     
                    print("{}  {}。".format(datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"),lastEx)) 
        self.account=AC
        
        hold=self.hold
        i=pd.to_datetime(datetime.datetime.now().strftime("%Y-%m-%d"))
        hold=hold[hold['date']==i]
        if len(hold)>0:
            max_hold=self.max_hold
            AC=self.account
            data=self.data
            #print(i)        
            if self.frequence in frequence_day_:
                date_='date'
                str_i=QA_util_datetime_to_strdate(QA_util_pands_timestamp_to_date(i))
            if self.frequence in frequence_min_:
                date_='datetime'
                str_i=QA_util_datetime_to_strdatetime(QA_util_pands_timestamp_to_datetime(i))
                
            # if i in buy[date_].tolist():
            #     pass
            if i in hold[date_].to_list():
                pass
                code_to_hold=hold[hold[date_]==i].code.to_list()
                #现卖后买 卖掉不在列表里的
                position=acc.query('position') 
                code_hold_now=AC.query('position') 
                AC.buy('000001',20.68,200)
                hold.index.to_list()
                #union(并), intersection(交), difference(差)
                code_to_sell=list(set(code_hold_now).difference(set(code_to_hold)))
                if len(code_to_sell)>0:
                    pass
                    for code in code_to_sell:
                        if AC.sell_available.get(code, 0) > 0:
                            try :
                                price=round(data.select_day(str_i).select_code(code).open.values[0],2)
                                order = AC.send_order(
                                        code=code, time=str_i, amount=AC.sell_available.get(code, 0), 
                                        towards=QA.ORDER_DIRECTION.SELL, price=price, 
                                        order_model=QA.ORDER_MODEL.LIMIT, #市价单 成交价为bar的最高价和最低价平均
                                        amount_model=QA.AMOUNT_MODEL.BY_AMOUNT
                                    )
                                if order:
                                    Broker.market_data=data.select_day(str_i).select_code(code).data
                                    order = Broker.warp(order)
                                    order.trade('unknownTrade', order.price,order.amount, order.datetime) 
                            except Exception as ex:
                                lastEx = ex     
                                print("{}  {}。".format(datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"),lastEx)) 
                                
                code_to_buy=list(set(code_to_hold).difference(set(code_hold_now))) 
                for code in code_to_buy:
                    try:
                        max_to_hold=max_hold-len(AC.hold)
                        acount_to_buy=min(len(code_to_buy),max_to_hold)
                        if acount_to_buy > 0:
                            price=round(data.select_day(str_i).select_code(code).close.values[0],2)
                
                            order = AC.send_order(
                                    code=code, time=str_i, money=AC.latest_cash*0.98/acount_to_buy, 
                                    towards=QA.ORDER_DIRECTION.BUY, price=price, 
                                    order_model=QA.ORDER_MODEL.LIMIT, #限价单 按照委托价成交
                                    amount_model=QA.AMOUNT_MODEL.BY_MONEY
                                )
                            if order:
                                Broker.market_data=data.select_day(str_i).select_code(code).data
                                order = Broker.warp(order)
                                order.trade('unknownTrade', order.price,order.amount, order.datetime)
                    except Exception as ex:
                        lastEx = ex     
                        print("{}  {}。".format(datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"),lastEx))                
                
        else:
            #卖掉所有持仓
            try:                
                code_hold_now=AC.hold.index.to_list()
            except:
                code_hold_now=[]
            #union(并), intersection(交), difference(差)
            code_to_sell=code_hold_now
            if len(code_to_sell)>0:
                pass
                for code in code_to_sell:
                    if AC.sell_available.get(code, 0) > 0:
                        try :
                            price=round(data.select_day(str_i).select_code(code).open.values[0],2)
                            order = AC.send_order(
                                    code=code, time=str_i, amount=AC.sell_available.get(code, 0), 
                                    towards=QA.ORDER_DIRECTION.SELL, price=price, 
                                    order_model=QA.ORDER_MODEL.LIMIT, #市价单 成交价为bar的最高价和最低价平均
                                    amount_model=QA.AMOUNT_MODEL.BY_AMOUNT
                                )
                            if order:
                                Broker.market_data=data.select_day(str_i).select_code(code).data
                                order = Broker.warp(order)
                                order.trade('unknownTrade', order.price,order.amount, order.datetime) 
                        except Exception as ex:
                            lastEx = ex     
                            print("{}  {}。".format(datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"),lastEx)) 


                self.account=AC         
        
    def update_data(self):
        now=datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        print(now+' 正在更新盘中数据。。。')
        code=self.code
        data=self.data
        #code='159915'
        end=QA_util_get_real_date(datetime.date.today().strftime("%Y-%m-%d"), towards=-1)
        start=end#QA_util_get_last_day(self.end_date,30) #得到上一个(n)交易日        
        res=pd.DataFrame()
        for i in code:
            res_=QA.QAFetch.QATdx.QA_fetch_get_index_min(i,start,end,'5min')
            res=pd.concat([res,res_],axis=0)
        res.rename(columns={'vol':'volume'}, inplace=True)
        res.datetime=pd.to_datetime(res.datetime)
        data_new=QA_DataStruct_Index_min(res.set_index(['datetime', 'code'], drop=True))  

        if len(data_new.data)>0:
            data_new2=QA_DataStruct_Index_min(data_new.resample(self.frequence))
            data=data.select_time(self.start,self.end).__add__(data_new2)
            
        self.data=data
#run_bt([5,10,0.02,'50ETF'])
        now=datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        print(now+' 更新盘中数据完成。。。')    
    
#def run_bt(para):
#    print('开始运行'+str(para[0])+' '+str(para[1]))
#    time.sleep(5)
if __name__=='__main__':
    list_etf=['50ETF','300ETF','500ETF','创业板','800ETF']
    list_etf_code=['510050','510300','510500','159915','515800']    
    self=etf_macd_60min(code=list_etf_code,
                        market_type=QA.QAUtil.QAParameter.MARKET_TYPE.INDEX_CN,
                        frequence='60min',
                        model='trade',
                        days_in_advance=60,
                        account_cookie='etf_60'
                        )
    
    self.load_data() 
    self.update_data()
#def run_bt(code,start,end,para,market_type,portfolio_cookie,account_cookie):
#    print('开始运行'+str(para[0])+' '+str(para[1]))
#    self=macd_60min(
#                portfolio_cookie=portfolio_cookie,
#                account_cookie=account_cookie,#QA_util_random_with_topic(str(code)),   
#                market_type=market_type,#INDEX_CN,
#                start=start,
#                end=end,
#                code=code,
#                para=para  
#                )
#    
#    self.run()  
#    print('运行完成'+str(para[0])+' '+str(para[1])) 
#
#def run(max_process=3):
#
#    executor = ProcessPoolExecutor (max_process) 
#    
#    etf_list=QA.QA_fetch_etf_list()
#    etf_list[etf_list.name.str.contains('创业板')]
#    list_etf=['50ETF','300ETF','500ETF','创业板','800ETF']    
#    end=QA_util_get_real_date(datetime.date.today().strftime("%Y-%m-%d"), towards=-1)
#    start='2018-01-01'#QA_util_get_last_day(end_date,700) #得到上一个(n)交易日
#    
#    #单线程可以提前读取数据然后循环计算，多进程只能每次让其自己读取数据
#    list_etf=['50ETF','300ETF','500ETF','创业板','800ETF']       
#    list_i=list(np.arange(2,3,1))
#    list_j=list(np.arange(7,8,1))
#    all_task = []
#    portfolio_cookie='test'
#    for aa in list_etf: 
#        pass   
#        code=etf_list[etf_list.name==aa].code.tolist()[0] #两个300etf
#        name=etf_list[etf_list.name==aa].name.tolist()[0] #两个300etf
#        for i in list_i:
#            pass
#            for j in list_j:
#                pass
#                para=[12,26,9]
#                account_cookie=code+'_'+name+'_'+str(para)#QA_util_random_with_topic(str(code))
#                #run_bt(para)
#                executor.submit(
#                        run_bt,
#                        code=code,
#                        start=start,
#                        end=end,
#                        para=para,
#                        market_type=INDEX_CN,
#                        portfolio_cookie=portfolio_cookie,
#                        account_cookie=account_cookie
#                        )
#                #process_results = [task.result() for task in as_completed(all_task)]
#    executor.shutdown(True)
        
 
