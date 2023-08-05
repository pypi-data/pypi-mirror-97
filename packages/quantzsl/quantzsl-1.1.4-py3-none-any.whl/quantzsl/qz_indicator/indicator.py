# -*- coding: utf-8 -*-
"""
Created on Sat Oct  3 16:27:13 2020

@author: ZSL
"""
from functools import reduce

import numpy as np
import pandas as pd
import empyrical

from QUANTAXIS.QAIndicator.base import *

import QUANTAXIS as QA
data = QA.QA_fetch_stock_day_adv('000001', '2019-10-10', '2020-09-05').to_qfq()#.close#.plot()
DataFrame=data.data

def qz_indicator_sharpe(DataFrame, n=30):
    """
    MACD CALC
    """
    def cal_sharpe(Series):
        return(Series-0.04/252).mean() * math.sqrt(len(Series))/Series.std()  #std计算标准差

    pct_change=DataFrame[['close']].pct_change()
    res=pct_change.rolling(n).apply(cal_sharpe)
    res.columns=['sharpe']
    return res
'''
将计算那结果与股票价格进行对比，结果还算理想
'''
#res=data.add_func(qz_indicator_sharpe,30)
#aa=pd.concat([DataFrame,res],axis=1)
#aa['close']=aa['close']-16
#aa['zo']=0
#aa[['close','sharpe','zo']].plot()

'''
次计算公式和empyrical包里roll_sharpe_ratio计算出来的数值差3倍左右，不知道原因
'''
#    res=data.add_func(qz_indicator_sharpe,30) *3   
#    aaa=empyrical.roll_sharpe_ratio(DataFrame['close'].pct_change(),n)
#    aa=pd.concat([aaa,res],axis=1)
#    aa['zo']=0
#    aa.plot()


    
def qz_indicator_sortino(DataFrame, n=63):
    """
    索提诺比率（Sortino Ratio）区分了波动的好坏，计算波动时它所采用的不是标准差，而是下行标准差。
    意思是，投资组合的上涨（正回报率）符合投资人的需求，不应计入风险调整。
    Sortino Ratio越高，表明基金承担相同单位下行风险能获得更高的超额回报率。
    索提诺比率可以看作是夏普比率在衡量对冲基金/私募基金时的一种修正方式。
    关于夏普比率详情，参见《理解Sharpe夏普比率与Python实现》
    """
    def cal_sharpe(Series):
        return(Series-0.004/252).mean() * math.sqrt(len(Series))/Series.std()  #std计算标准差

    pct_change=DataFrame[['close']].pct_change()
    res=pct_change.rolling(n).apply(cal_sharpe)
    res.columns=['sharpe']
    return res

    res=empyrical.roll_sortino_ratio(DataFrame['close'].pct_change(),n)
    aaa=empyrical.roll_sharpe_ratio(DataFrame['close'].pct_change(),n)
    aa=pd.concat([aaa,res],axis=1)
    aa=pd.concat([aa,DataFrame['close']-16],axis=1)
    aa['zo']=0
    aa.plot()
    
    
    return pd.DataFrame({'DIF': DIF, 'DEA': DEA, 'MACD': MACD})

def qz_indicator_sharpe(DataFrame,*args,**kwargs):
    """MA
    
    Arguments:
        DataFrame {[type]} -- [description]
    
    Returns:
        [type] -- [description]
    """

    CLOSE = DataFrame['close']
    return pd.DataFrame({'MA{}'.format(N): MA(CLOSE, N)  for N in list(args)})