# -*- coding: utf-8 -*-
"""
Created on Fri Feb 26 23:02:07 2021

@author: ZSL
"""
import QUANTAXIS as QA
import numpy as np
import pandas as pd
import datetime
from QIFIAccount import QIFI_Account, ORDER_DIRECTION

myacc =  QIFI_Account(username='test1', password='test1', model="BACKTEST")

myacc.initial()
print('持仓')
print(myacc.positions)
myacc.on_price_change('000001', 23.29, '2021-01-27 09:58:00')
myacc.dtstr
myacc.datetime



st1=datetime.datetime.now()
# define the MACD strategy
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
    ZERO = 0
    return pd.DataFrame({'DIFF': DIFF, 'DEA': DEA, 'MACD': MACD, 'CROSS_JC': CROSS_JC, 'CROSS_SC': CROSS_SC, 'ZERO': ZERO})


# create account

data = QA.QA_fetch_stock_day_adv(
    ['000001', '000002', '000004', '600000'], '2017-09-01', '2018-05-20')
data = data.to_qfq()

# add indicator
ind = data.add_func(MACD_JCSC)
# ind.xs('000001',level=1)['2018-01'].plot()

data_forbacktest=data.select_time('2018-01-01','2018-05-01')

for items in data_forbacktest.panel_gen:
    for item in items.security_gen:
        daily_ind=ind.loc[item.index]
        pass
        item.data.close.values[0]
        if daily_ind.CROSS_JC.iloc[0]>0:
            myacc.on_price_change(item.code[0], item.data.close.values[0], str(item.date[0]))
            order = myacc.send_order(item.code[0], 
                                     1000, 
                                     item.data.close.values[0], 
                                     ORDER_DIRECTION.BUY, 
                                     datetime=item.date[0])
            myacc.make_deal(order)
        elif daily_ind.CROSS_SC.iloc[0]>0:
            myacc.on_price_change(item.code[0], item.data.close.values[0], str(item.date[0]))
            order = myacc.send_order(item.code[0], 
                                     1000, 
                                     item.data.close.values[0], 
                                     ORDER_DIRECTION.SELL, 
                                     datetime=item.date[0])
            myacc.make_deal(order)
    myacc.settle()
dir(myacc)
import  qifimanager  
ls=qifimanager.QA_QIFIMANAGER('test1')
a=ls.create_returns_tear_sheet()
