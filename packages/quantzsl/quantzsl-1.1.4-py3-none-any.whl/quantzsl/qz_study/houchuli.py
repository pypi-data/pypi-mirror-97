# -*- coding: utf-8 -*-
"""
Created on Thu Mar 21 11:05:01 2019

@author: Administrator
"""

import pandas as pd
import numpy as np
import datetime
import pymongo
import json
import quantzsl as qz
import time
import QUANTAXIS as QA
import glob
import os
from quantzsl.qz_database.qz_mongo import (
                                                qz_mongo
                                            )

from QUANTAXIS.QAARP.QAAccount import QA_Account
from QUANTAXIS.QAARP.QARisk import QA_Performance, QA_Risk

def save_acc_message_to_excel(user_cookie,portfolio_cookie,account_cookie,dir_acc,start=None,end=None):
    AC=QA_Account(account_cookie=account_cookie,
                  portfolio_cookie=portfolio_cookie,
                  user_cookie=user_cookie
                  )
    
    AC.reload()
#    end='2021-02-18'#QA_util_get_real_date(datetime.date.today().strftime("%Y-%m-%d"), towards=-1)
#    start='2020-01-01'
    if start:
        AC.start_=start
        AC.end_=end      
    history_table_min=AC.history_table_min
    cash=AC.cash
#    dir(AC) 
    cash_table=AC.cash_table 

    r = QA.QA_Risk(AC,if_fq=True)
    p=QA_Performance(AC)
    r.plot_assets_curve() 
    risk_mess=r.message
    acc_mess=AC.message
    perf_mess=p.message
    risk_mess
    assets=r.assets     
#    AC.save()
#    r.save()
    res_perf=pd.DataFrame({
                            '初始资金':[risk_mess['init_cash']],
                            '最终资产':[risk_mess['last_assets']], 
                            '阿尔法':[risk_mess['alpha']],
                            '贝塔':[risk_mess['beta']],
                            '夏普比率':[risk_mess['sharpe']], 
                            '最大回撤':[risk_mess['max_dropback']], 
                            '年华收益率':[risk_mess['annualize_return']],
                            '信息比率':[risk_mess['ir']],  
                            '持续时间':[risk_mess['time_gap']+1],
                            '总佣金':[-risk_mess['total_commission']],
                            '总税金':[-risk_mess['total_tax']],
                            '利润':[risk_mess['profit_money']],                            
                            '总收益':[perf_mess['total_profit']],
                            '总亏损':[perf_mess['total_loss']],
                            '总盈利/总亏损':[perf_mess['total_pnl']],
                            '交易比数':[perf_mess['trading_amounts']],
                            '利润笔数':[perf_mess['profit_amounts']],
                            '亏损笔数':[perf_mess['loss_amounts']],
                            '持平笔数':[perf_mess['even_amounts']],
                            '利润单占比':[perf_mess['profit_precentage']],
                            '亏损单占比':[perf_mess['loss_precentage']],
                            '持平单占比':[perf_mess['even_precentage']],
                            '每单平均利润':[perf_mess['average_profit']],
                            '每单平均亏损':[perf_mess['average_loss']],
                            '均利润/均亏损':[perf_mess['average_pnl']],
                            '单笔最大利润':[perf_mess['max_profit']],
                            '单笔最大亏损':[perf_mess['max_loss']],
                            '单笔最大利润/亏损':[perf_mess['max_pnl']],
                            '净利润/总亏损':[perf_mess['netprofio_maxloss_ratio']],
                            '连续盈利单数':[perf_mess['continue_profit_amount']],
                            '连续亏损单数':[perf_mess['continue_loss_amount']],
                            '平均持仓时间':[perf_mess['average_holdgap']],
                            '利润平均持仓时间':[perf_mess['average_profitholdgap']],
                            '亏单平均持仓时间':[perf_mess['average_losssholdgap']],
                            'account_cookie':account_cookie,
                            }).set_index('account_cookie').T
    
    res_asset=pd.DataFrame({
                            'timeindex':risk_mess['totaltimeindex'],
                            'benchmark_assets':risk_mess['benchmark_assets'],
                            'assets':risk_mess['assets'],
                            })
    
    res_pnl=p.pnl_lifo
    res_history_table=AC.history_table
    with pd.ExcelWriter(dir_acc+'/'+
                        str(datetime.datetime.now().strftime("%Y-%m-%d"))+' '+
                        portfolio_cookie+'_'+
                        account_cookie+'.xlsx') as writer:
        res_perf.to_excel(writer, sheet_name='概况')         
        res_asset.to_excel(writer, sheet_name='资产')  
        res_pnl.to_excel(writer, sheet_name='交易明细')
        res_history_table.to_excel(writer, sheet_name='买卖明细')
if __name__=='__main__':
    client = qz_mongo().quantzsl
    username='quantaxis'
    password='quantaxis'
    User=QA.QA_User(username=username,password=password)
    user_cookie= User.user_cookie
    portfolio_cookie='xincelue'
    account_cookie='day_allm_10w_qzt_2021' 
    work_path=os.getcwd()
    dir_acc =r"/".join(work_path.split("\\")) #"D:\\ANSYS\\20190718jietou" 
    save_acc_message_to_excel(user_cookie,portfolio_cookie,account_cookie,dir_acc)#,
                              #start='2005-01-04',
                              #end='2005-04-01')
   