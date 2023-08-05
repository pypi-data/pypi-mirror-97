# -*- coding: utf-8 -*-
"""
Created on Thu Sep  6 22:25:21 2018

@author: ZSL
"""
#pip install QUANTAXIS
#pip install --upgrade QUANTAXIS
#pip install quantaxis==1.1.7.dev1
import pandas as pd
import QUANTAXIS as QA
import time
import datetime

from QUANTAXIS.QAFetch.QATdx import select_best_ip
from QUANTAXIS.QAUtil import (
                              QA_util_if_tradetime,
                              QA_util_if_trade

                              ) 
from QUANTAXIS.QASU.main import (
    QA_SU_save_future_list,
    QA_SU_save_future_day_all,
    QA_SU_save_future_min_all,
    )
if __name__=='__main__':
    
    #以下为qa的函数    
    select_best_ip()  #选ip是用了多进程函数 所以必须在if __name__=='__main__': 条件下执行，因为
    #之前出现过ip选不出来一直多进程卡死的现象，所以在下载之前先选出ip在进行下载    
        #期货
    QA_SU_save_future_list('tdx')
    QA_SU_save_future_day_all('tdx')
    QA_SU_save_future_min_all('tdx')
    
    #以下为qz的函数
    try:
        import quantzsl as qz
        qz.qz_save_stock_list_tushare() #股票列表    
        qz.qz_save_block_stock_eastmoney() #板块个股
        qz.qz_save_block_day_eastmoney()   #板块日线数据
        qz.qz_save_stock_day_tushare() #股票日线数据
        qz.qz_save_stock_daily_basic_tushare() #股票daily_basic数据   
    except:
        pass
    

    #股票
    QA.QA_SU_save_stock_list('tdx')
    QA.QA_SU_save_stock_day('tdx')
    QA.QA_SU_save_stock_xdxr('tdx')
    QA.QA_SU_save_stock_block('tdx')
    QA.QA_SU_save_stock_info('tdx')
    QA.QA_SU_save_stock_min('tdx')
    
    #指数
    QA.QA_SU_save_index_list('tdx')
    QA.QA_SU_save_index_day('tdx')
    QA.QA_SU_save_index_min('tdx')
    
    #etf
    QA.QA_SU_save_etf_day('tdx')
    QA.QA_SU_save_etf_min('tdx')
#        QA.QA_SU_save_etf_list('tdx')



    