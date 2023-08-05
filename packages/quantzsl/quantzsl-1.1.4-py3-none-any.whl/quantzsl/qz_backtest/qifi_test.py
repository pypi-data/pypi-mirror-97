# -*- coding: utf-8 -*-
"""
Created on Fri Feb 26 22:20:55 2021

@author: ZSL
"""
import QUANTAXIS as QA
import numpy as np
import pandas as pd
import datetime
from QIFIAccount import QIFI_Account, ORDER_DIRECTION
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
username='quantaxis'
password='quantaxis'
User=QA.QA_User(username=username,password=password)
user_cookie= User.user_cookie
portfolio_cookie='xincelue'
account_cookie='day_allm_10w_qzt_2021' 
AC=QA.QA_Account(account_cookie=account_cookie,
              portfolio_cookie=portfolio_cookie,
              user_cookie=user_cookie
              )

AC.reload()



history_table=AC.history_table
#history_table.to_excel('history_table.xlsx')

#history_tabl=pd.read_excel('history_table.xlsx',dtype={'code':str})
DATABASE.history.delete_many({
                          'account_cookie':account_cookie,
                          'portfolio':'QAPaperTrade'
                          })
myacc =  QIFI_Account(username=account_cookie, password=account_cookie,init_cash=100000, model="BACKTEST")
myacc.initial()
date=history_table.iloc[0,:].datetime[:10]
for i in history_table.index: ###########此处运行前4个都是买入没问题，运行第5个卖出后 acc.money不增加,
    #导致后续买不进去
    #i=history_table.index[4]
    pass
    ls=history_table.iloc[i,:]
    if ls.datetime[:10]==date:
        pass
    else:
        myacc.settle() 
        date=ls.datetime[:10]
    print(i)


    if ls.amount>0:
        direc=ORDER_DIRECTION.BUY
        amount=ls.amount
    else:
        direc=ORDER_DIRECTION.SELL
        amount=-ls.amount
    myacc.on_price_change(ls.code, ls.price, ls.datetime)    
    order = myacc.send_order(ls.code, 
                             amount, 
                             ls.price, 
                             direc, 
                             ls.datetime)
    myacc.make_deal(order)
    myacc.on_price_change(ls.code, ls.price, ls.datetime)   


    
myacc.positions
myacc.float_profit
myacc.balance
myacc.money




order = myacc.send_order('000001', 100, 12, ORDER_DIRECTION.BUY, datetime='2020-01-01')
import uuid
myacc.make_deal(order)

myacc.get_position('stock_cn.000001').last_price
myacc.get_position('stock_cn.000001').open_cost_long
myacc.datetime
myacc.on_price_change('000001', 13, '2020-01-01')
myacc.positions
myacc.float_profit
myacc.balance
myacc.money





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
            order = myacc.send_order(item.code[0], 
                                     1000, 
                                     item.data.close.values[0], 
                                     ORDER_DIRECTION.BUY, 
                                     datetime=str(item.date[0]))
            myacc.make_deal(order)
        elif daily_ind.CROSS_SC.iloc[0]>0:
            order = myacc.send_order(item.code[0], 
                                     1000, 
                                     item.data.close.values[0], 
                                     ORDER_DIRECTION.SELL, 
                                     datetime=str(item.date[0]))
            myacc.make_deal(order)
    myacc.settle()
dir(myacc)
import  qifimanager  
ls=qifimanager.QA_QIFIMANAGER('test')
a=ls.create_returns_tear_sheet()
