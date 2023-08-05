# -*- coding: utf-8 -*-
"""
Created on Sat Jan 16 15:37:25 2021

@author: ZSL
"""

import quantzsl as qz
import QUANTAXIS as QA
import datetime
import pandas as pd
import numpy as np
from QUANTAXIS.QAData import (
    QA_DataStruct_Stock_day
)
from QUANTAXIS.QAData.data_resample import (
    QA_data_tick_resample,
    QA_data_day_resample,
    QA_data_futureday_resample,
    QA_data_min_resample,
    QA_data_futuremin_resample,
    QA_data_cryptocurrency_min_resample
)




##获取股票列表
stock_list_=qz.qz_fetch_stock_list_tushare()
stock_list_all=stock_list_.code.to_list()
stock_list_kcb=stock_list_[stock_list_['market']=='科创板'].code.to_list()
stock_list=sorted(list(set(stock_list_all).difference(set(stock_list_kcb))))
##获取日线数据
delta=300
end=datetime.datetime.now().strftime("%Y-%m-%d")
start=(datetime.date.today() - datetime.timedelta(days=delta)).strftime("%Y-%m-%d")
stock_data=qz.qz_fetch_stock_day_tushare(code=stock_list,start=start,end=end)
#res =QA.QA_fetch_stock_day(code=stock_list,start=start,end=end,format='pd')
#data=QA.QA_fetch_stock_day_adv(code=stock_list,start=start,end=end)
data=QA_DataStruct_Stock_day(stock_data.set_index(['date', 'code'], drop=True)).to_qfq()


def cal_macd(data,status=0):
    '''
    选出macd大于零的code
    支持股票、板块数据和指数
    Parameters
    ----------
    data : adv格式
        日线数据的adv格式..

    Returns
    -------
    最后一天满足条件的list格式的code.

    '''
    
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
        CROSS_JC_STATUS = QA.CROSS_STATUS(DIFF, DEA)
        CROSS_SC_STATUS = QA.CROSS_STATUS(DEA, DIFF)        
        ZERO = 0
        return pd.DataFrame({'DIFF': DIFF, 
                             'DEA': DEA, 
                             'MACD': MACD, 
                             'CROSS_JC': CROSS_JC, 
                             'CROSS_SC': CROSS_SC, 
                             'CROSS_JC_STATUS': CROSS_JC_STATUS, 
                             'CROSS_SC_STATUS': CROSS_SC_STATUS,                             
                             'ZERO': ZERO})
    ind=data.add_func(MACD_JCSC).dropna() #采用默认参数计算macd
    ind_adv =QA.QA_DataStruct_Indicators(ind.dropna())
    #ind.groupby(level=1, sort=False).apply(cross)
    if status==0:
        res_ind=ind[ind['CROSS_JC']==1].reset_index()
#        aa=res_ind[res_ind.code=='000001']
    else:
        res_ind=ind[ind['CROSS_JC_STATUS']==1].reset_index()
    if 'datetime' in res_ind.columns:
        res_ind['date']=res_ind.datetime
    ls=list(set(res_ind.date))
    ls.sort()
    res_=[]
    for i in ls:
        pass  
        ls_=res_ind[res_ind.date==i].code.to_list() 
        res_.append([i,ls_,len(ls_)])
    res_day=pd.DataFrame(res_)  
    res_day.columns=['date','code','amount']  
    
    return res_day.code[-1:].values[0]


##计算日线级别指标
res_code_day=cal_macd(data,status=1)
##计算周线级别指标
'''
因为有个别股票处于停盘状态，导致他们读取的第一天和大多数股票不一样，这样在resample到week级别的时候
就会多出一天的数据和大部分数据对不上，所以先弄一个标准的周线date日期然后。
'''
index_day_=pd.DataFrame(data.index.levels[0].to_list(),columns=['date']).assign(
            code='000001',
            open=1,
            high=1,
            low=1,
            close=1,
            volume=1,
            amount=1)
index_day=data.index.levels[0]
index_week=QA_data_day_resample(index_day_,type_='w').index.levels[0]
data_week_=data.week.reset_index()
data_week_=data_week_[data_week_.date.isin(index_week)]
data=QA_DataStruct_Stock_day(data_week_.set_index(['date', 'code'], drop=True))
res_code_week=cal_macd(data,status=1)
##计算60min线级别指标
'''
60分钟级别 数据量大 少度几天
'''
delta_60min=delta/20
end_60min=datetime.datetime.now().strftime("%Y-%m-%d")
start_60min=(datetime.date.today() - datetime.timedelta(days=delta_60min)).strftime("%Y-%m-%d")
data=QA.QA_fetch_stock_min_adv(code=stock_list,start=start_60min,end=end_60min,frequence='60min').to_qfq()
res_code_60min=cal_macd(data,status=1)

res_code_bar=list(set(res_code_day).intersection(set(res_code_week)))
res_code_bar=list(set(res_code_bar).intersection(set(res_code_60min)))
res_code_bar.sort()


block=qz.qz_fench_block_eastmoney()
概念分类=block[block['fenlei']=='概念板块'][['block','block_code']].drop_duplicates()
行业分类=block[block['fenlei']=='行业板块'][['block','block_code']].drop_duplicates()
地域分类=block[block['fenlei']=='地域板块'][['block','block_code']].drop_duplicates()

# res2=概念分类[概念分类['block']=='芯片']
# res2=block[block['block'].str.contains('芯片')].code.to_list()

list_gainian=概念分类.block_code.to_list()
data=qz.qz_fetch_block_stock_day_eastmoney(code=list_gainian,start=start,end=end)
data=QA_DataStruct_Stock_day(data.set_index(['date', 'code'], drop=True))
##计算日线级别指标
res_code_gainian_day=cal_macd(data,status=1)
##计算周线级别指标
'''
因为有个别股票处于停盘状态，导致他们读取的第一天和大多数股票不一样，这样在resample到week级别的时候
就会多出一天的数据和大部分数据对不上，所以先弄一个标准的周线date日期然后。
'''
data_week_=data.week.reset_index()
data_week_=data_week_[data_week_.date.isin(index_week)]
data=QA_DataStruct_Stock_day(data_week_.set_index(['date', 'code'], drop=True))
res_code_gainian_week=cal_macd(data,status=1)

res_ls=list(set(res_code_gainian_day).intersection(set(res_code_gainian_week)))
res_code_gainian=list(set(block[block.block_code.isin(res_ls)].code))



list_hangye=行业分类.block_code.to_list()
data=qz.qz_fetch_block_stock_day_eastmoney(code=list_hangye,start=start,end=end)
data=QA_DataStruct_Stock_day(data.set_index(['date', 'code'], drop=True))
##计算日线级别指标
res_code_gainian_day=cal_macd(data,status=1)
##计算周线级别指标
'''
因为有个别股票处于停盘状态，导致他们读取的第一天和大多数股票不一样，这样在resample到week级别的时候
就会多出一天的数据和大部分数据对不上，所以先弄一个标准的周线date日期然后。
'''
data_week_=data.week.reset_index()
data_week_=data_week_[data_week_.date.isin(index_week)]
data=QA_DataStruct_Stock_day(data_week_.set_index(['date', 'code'], drop=True))
res_code_gainian_week=cal_macd(data,status=1)

res_ls=list(set(res_code_gainian_day).intersection(set(res_code_gainian_week)))
res_code_hangye=list(set(block[block.block_code.isin(res_ls)].code))



########2-8定律选市场上流动性强的股票
daliy_basic=qz.qz_fetch_stock_daily_basic_tushare(code=stock_list,start=end,end=end)
day=qz.qz_fetch_stock_day_tushare(code=stock_list,start=end,end=end)
perc=90
res_code_turnover_rate=daliy_basic[daliy_basic.turnover_rate>np.percentile(daliy_basic.turnover_rate, perc)].code.to_list()
res_code_amount=day[day.amount>np.percentile(day.amount, perc)].code.to_list()
res_code_2_8=list(set(res_code_turnover_rate).union(set(res_code_amount)))  #并集

res_code=list(set(res_code_bar).intersection(set(res_code_gainian)))
res_code=list(set(res_code_2_8).intersection(set(res_code)))
res_code=stock_list_[stock_list_.code.isin(res_code)]












###日线和周线取交集
code_res=list(set(res_day.code[-1:].values[0]).intersection(set(res_week.code[-1:].values[0])))

def cal_macd_day_and_week(data,status=0):
    '''
    选出日线和周线macd同事大于零的code
    支持股票、板块数据和指数

    Parameters
    ----------
    data : adv格式
        日线数据的adv格式..

    Returns
    -------
    最后一天满足条件的list格式的code.

    '''
    index_day_=pd.DataFrame(data.index.levels[0].to_list(),columns=['date']).assign(
                code='000001',
                open=1,
                high=1,
                low=1,
                close=1,
                volume=1,
                amount=1)
    index_day=data.index.levels[0]
    index_week=QA_data_day_resample(index_day_,type_='w').index.levels[0]
    index_month=QA_data_day_resample(index_day_,type_='m').index.levels[0]
    
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
        CROSS_JC_STATUS = QA.CROSS_STATUS(DIFF, DEA)
        CROSS_SC_STATUS = QA.CROSS_STATUS(DEA, DIFF)        
        ZERO = 0
        return pd.DataFrame({'DIFF': DIFF, 
                             'DEA': DEA, 
                             'MACD': MACD, 
                             'CROSS_JC': CROSS_JC, 
                             'CROSS_SC': CROSS_SC, 
                             'CROSS_JC_STATUS': CROSS_JC_STATUS, 
                             'CROSS_SC_STATUS': CROSS_SC_STATUS,                             
                             'ZERO': ZERO})
    ##计算日线级别指标
    data2=data.select_code(data.code[:1])
    
    ind=data.add_func(MACD_JCSC).dropna() #采用默认参数计算macd
    ind_adv =QA.QA_DataStruct_Indicators(ind.dropna())
    #ind.groupby(level=1, sort=False).apply(cross)
    if status==0:
        res_ind=ind[ind['CROSS_JC']==1].reset_index()
#        aa=res_ind[res_ind.code=='000001']
    else:
        res_ind=ind[ind['CROSS_JC_STATUS']==1].reset_index()
    ls=list(set(res_ind.date))
    ls.sort()
    res_=[]
    for i in ls:
        pass  
        ls_=res_ind[res_ind.date==i].code.to_list() 
        res_.append([i,ls_,len(ls_)])
    res_day=pd.DataFrame(res_)  
    res_day.columns=['date','code','amount']  
    
    ##计算周线级别指标
    data_week_=data.week.reset_index()
    data_week_=data_week_[data_week_.date.isin(index_week)]
    data=QA_DataStruct_Stock_day(data_week_.set_index(['date', 'code'], drop=True))
    ind=data.add_func(MACD_JCSC).dropna() #采用默认参数计算macd
    ind_adv =QA.QA_DataStruct_Indicators(ind.dropna())
    res_ind=ind[ind['CROSS_JC_STATUS']==1].reset_index()
    
    ls=list(set(ind.reset_index().date))
    ls.sort()
    res_=[]
    for i in ls:
        pass  
        ls_=res_ind[res_ind.date==i].code.to_list() 
        res_.append([i,ls_,len(ls_)])
    res_week=pd.DataFrame(res_)  
    res_week.columns=['date','code','amount']  
    
    aa=res_week.code[-1:].values[0]
    
    ###日线和周线取交集
    code_res=list(set(res_day.code[-1:].values[0]).intersection(set(res_week.code[-1:].values[0])))
    return code_res


res_code=cal_macd_day_and_week(data,status=1)






close=data.pivot('close')
#aa=date1.reset_index().pivot_table(index='date',columns=['name'],values='close')
def aas(x):
    x=x.dropna()
    x=x/x[0]
    return x



stock_list_=qz.qz_fetch_stock_list_tushare()
stock_list_all=stock_list_.code.to_list()
stock_list_kcb=stock_list_[stock_list_['market']=='科创板'].code.to_list()
stock_list=sorted(list(set(stock_list_all).difference(set(stock_list_kcb))))
data=qz.qz_fetch_stock_day_tushare(code=stock_list,start=start,end=end)
data=QA_DataStruct_Stock_day(data.set_index(['date', 'code'], drop=True)).to_qfq() #将格式转换为qa的ds格式




code_res=list(set(code_res).intersection(set(code_month)))


from QUANTAXIS.QAIndicator.base import *
CLOSE=data.select_code('000001').data.close
EMA(close, 12)
EMA(close, 12)
short=12
long=26
mid=9
DIF = EMA(CLOSE, short)-EMA(CLOSE, long)
DEA = EMA(DIF, mid)
MACD = (DIF-DEA)*2
data_week=data.week
data_week_adv=QA_DataStruct_Stock_day(data_week)
data_week_macd=data_week_adv.add_func(QA.QA_indicator_MACD) #采用默认参数计算macd

CROSS_STATUS
buy=ind[QA.CROSS_STATUS(ind.MA5, ind.MA20)==1].reset_index()['date'].tolist()
sell=ind[QA.CROSS(ind.MA20, ind.MA5)==1].reset_index()['date'].tolist() 
    
    
data2=data.select_code('000001')
data2.week

data2.resample('w')


####月线数据有问题  个别月会跳过  先弄到周线级别
delta=1200
end=datetime.datetime.now().strftime("%Y-%m-%d")
start=(datetime.date.today() - datetime.timedelta(days=delta)).strftime("%Y-%m-%d")


stock_list=QA.QA_fetch_stock_list().code.to_list()
data=QA.QA_fetch_stock_day_adv(code=stock_list[:30],start=start,end=end)

data_month=data.month
ls=list(set(data_month.reset_index().date))
ls.sort()
