# -*- coding: utf-8 -*-
"""
Created on Sat Aug 24 19:08:57 2019

@author: ZSL
"""
import QUANTAXIS as QA
import datetime
def if_trade_time(func):
    pass
    def wrapper(*args, **kwargs):  # 指定宇宙无敌参数
                
        if QA.QAUtil.QA_util_if_trade(datetime.datetime.now().strftime("%Y-%m-%d"))==True:#判断时候否在交易日
            ts=datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            timenum=int(ts[11:13])*100+int(ts[14:16])                
            if (timenum>=925 and timenum<1130) or (timenum>=1300 and timenum<1500): #or 1
                return func(*args, **kwargs)
            else:
                print(ts+' 非交易时间。。')                    
                return None             
        else:
            ts=datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            print(ts+' 非交易日期。。')                    
            return None                  
    return wrapper  # 返回