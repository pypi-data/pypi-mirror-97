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
import quantzsl as qz
from QUANTAXIS.QAFetch.QATdx import select_best_ip
if __name__=='__main__':

    #以下为qz的函数
    qz.qz_save_block_stock_eastmoney() #板块个股
    qz.qz_save_block_day_eastmoney()   #板块日线数据
    qz.qz_save_stock_list_tushare() #股票列表
    qz.qz_save_stock_day_tushare() #股票日线数据
    qz.qz_save_stock_daily_basic_tushare() #股票daily_basic数据
    