# -*- coding: utf-8 -*-
"""
Created on Wed Jan 13 22:12:03 2021

@author: ZSL
"""

import QUANTAXIS as QA
import quantzsl as qz
import tushare as ts
import numpy as np
import pandas as pd
#import talib
import time
import datetime
from QUANTAXIS.QAUtil.QAParameter import (DATASOURCE, FREQUENCE, MARKET_TYPE, OUTPUT_FORMAT)
import matplotlib.patches as mpatches
import matplotlib.pyplot as plt                                         
import matplotlib.ticker as ticker
#import matplotlib.finance as mpf
#from mpl_finance import candlestick_ochl
from matplotlib.pylab import date2num
class qz_analysis_block():
    def __init__(self, code=[], name=None, start=None, end=None,data=None,methods='总市值' , frequence=FREQUENCE.DAY,  *args, **kwargs):
        self.code = code 
        self.start = start
        self.end = end
        self.frequence = frequence
        self.name = name
        self.methods=methods
        try:
            if 'datetime' in data.columns:
                self.market_value=data.set_index(['datetime','code']).drop_duplicates().sort_index() 
            else:
                self.market_value=data.set_index(['date','code']).drop_duplicates().sort_index()
        except:
            pass
        # if data==None: #没有传入数据则自己读取
        #     pass
            # stock_list=qz.qz_fetch_stock_list_tushare()
            # stock_list=stock_list[stock_list['list_status']=='L']
            # self.stock_list=stock_list.set_index(stock_list.code)  
            # code=stock_list.code.to_list()
            # #self.stock_code=self.stock_list['symbol'].tolist()#导入股票列表   
            # date_today=datetime.date.today().strftime("%Y-%m-%d")#结束日期 今天
            # date_last_trade=QA.QAUtil.QADate_trade.QA_util_get_real_date(date_today, towards=-1)  #返回今天之前的最近一个交易日
            # date_trade_300=QA.QAUtil.QADate_trade.QA_util_get_last_day(date_last_trade,100) #返回前3个交易日
            # stock_data=qz.qz_fetch_stock_day_tushare(code=code,start=date_trade_300,end=date_today)
            # daliy_basic=qz.qz_fetch_stock_daily_basic_tushare(code=code,start=date_trade_300,end=date_today)
            # self.stock_data=stock_data.assign(
            #     total_mv=daliy_basic.total_mv,
            #     circ_mv=daliy_basic.circ_mv,
            #     total_share=daliy_basic.total_share,
            #     float_share=daliy_basic.float_share,
            #     free_share=daliy_basic.free_share,
            #     pe=daliy_basic.pe,
            #     pe_ttm=daliy_basic.pe_ttm,
            #     turnover_rate_f=daliy_basic.turnover_rate_f,
            #     turnover_rate=daliy_basic.turnover_rate,
            #     )
            # self.market_value=self.stock_data.set_index(['date','code']).drop_duplicates().sort_index()             
        # else:
        #     pass
            # self.market_value=self.data.set_index(['date','code']).drop_duplicates().sort_index()   
                                          
    def block_index(self, methods='总市值',iterm='close'):    
        if methods == '总市值':
            res = self.market_value.groupby(level=0).apply(
                lambda x: np.average(x[iterm], weights=x.total_mv))
        elif methods == '流通市值':
            res = self.market_value.groupby(level=0).apply(
                lambda x: np.average(x[iterm], weights=x.circ_mv))
        elif methods == '简单平均':
            res = self.market_value.groupby(level=0).apply(
                lambda x: np.average(x[iterm]))
        elif methods == '成交量':
            res = self.market_value.groupby(level=0).apply(
                lambda x: np.average(x[iterm], weights=x.volume))
        elif methods == '总股本':
            res = self.market_value.groupby(level=0).apply(
                lambda x: np.average(x[iterm], weights=x.total_share))            
        elif methods == '流通股本':
            res = self.market_value.groupby(level=0).apply(
                lambda x: np.average(x[iterm], weights=x.float_share))  
        elif methods == '自由流通股本':
            res = self.market_value.groupby(level=0).apply(
                lambda x: np.average(x[iterm], weights=x.free_share))
        elif methods == '市盈率':
            res = self.market_value.groupby(level=0).apply(
                lambda x: np.average(x[iterm], weights=x.pe))
        elif methods == '市盈率_ttm':
            res = self.market_value.groupby(level=0).apply(
                lambda x: np.average(x[iterm], weights=x.pe_ttm))
        elif methods == '换手率（自由流通股）':
            res = self.market_value.groupby(level=0).apply(
                lambda x: np.average(x[iterm], weights=x.turnover_rate_f))            
        elif methods == '换手率':
            res = self.market_value.groupby(level=0).apply(
                lambda x: np.average(x[iterm], weights=x.turnover_rate))                         
        else:
            res = self.market_value.groupby(level=0).apply(
                lambda x: np.average(x[iterm], weights=x.shares))
            print(
                '错误记权方法')
        return res/res.iloc[0]*1000

    @property
    def data_k(self):
        methods=self.methods
        res=pd.DataFrame()
        list_k=['open','close','high','low','volume']
        for i in list_k:
            res[i]=self.block_index(methods=methods,iterm=i)            
        return res.reset_index()
    @property    
    def close(self):
        methods=self.methods
        res=pd.DataFrame()
        res['close']=self.block_index(methods=methods,iterm='close')  
        return res

            
    def plot_k(self,length=14, height=12):
        def date_to_num(dates):
            num_time = []
            for date in dates:
                date_time =date# datetime.datetime.strptime(date,'%Y-%m-%d')
                num_date = date2num(date_time)
                num_time.append(num_date)
            return pd.DataFrame(num_time)
        res=pd.DataFrame()        
        res['date']=date_to_num(self.data_k['date'])[0]  
        res_=self.data_k
        res['open']=res_['open']
        res['close']=res_['close']  
        res['high']=res_['high']
        res['low']=res_['low']        
        plt.rcParams["font.sans-serif"]='SimHei'
        #解决负号无法正常显示问题
        plt.rcParams["axes.unicode_minus"]= False
        #设置为矢量图
     #   %config InlineBackend.figure_format = 'svg'        
        plt.style.use('ggplot')       
        fig = plt.figure(figsize=(length, height))
        plt.title('指数', fontsize=25)         
        ax = fig.add_subplot(1, 1, 1) 
        date_tickers=self.data_k.index.values  
        aa=res.as_matrix()                    
        weekday_quotes=[tuple([i]+list(quote[1:])) for i,quote in enumerate(res.values)]        
        def format_date(x,pos=None):
            if x<0 or x>len(date_tickers)-1:
                return ''
            return date_tickers[int(x)]
 

        # fig.autofmt_xdate()
         
        candlestick_ochl(ax,aa,colordown='#53c156', colorup='#ff1717',width=0.2)
        #ax.xaxis.set_major_locator(ticker.MultipleLocator(6))
        #ax.xaxis.set_major_formatter(ticker.FuncFormatter(format_date))
        ax.grid(True)
        ax.xaxis_date ()
        plt.show()    
    def plot_compare(self, mes=['成交量','流通股本','总股本','简单平均'],length=14, height=12):
        """
        资金曲线叠加图
        """
        #解决中文乱码问题
        res=pd.DataFrame()
        for i in mes:
            res[i]=self.block_index(i)   
        res.index=pd.to_datetime(res.index)
        plt.rcParams["font.sans-serif"]='SimHei'
        #解决负号无法正常显示问题
        plt.rcParams["axes.unicode_minus"]= False
        #设置为矢量图
     #   %config InlineBackend.figure_format = 'svg'        
        plt.style.use('ggplot')       
        fig = plt.figure(figsize=(length, height))
        plt.title('指数', fontsize=25)         
        ax = fig.add_subplot(1, 1, 1)        
        #plt.subplot(211)
        N = len(res.index)
        def format_date(x, pos=None):
            # 保证下标不越界,很重要,越界会导致最终plot坐标轴label无显示          
            thisind = np.clip(int(x), 0, N-1)
            #print(x)
            return res.index[thisind].strftime('%Y-%m-%d') #%H:%M')
        for i in res:
            pass
            ax.plot(list(res[i]))#.plot()        
            #ax.plot(list(res.index),res[i])#.plot()         
        plt.legend(mes, loc=2,fontsize=15)
        #plt.xaxis.set_major_locator(ticker.MultipleLocator(5))
        ax.xaxis.set_major_locator(ticker.MultipleLocator(6))        
        ax.xaxis.set_major_formatter(ticker.FuncFormatter(format_date))        
        plt.show()       

## 设置主刻度 次刻度
#x_major_locator = MultipleLocator(1) #将x轴主刻度标签设置为1的倍数
#ax1.xaxis.set_major_locator(x_major_locator)
#x_major_formatter = FormatStrFormatter('%.0f') #设置x轴标签文本的格式
#ax1.xaxis.set_major_formatter(x_major_formatter)
#x_minor_locator = MultipleLocator(0.5) #将x轴次刻度标签设置为0.5的倍数ax.xaxis.set_minor_locator(xminorLocator)
#ax1.xaxis.set_minor_locator(x_minor_locator)


if __name__ == "__main__":
    pro=qz.qz_ts_pro()
    concept = pro.concept(src='ts')    
#    res_con={}
#    for i in concept['code']:
#        pass
#        res_con[i] = pro.concept_detail(id=i, fields='id,concept_name,ts_code,name,in_date,out_date')
#    df = pro.concept_detail(ts_code = '600848.SH') #获取某个股票 属于哪个版块 
    id_=concept[concept['name']=='5G'].code.values[0]
    code=pro.concept_detail(id=id_, fields='id,concept_name,ts_code,name,in_date,out_date')['ts_code'].apply(lambda x:x[:6]).tolist()    
    date_today=datetime.date.today().strftime("%Y-%m-%d")#结束日期 今天
    date_last_trade=QA.QAUtil.QADate_trade.QA_util_get_real_date(date_today, towards=-1)  #返回今天之前的最近一个交易日
    date_trade_300=QA.QAUtil.QADate_trade.QA_util_get_last_day(date_last_trade,100) #返回前3个交易日
    stock_data=qz.qz_fetch_stock_day_tushare(code=code,start=date_trade_300,end=date_today)
    daliy_basic=qz.qz_fetch_stock_daily_basic_tushare(code=code,start=date_trade_300,end=date_today)
    stock_data=stock_data.assign(
        total_mv=daliy_basic.total_mv,
        circ_mv=daliy_basic.circ_mv,
        total_share=daliy_basic.total_share,
        float_share=daliy_basic.float_share,
        free_share=daliy_basic.free_share,
        pe=daliy_basic.pe,
        pe_ttm=daliy_basic.pe_ttm,
        turnover_rate_f=daliy_basic.turnover_rate_f,
        turnover_rate=daliy_basic.turnover_rate,
        )
    stock_data.set_index(['date','code']).drop_duplicates().sort_index()    
    self=qz_analysis_block(code=code,start=date_trade_300,end=date_last_trade,data=stock_data)
    close=self.close
    self.plot_compare()
    self.plot_k()  
    self.market_value
#    
#    aaa=pd.DataFrame()
#    aaa['成交量']=self.block_index('成交量')
#    aaa['流通股本']=self.block_index('流通股本')
#    aaa['总股本']=self.block_index('总股本')    
#
#aaa.plot()
#    id_=concept[concept['name']=='养鸡'].code.values[0]
#    code=pro.concept_detail(id=id_, fields='id,concept_name,ts_code,name,in_date,out_date')['ts_code'].apply(lambda x:x[:6]).tolist()    
#
#
#index = stock_data2.index.remove_unused_levels()
#        try:
#            return index.levels[0] if 'date' in stock_data2.index.names else list(
#                set(self.datetime.date)
#            )
#
#
#aaa=pd.DataFrame()
#aaa['vol']=ana.block_index('lv')
#aaa['close']=ana.block_index('close')
#aaa['volume']=ana.block_index('volume')
#
#avalue.reset_index()
#
#
#
#con_list=['000001,000002,000004']
#
#
   