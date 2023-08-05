# -*- coding: utf-8 -*-
"""
Created on Thu Feb  7 22:06:09 2019

@author: ZSL
"""
import pandas as pd
import numpy as np 
import tushare as ts 
import time
import copy
import datetime
import QUANTAXIS as QA
import quantzsl as qz
def qz_data_tick_resample_1min(res2,periodS = '1min'):
    """
    tick数据采样成1min数据
    Arguments:
        res {[type]} -- dic
        
    Returns:
        kdata[type] -- dic
    输入返回均为字典格式，字典里包含o l g l v a 六个df
    """             
    #res2=self.data['stock_cn_tick_real']
    res=copy.deepcopy(res2)   
    try:
        for i in res:
            pass
            res[i]=res[i].set_index(pd.to_datetime(res[i].reset_index()['datetime'])) 
    except:
        pass
            
    kdata={}  
    kdata1_open=res['close'][datetime.time(9,25):datetime.time(11,31)].resample(periodS).first()
    kdata1_high=res['close'][datetime.time(9,25):datetime.time(11,31)].resample(periodS).max()
    kdata1_low=res['close'][datetime.time(9,25):datetime.time(11,31)].resample(periodS).min()
    kdata1_close=res['close'][datetime.time(9,25):datetime.time(11,31)].resample(periodS).last()
    try:
        kdata1_vol=res['cur_vol'][datetime.time(9,25):datetime.time(11,31)].resample(periodS).sum()            
        kdata1_amount=res['amount'][datetime.time(9,25):datetime.time(11,31)].resample(periodS).sum() 
    except:
        pass           
                
    kdata2_open=res['close'][datetime.time(13,0):datetime.time(15,1)].resample(periodS).first()
    kdata2_high=res['close'][datetime.time(13,0):datetime.time(15,1)].resample(periodS).max()
    kdata2_low=res['close'][datetime.time(13,0):datetime.time(15,1)].resample(periodS).min()
    kdata2_close=res['close'][datetime.time(13,0):datetime.time(15,1)].resample(periodS).last()
    try:
        kdata2_vol=res['cur_vol'][datetime.time(13,0):datetime.time(15,1)].resample(periodS).sum()            
        kdata2_amount=res['amount'][datetime.time(13,0):datetime.time(15,1)].resample(periodS).sum() 
    except:
        pass     
           

    kdata['open']=kdata1_open.append(kdata2_open)
    kdata['high']=kdata1_high.append(kdata2_high)
    kdata['low']= kdata1_low.append(kdata2_low)
    kdata['close']=kdata1_close.append(kdata2_close)
    try:
        kdata['vol'] =kdata1_vol.append(kdata2_vol)    
        kdata['amount']=kdata1_amount.append(kdata2_amount)
    except:
        pass     

    return kdata  
  
def qz_data_1min_resample_nmin(res2,periodS = 5): 
    """
    1min数据采样成nmin数据，限于60分钟及以内
    Arguments:
        res {[type]} -- dic  一分钟数据
        
    Returns:
        kdata[type] -- dic   n分钟数据
    输入返回均为字典格式，字典里包含o l g l v a 六个df
    """                        
    #res2=self.data['stock_cn_1min']
    periodS = str(periodS)+'min'
    res=copy.deepcopy(res2)  
    for i in res:
        pass
        df_=pd.DataFrame(np.vectorize(lambda s: s.strftime('%Y-%m-%d'))(res[i].index.to_pydatetime())).set_index(res[i].index)
        res[i]=res[i].assign(date=df_)        
#        for i in res:
#            pass
#            res[i]=res[i].drop('date',axis=1)
    #res=self.data['stock_data_1min']
#        for i in res:
#            date=pd.DataFrame(pd.DataFrame(res[i].index).apply(lambda x: str(x)[4:14],axis=1)).set_index(res[i].index)
#            res[i].assign(date=date)
    t=time.time()
    resx = pd.DataFrame()
    _dates=set(res['close']['date'])
    kdata_={} 
    kdata={}     
    kdata_open= pd.DataFrame()             
    kdata_high= pd.DataFrame()
    kdata_low= pd.DataFrame()             
    kdata_close= pd.DataFrame()
    kdata_vol= pd.DataFrame()             
    kdata_amount= pd.DataFrame()
    
    for date in sorted(list(_dates)):  
        pass                                        
        kdata1_open=res['close'].loc[res['close'].date == date].drop('date',axis=1)[datetime.time(9,25):datetime.time(11,31)].resample(periodS,closed='right',base=30,loffset=periodS).first()
        kdata1_high=res['close'].loc[res['close'].date == date].drop('date',axis=1)[datetime.time(9,25):datetime.time(11,31)].resample(periodS,closed='right',base=30,loffset=periodS).max()
        kdata1_low=res['close'].loc[res['close'].date == date].drop('date',axis=1)[datetime.time(9,25):datetime.time(11,31)].resample(periodS,closed='right',base=30,loffset=periodS).min()
        kdata1_close=res['close'].loc[res['close'].date == date].drop('date',axis=1)[datetime.time(9,25):datetime.time(11,31)].resample(periodS,closed='right',base=30,loffset=periodS).last()
        try:
            kdata1_vol=res['vol'].loc[res['vol'].date == date].drop('date',axis=1)[datetime.time(9,25):datetime.time(11,31)].resample(periodS,closed='right',base=30,loffset=periodS).sum()            
            kdata1_amount=res['amount'].loc[res['amount'].date == date].drop('date',axis=1)[datetime.time(9,25):datetime.time(11,31)].resample(periodS,closed='right',base=30,loffset=periodS).sum()            
    
        except:
            pass                    
        kdata2_open=res['close'].loc[res['close'].date == date].drop('date',axis=1)[datetime.time(13,0):datetime.time(15,1)].resample(periodS,closed='right',loffset=periodS).first()
        kdata2_high=res['close'].loc[res['close'].date == date].drop('date',axis=1)[datetime.time(13,0):datetime.time(15,1)].resample(periodS,closed='right',loffset=periodS).max()
        kdata2_low=res['close'].loc[res['close'].date == date].drop('date',axis=1)[datetime.time(13,0):datetime.time(15,1)].resample(periodS,closed='right',loffset=periodS).min()
        kdata2_close=res['close'].loc[res['close'].date == date].drop('date',axis=1)[datetime.time(13,0):datetime.time(15,1)].resample(periodS,closed='right',loffset=periodS).last()
        try:
            kdata2_vol=res['vol'].loc[res['vol'].date == date].drop('date',axis=1)[datetime.time(13,0):datetime.time(15,1)].resample(periodS,closed='right',loffset=periodS).sum()            
            kdata2_amount=res['amount'].loc[res['amount'].date == date].drop('date',axis=1)[datetime.time(13,0):datetime.time(15,1)].resample(periodS,closed='right',loffset=periodS).sum()            
        except:
            pass         
        kdata_open=kdata_open.append(kdata1_open).append(kdata2_open)
        kdata_high=kdata_high.append(kdata1_high).append(kdata2_high)
        kdata_low = kdata_low.append(kdata1_low).append(kdata2_low)
        kdata_close =kdata_close.append(kdata1_close).append(kdata2_close)
        try:
            kdata_vol=kdata_vol.append(kdata1_vol).append(kdata2_vol)    
            kdata_amount=kdata_amount.append(kdata1_amount).append(kdata2_amount)        
        except:
            pass         

        
    kdata_['open'] =kdata_open
    kdata_['high'] =kdata_high
    kdata_['low'] = kdata_low
    kdata_['close'] =kdata_close
    try:
        kdata_['vol'] =kdata_vol   
        kdata_['amount'] =kdata_amount 
    except:
        pass 
    
    for i in res:
        pass  
        kdata[i]=kdata_[i]
    #print(time.time()-t)
    return kdata 
def qz_data_min_resample_day(res2): 
    """
    min数据采样成日线数据
    Arguments:
        res {[type]} -- dic  分钟数据
        
    Returns:
        kdata[type] -- dic   日线数据
    输入返回均为字典格式，字典里包含o l g l v a 六个df
    """                        
    #res2=self.data['stock_cn_5min']
    periodS = 'd'
    res=copy.deepcopy(res2)
    for i in res:
        pass
        df_=pd.DataFrame(np.vectorize(lambda s: s.strftime('%Y-%m-%d'))(res[i].index.to_pydatetime())).set_index(res[i].index)
        res[i]=res[i].assign(date=df_)        
#        for i in res:
#            pass
#            res[i]=res[i].drop('date',axis=1)
    #res=self.data['stock_data_1min']
#        for i in res:
#            date=pd.DataFrame(pd.DataFrame(res[i].index).apply(lambda x: str(x)[4:14],axis=1)).set_index(res[i].index)
#            res[i].assign(date=date)
    t=time.time()
    resx = pd.DataFrame()
    _dates=set(res['close']['date'])
    kdata={} 
    kdata_={}     
    kdata_open= pd.DataFrame()             
    kdata_high= pd.DataFrame()
    kdata_low= pd.DataFrame()             
    kdata_close= pd.DataFrame()
    kdata_vol= pd.DataFrame()             
    kdata_amount= pd.DataFrame()
    
    for date in sorted(list(_dates)):  
        pass                                        
        kdata1_open=res['open'].loc[res['close'].date == date].drop('date',axis=1).resample(periodS).first()
        kdata1_high=res['high'].loc[res['close'].date == date].drop('date',axis=1).resample(periodS).max()
        kdata1_low=res['low'].loc[res['close'].date == date].drop('date',axis=1).resample(periodS).min()
        kdata1_close=res['close'].loc[res['close'].date == date].drop('date',axis=1).resample(periodS).last()
        try:
            kdata1_vol=res['vol'].loc[res['vol'].date == date].drop('date',axis=1).resample(periodS).sum()            
            kdata1_amount=res['amount'].loc[res['amount'].date == date].drop('date',axis=1).resample(periodS).sum()            
        except:
            pass                          
        kdata_open=kdata_open.append(kdata1_open)
        kdata_high=kdata_high.append(kdata1_high)
        kdata_low = kdata_low.append(kdata1_low)
        kdata_close =kdata_close.append(kdata1_close)
        try:
            kdata_vol=kdata_vol.append(kdata1_vol) 
            kdata_amount=kdata_amount.append(kdata1_amount)
        except:
            pass         

        
    kdata_['open'] =kdata_open
    kdata_['high'] =kdata_high
    kdata_['low'] = kdata_low
    kdata_['close'] =kdata_close
    try:
       kdata_['vol'] =kdata_vol   
       kdata_['amount'] =kdata_amount
    except:
        pass    
    for i in res:
        pass  
        kdata[i]=kdata_[i]     
    #print(time.time()-t)
    return kdata 
if __name__=='__main__':
    stock_list=QZ.QA_fetch_stock_list_pg()
    stock_list=stock_list[stock_list['list_status']=='L']
    stock_list=stock_list.set_index(stock_list.symbol)  
    stock_code=stock_list['symbol'].tolist() #导入股票列表              
    stock_min1=QA.QAFetch.QAQuery.QA_fetch_stock_min(stock_code[:50], '2019-01-02', '2019-01-04', 'pd', frequence='1min')
    stock_min2=stock_min1[['code','datetime','open','high','low','close','amount','vol']]
    
#        stock_min1['date']=pd.DataFrame(pd.DataFrame['datetime'].apply(lambda x: str(x)[4:14],axis=1)).set_index(res[i].index)
    
    stock_min2.rename(columns={'datetime': 'trade_date'}, inplace=True)
    stock_min3=stock_min2.set_index(['trade_date', 'code'], drop=True)#处理日线数据
    stock_data_min=QZ.QZ_data_pivot(stock_min3)#将日线数据切片
    res_5min=QZ_data_1min_resample_nmin(res_1min,5)
    res_30min=QZ_data_1min_resample_nmin(res_1min,30) 
    
    res_60min=QZ_data_1min_resample_nmin(res_1min,60) 
    
    #res_120min=QZ_data_1min_resample_nmin(res_1min,120)  最多到60min，120min的不行
        