# -*- coding: utf-8 -*-
"""
Created on Thu Oct  1 19:56:13 2020

@author: ZSL
"""

# -*- coding: utf-8 -*-
"""
Created on Mon Feb 17 14:10:18 2020

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
import datetime 
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
                              QA_util_get_trade_range
                              )

from QUANTAXIS.QAUtil.QADate import (
                                QA_util_to_datetime,
                                QA_util_datetime_to_strdate,
                                QA_util_datetime_to_strdatetime
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
from QUANTAXIS.QAData.data_resample import (
    QA_data_day_resample,#day  to  week
    QA_data_min_to_day,#min to day
    QA_data_min_resample,#min to min
)
from QUANTAXIS.QAData import (
                                QA_DataStruct_Stock_min,
                                QA_DataStruct_Stock_day,
                                    QA_DataStruct_Index_day,
                                    QA_DataStruct_Index_min,
                                )
from QUANTAXIS.QAUtil.QAParameter import (FREQUENCE, MARKET_TYPE,
                                          OUTPUT_FORMAT)
STOCK_CN=MARKET_TYPE.STOCK_CN
INDEX_CN=MARKET_TYPE.INDEX_CN
frequence_day_=[FREQUENCE.YEAR,FREQUENCE.MONTH,FREQUENCE.WEEK,FREQUENCE.DAY]
frequence_min_=[FREQUENCE.ONE_MIN,FREQUENCE.FIVE_MIN,FREQUENCE.FIFTEEN_MIN,
                FREQUENCE.THIRTY_MIN,FREQUENCE.SIXTY_MIN]



class stock_backtest_base():
    '''
    回测基类，支持股票、指数、etf的单标的和多标的
    回测分为两种，一种为一次性回测，即先读入全部数据，然后计算指标 进行回测，
    另一种为增量回测，每日从数据库读入当日数据，和老数据合同，然后计算指标，进行回测
    第二种模式主要是全市场长时间分钟回测或者计算买卖指标需要获取每日持仓数据时，由于设备原因不能一次性全部读入数据，所以分开读入数据
    直接继承然后修改cal_signal函数即可，如有需要也可以修改on_bar函数
    '''
    def __init__(self,
                username='quantaxis',
                password='quantaxis',
                portfolio_cookie='simulate',
                account_cookie='default',
                code=['000001'],
                start='2018-01-01',
                end='2019-01-01', 
                frequence='day',
                market_type=QA.QAUtil.QAParameter.MARKET_TYPE.STOCK_CN,
                max_hold=2,
                para=[5,20,30],
                data=None,
                if_real_save=False,
                if_add_data=False,
                days_in_advance=0,
                init_cash=100000
                ):
        pass
        self.username=username
        self.password=password    
        self.portfolio_cookie=portfolio_cookie
        self.account_cookie=account_cookie
        self.code=code
        self.start=start
        self.end=end
        self.frequence=frequence
        self.market_type=market_type
        self.broker=QA.QA_BacktestBroker()
        self.max_hold=max_hold
        self.para=para
        self.data=data
        self.real_save=if_real_save#每回测一天 就将结果存入数据库，方便大周期回测时 查看实时结果
        self.if_add_data=if_add_data #是否执行增量回测模式
        self.buy=[]
        self.sell=[]
        self.len_data=250 #增量模式下 数据存储的最大长度
        self.days_in_advance=days_in_advance
        self.init_cash=init_cash
    def load_account(self):
        username=self.username
        password=self.password
        User=QA.QA_User(username=username,password=password)
        Portfolio = User.new_portfolio(self.portfolio_cookie)
        self.user_cookie= User.user_cookie
        try:
            DATABASE.account.delete_many({
                                          'user_cookie':self.user_cookie,
                                          'account_cookie':self.account_cookie,
                                          'portfolio_cookie':self.portfolio_cookie
                                          
                                          })
            DATABASE.risk.delete_many({
                                      'user_cookie':self.user_cookie,
                                      'account_cookie':self.account_cookie,
                                      'portfolio_cookie':self.portfolio_cookie
                                      })
            print("删除既有账号")
#            re=DATABASE.account.find({
#                                          'user_cookie':self.user_cookie,
#                                          'account_cookie':self.account_cookie,
#                                          'portfolio_cookie':self.portfolio_cookie
#                                          
#                                              })
#            aa=pd.DataFrame([i for i in re])
        except:
            pass
       
        AC = Portfolio.new_account(account_cookie=self.account_cookie,
                                   init_cash=self.init_cash, 
                                   commission_coeff=0.0002,
                                   tax_coeff=0.001,
                                   frequence=self.frequence)     
        AC.frequence=self.frequence
        AC.init_cash=self.init_cash
        AC.cash = [self.init_cash]  #程序bug  就是传不进去  需要手动更正  也是醉了
        self.user=User
        self.portfolio=Portfolio
        self.account=AC 
        

    def load_data(self):
        '''
        不传入data时从数据库读取数据
        '''
        if self.if_add_data: #如果为增量回测模式 首次无需读入数据
            pass
            if self.days_in_advance>0:
                now=datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                print(now+' 正在载入部分历史数据。。。') 
                data = QA.QA_quotation(self.code,
                                            QA_util_get_last_day(QA_util_get_real_date(self.start),self.days_in_advance), 
                                            self.start, 
                                            source=QA.DATASOURCE.MONGO,
                                            frequence=self.frequence, 
                                            market=self.market_type, 
                                            output=QA.OUTPUT_FORMAT.DATASTRUCT)        
                try:#此处是为了兼容 index没有复权的问题
                    self.data=data.to_qfq()  
                except:
                    self.data=data 
        else:
            now=datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            print(now+' 正在载入全部历史数据。。。')             
            data = QA.QA_quotation(self.code,
                                        QA_util_get_last_day(QA_util_get_real_date(self.start),self.days_in_advance), 
                                        self.end, 
                                        source=QA.DATASOURCE.MONGO,
                                        frequence=self.frequence, 
                                        market=self.market_type, 
                                        output=QA.OUTPUT_FORMAT.DATASTRUCT)        
            try:#此处是为了兼容 index没有复权的问题
                self.data=data.to_qfq()  
            except:
                self.data=data            
    def cal_signal(self):
        try: #计算指标加兼容，防止数据长度不够等原因计算出错
            data=self.data
            para=self.para
            ind = data.add_func(QA.QA_indicator_MA,para[0],para[1])
            indadv =QA.QA_DataStruct_Indicators(ind)#.dropna())
            buy=ind[QA.CROSS(ind[ind.columns[0]],ind[ind.columns[1]])==1].reset_index()
            #buy.date=buy.date.apply(lambda x :pd.to_datetime(QA_util_get_next_day(x, 1))) #将交易日期错后一天 既第二天开盘价买入    
        
            sell=ind[QA.CROSS(ind[ind.columns[1]], ind[ind.columns[0]])==1].reset_index()
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
        except Exception as ex:   
            print("{} cal_signal has something wrong:{}。".format(datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"),ex))     
            self.buy=pd.DataFrame({'date':None,
                                   'code':None})
            self.sell=pd.DataFrame({'date':None,
                                   'code':None})
    def on_bar(self,i):  #单周期 onbar模板（单股票、多股票）
        buy=self.buy
        sell=self.sell
        max_hold=self.max_hold
        AC=self.account
        data=self.data
        Broker=self.broker
        #print(i)  

        if self.frequence in frequence_day_:
            date_='date'
            str_i=QA_util_datetime_to_strdate(QA_util_pands_timestamp_to_date(i))
        if self.frequence in frequence_min_:
            date_='datetime'
            str_i=QA_util_datetime_to_strdatetime(QA_util_pands_timestamp_to_datetime(i))
            
        # if i in buy[date_].tolist():
        #     pass
        if len(sell)>0:        
            for code in sell[sell[date_]==i].code:
                pass        
                if AC.sell_available.get(code, 0) > 0:
                    try :
                        price=round(data.select_day(str_i).select_code(code).close.values[0],2)
                        order = AC.send_order(
                                code=code, time=str_i, amount=AC.sell_available.get(code, 0), 
                                towards=QA.ORDER_DIRECTION.SELL, price=price, 
                                order_model=QA.ORDER_MODEL.CLOSE, #市价单 成交价为bar的最高价和最低价平均
                                amount_model=QA.AMOUNT_MODEL.BY_AMOUNT
                            )
                        if order:
                            Broker.market_data=data.select_day(str_i).select_code(code).data
                            order = Broker.warp(order)
                            order.trade('unknownTrade', order.price,order.amount, order.datetime) 
                    except Exception as ex:
                        lastEx = ex     
                        print("{}  {}。".format(datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"),lastEx)) 

        if len(buy)>0:
            for code in buy[buy[date_]==i].code:# 一直买直到买够max_hold或者buy的code不足 [:max_hold].code:
                pass
                if code not in AC.hold.index.to_list():
                    try:
                        max_to_hold=max_hold-len(AC.hold)
                        acount_to_buy=min(len(buy[buy[date_]==i]),max_to_hold)
                        if acount_to_buy > 0:
                            price=round(data.select_day(str_i).select_code(code).close.values[0],2)
                
                            order = AC.send_order(
                                    code=code, time=str_i, money=AC.latest_cash*0.98/acount_to_buy, 
                                    towards=QA.ORDER_DIRECTION.BUY, price=price, 
                                    order_model=QA.ORDER_MODEL.CLOSE, #限价单 按照委托价成交
                                    amount_model=QA.AMOUNT_MODEL.BY_MONEY
                                )
                            if order:
                                Broker.market_data=data.select_day(str_i).select_code(code).data
                                order = Broker.warp(order)
                                order.trade('unknownTrade', order.price,order.amount, order.datetime)
                    except Exception as ex:
                        lastEx = ex     
                        print("{}  {}。".format(datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"),lastEx))                

                
        # if i in sell[date_].tolist():
        self.account=AC 
    def initialize(self):
        '''
        初始化，回测前如有需要定义的参数，可以放在这里
        '''
        pass
    def run(self): 
        
        self.initialize()
        datelist=pd.to_datetime(QA_util_get_trade_range(self.start, self.end) )      
        data=self.data
        if data==None:
            self.load_data() 
        data=self.data    
        self.load_account()     
        AC=self.account
       
        index_=datelist
        if self.if_add_data: #如果为增量回测模式 不用在外面计算指标
            pass
        else:
            self.cal_signal()            
        for i in index_: #每一天循环
            pass
            self.date=i#QA_util_format_date2str(i)
            if self.if_add_data: #如果为增量回测模式 需要读入数据
                print('读入数据')
#                    aa=QA.QA_fetch_index_min_adv(self.code,
#                                        '2020-12-31', 
#                                        '2020-12-31',
#                                        frequence=self.frequence)
#                    aaa=aa.data
                data_new= QA.QA_quotation(self.code,
                                    str(i)[:10], 
                                    str(i)[:10], 
                                    source=QA.DATASOURCE.MONGO,
                                    frequence=self.frequence, 
                                    market=self.market_type, 
                                    output=QA.OUTPUT_FORMAT.DATASTRUCT)
                try:#此处是为了兼容 index没有复权的问题
                    self.data_new=data_new.to_qfq()
                except:
                    self.data_new=data_new
                try:#此处是为了兼容第一天回测没有旧数据的问题
                    self.data=self.data.__add__(self.data_new)
                    if self.frequence in frequence_day_:
                        ls=min(self.len_data,len(self.data.date))     
                    if self.frequence in frequence_min_:                    
                        ls=min(self.len_data,len(self.data.datetime))
                    self.data=self.data.select_time(self.data.datetime[-ls],self.data.datetime[-1])
                except:
                    self.data=self.data_new  
                    self.data.data.index.to_list()
                #self.data=self.data.select_time(self.data.date[-])[-10000:]  #取前250行 为了防止每天堆积数据 太多过卡
                data=self.data
                try:#此处是为了兼容  回测第一天数据可能太短   计算指标会出错
                    self.cal_signal() 
                    print('计算信号完成'+str(self.date))
                except:
                    pass        
            #i=index_[1]
            
            #i=pd.to_datetime(self.date)#调试用
            print(i)
            #i=index_[1]
            if self.frequence in frequence_day_:
                self.on_bar(i)
                print('on bar完成'+str(self.date))
            if self.frequence in frequence_min_:
                ls=self.data.select_day(QA_util_format_date2str(i)).data
                ls_=ls.reset_index().datetime.to_list()
                ls=list(set(ls_))
                ls.sort()
                for j in ls:#不能把.levels[0]放在此处，会回复成原来的。。。
                    pass
                    self.on_bar(j)
            AC.end_=QA_util_format_date2str(i)
            AC.settle()
            if self.real_save: #实时保存回测结果
                try: #防止第一天没有交易的容错
                    AC.save()
                    #aa=AC.history_table
                    if self.frequence in frequence_day_:
                        #aa=AC.history_table
                        r = QA.QA_Risk(AC,if_fq=False,market_data=data.select_time(AC.start_date,AC.end_date).select_code(AC.code))
                        r.save() 
                        #r.plot_assets_curve() 
                        r.init_cash
                        r.assets()
                    if self.frequence in frequence_min_:
                        if self.market_type==STOCK_CN:
                            market_data=QA.QA_fetch_stock_day_adv(AC.code, AC.start_date, AC.end_date)          
                        elif self.market_type==INDEX_CN:                
                            market_data=QA.QA_fetch_index_day_adv(AC.code, AC.start_date, AC.end_date)

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
                    market_data=QA.QA_fetch_stock_day_adv(AC.code, AC.start_date, AC.end_date)          
                elif self.market_type==INDEX_CN:                
                    market_data=QA.QA_fetch_index_day_adv(AC.code, AC.start_date, AC.end_date)
                r = QA.QA_Risk(AC,if_fq=False,market_data=market_data)
                r.save() 
                r.plot_assets_curve()
            self.risk=r                
        except:
            pass 
#self.daily_hold()

if __name__=='__main__':
    #上证指数 000001
    #上证50  000016
    #中证500 399905
    #沪深300 000300
    #创业板  399006

    code='000001'
    end='2021-02-01' #QA_util_get_real_date(datetime.date.today().strftime("%Y-%m-%d"), towards=-1)
    start='2020-11-01' 
    
    self=stock_backtest_base(
                portfolio_cookie='etf_day_ma_double',
                account_cookie='test',#QA_util_random_with_topic('hs300_')    
                market_type=STOCK_CN,#INDEX_CN,
                code=code,
                start=start,
                end=end,
                para=[5,40] ,
                frequence='30min',
                if_real_save=True,
                if_add_data=True                
                )
    self.run()    
    

#dir(self.account)
#dir(self.risk)
#amessage=self.account.message  #存入数据库部分
#ahistory_table=self.account.history_table#交易列表
#acash_table=self.account.cash_table #资金列表
#atrade_range=self.account.trade_range #交易日期列表
#atrade=self.account.trade # 交易切面表
#adaily_hold=self.account.self.daily_hold #持仓切面表
#adaily_cash=self.account.daily_cash #持仓切面表
#adaily_frozen=self.account.daily_frozen
#a=data.data
#self.generate_randomtrade('000001',start,end,'30min')
#self=self.account
#    etf_list=QA.QA_fetch_index_list()
#    etf_list[etf_list.name.str.contains('创业板')]
#    list_etf=['50ETF','300ETF','500ETF','创业板','800ETF']    
#    code='000005'#etf_list[etf_list.name=='50ETF'].code.tolist()[0]
#    end_date=QA_util_get_real_date(datetime.date.today().strftime("%Y-%m-%d"), towards=-1)
#    start_date='2021-01-01' 