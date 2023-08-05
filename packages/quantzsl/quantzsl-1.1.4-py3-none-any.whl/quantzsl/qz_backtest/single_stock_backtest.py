# -*- coding: utf-8 -*-
"""
Created on Thu Oct  1 20:58:46 2020

@author: ZSL
"""

import time
import datetime
import random
import pandas as pd
import numpy as np
import quantzsl as qz
import QUANTAXIS as QA
STOCK_CN=QA.QAUtil.QAParameter.MARKET_TYPE.STOCK_CN
INDEX_CN=QA.QAUtil.QAParameter.MARKET_TYPE.INDEX_CN
from QUANTAXIS.QAUtil import (
                              QA_util_get_real_date,
                              QA_util_get_last_day,
                              QA_util_get_next_day,
                              QA_util_format_date2str,
                              QA_util_random_with_topic,
                              ORDER_STATUS,
                              DATABASE
                              )   
frequence_day_=[QA.FREQUENCE.YEAR,QA.FREQUENCE.MONTH,QA.FREQUENCE.WEEK,QA.FREQUENCE.DAY]
frequence_min_=[QA.FREQUENCE.ONE_MIN,QA.FREQUENCE.FIVE_MIN,QA.FREQUENCE.FIFTEEN_MIN,
                QA.FREQUENCE.THIRTY_MIN,QA.FREQUENCE.SIXTY_MIN]
from concurrent.futures import (
                                ThreadPoolExecutor, 
                                ProcessPoolExecutor,
                                as_completed
                                                )
from quantzsl import stock_backtest_base

class backtest(stock_backtest_base):

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
        
def run_bt(code,start,end,para,market_type,portfolio_cookie,account_cookie):
    print('开始运行'+str(para[0])+' '+str(para[1]))
    self=backtest(
                portfolio_cookie=portfolio_cookie,
                account_cookie=account_cookie,#QA_util_random_with_topic(str(code)),   
                market_type=market_type,#INDEX_CN,
                start=start,
                end=end,
                code=code,
                para=para  
                )
    
    self.run()  
    print('运行完成'+str(para[0])+' '+str(para[1])) 

def run(max_process=3):

    executor = ProcessPoolExecutor (max_process) 
    
    etf_list=QA.QA_fetch_etf_list()
    etf_list[etf_list.name.str.contains('创业板')]
    list_etf=['50ETF','300ETF','500ETF','创业板','800ETF']    
    end=QA_util_get_real_date(datetime.date.today().strftime("%Y-%m-%d"), towards=-1)
    start='2018-01-01'#QA_util_get_last_day(end_date,700) #得到上一个(n)交易日
    
    #单线程可以提前读取数据然后循环计算，多进程只能每次让其自己读取数据
    list_etf=['50ETF','300ETF','500ETF','创业板','800ETF']       
    list_i=list(np.arange(2,3,1))
    list_j=list(np.arange(7,8,1))
    all_task = []
    portfolio_cookie='test'
    for aa in list_etf: 
        pass   
        code=etf_list[etf_list.name==aa].code.tolist()[0] #两个300etf
        name=etf_list[etf_list.name==aa].name.tolist()[0] #两个300etf
        for i in list_i:
            pass
            for j in list_j:
                pass
                para=[12,26,9]
                account_cookie=code+'_'+name+'_'+str(para)#QA_util_random_with_topic(str(code))
                #run_bt(para)
                executor.submit(
                        run_bt,
                        code=code,
                        start=start,
                        end=end,
                        para=para,
                        market_type=INDEX_CN,
                        portfolio_cookie=portfolio_cookie,
                        account_cookie=account_cookie
                        )
                #process_results = [task.result() for task in as_completed(all_task)]
    executor.shutdown(True)
    






#run_bt([5,10,0.02,'50ETF'])
    
    
#def run_bt(para):
#    print('开始运行'+str(para[0])+' '+str(para[1]))
#    time.sleep(5)
if __name__=='__main__':
    run()
 


