# -*- coding: utf-8 -*-
"""
Created on Mon Feb 17 14:10:18 2020

@author: ZSL
"""

import pandas as pd
import numpy as np 
import tushare as ts 
import QUANTAXIS as QA
import quantzsl as qz
import time
import json
import pymongo
import os
import glob
import datetime
import threading
import warnings
from QUANTAXIS.QAUtil.QADate_trade import (QA_util_get_real_date,QA_util_get_last_day,
                                          QA_util_get_next_day,QA_util_format_date2str)
from QUANTAXIS.QAUtil.QARandom import QA_util_random_with_topic
from QUANTAXIS.QAUtil.QADate import (QA_util_datetime_to_strdate,QA_util_pands_timestamp_to_date,
                                    QA_util_pands_timestamp_to_datetime,QA_util_datetime_to_strdatetime)
from QUANTAXIS.QAUtil.QADate_trade import (QA_util_if_tradetime,QA_util_if_trade)
from QUANTAXIS.QAUtil import DATABASE
from QUANTAXIS.QAARP.QAAccount import QA_Account
warnings.filterwarnings("ignore")
from QUANTAXIS.QAUtil.QAParameter import (FREQUENCE, MARKET_TYPE,
                                          OUTPUT_FORMAT)
STOCK_CN=MARKET_TYPE.STOCK_CN
INDEX_CN=MARKET_TYPE.INDEX_CN
frequence_day_=[FREQUENCE.YEAR,FREQUENCE.MONTH,FREQUENCE.WEEK,FREQUENCE.DAY]
frequence_min_=[FREQUENCE.ONE_MIN,FREQUENCE.FIVE_MIN,FREQUENCE.FIFTEEN_MIN,
                FREQUENCE.THIRTY_MIN,FREQUENCE.SIXTY_MIN]
from QUANTAXIS.QAData import (
                                QA_DataStruct_Stock_min,
                                QA_DataStruct_Stock_day
                                )
from QUANTAXIS.QAData.data_resample import (
    QA_data_day_resample,#day  to  week
    QA_data_min_to_day,#min to day
    QA_data_min_resample,#min to min
)
from QUANTAXIS.QAIndicator.base import *
import tushare as ts
from quantzsl.qz_util.qz_util import (qz_util_change_len,)

try:                                      
    import puppet
except:
    pass
        
class stock_trade_base():
    '''
    实盘基类，支持股票、指数、etf的单标的和多标的
    直接继承然后修改cal_signal函数即可，如有需要也可以修改on_bar函数
    '''    
    def __init__(self,
                code=None,
                frequence='day',
                market_type=QA.QAUtil.QAParameter.MARKET_TYPE.STOCK_CN,
                max_hold=5,
                start=None,
                para=[5,20,30],
                model='trade',
                days_in_advance=260,
                account_cookie='日线趋势'
                ):
        self.max_hold=max_hold
        self.para=para
        self.frequence=frequence
        self.code=code if code!=None else qz.qz_fetch_stock_list_tushare().code.to_list()    
        self.model=model 
        self.market_type=market_type
        self.account_cookie=account_cookie
#        self.signal_收盘=1
#        self.end=datetime.datetime.now().strftime("%Y-%m-%d")
#        self.start=start if start!=None else (datetime.date.today() - datetime.timedelta(days=20)).strftime("%Y-%m-%d")
        self.buy={}
        self.sell={}
        self.days_in_advance=days_in_advance
        if frequence==QA.FREQUENCE.SIXTY_MIN:
            self.frequence_=['1030','1128','1400','1453']
        elif frequence==QA.FREQUENCE.THIRTY_MIN:
            self.frequence_=['1000','1030','1100','1128','1330','1400','1430','1453'] 
        elif frequence==QA.FREQUENCE.FIFTEEN_MIN:
            self.frequence_=['0945','1000','1015','1030','1045','1100','1115','1128',
                             '1315','1330','1345','1400','1415','1430','1445','1453']  
        elif frequence==QA.FREQUENCE.FIVE_MIN:
            self.frequence_=['1445'] 
        elif frequence==QA.FREQUENCE.DAY:
            self.frequence_=['1445']             
    def on_bar(self):  #单周期 onbar模板（单股票、多股票）
        now=datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        print(now+' 正在计算买卖指标。。。')          
        data=self.data
        aa=data.data
        para=self.para
        self.len_data=260 #增量模式下 数据存储的最大长度，根据计算需要取值 默认为250
        frequence=self.frequence
        #AC=self.account
        #dataframe=data.data
        current_day=pd.to_datetime(datetime.datetime.now().strftime("%Y-%m-%d"))#QA_util_to_datetime(self.date)
        stock_list=qz.qz_fetch_stock_list_tushare()
        #剔除新股，上市大于list_date天
        
        list_date=200
#        list_date_=(current_day - datetime.timedelta(days=list_date)).strftime("%Y-%m-%d")
#        stock_list=stock_list[stock_list['list_date']<list_date_]
#        stock_list=stock_list[~stock_list['name'].str.contains('ST')] 
#        code=stock_list.code.to_list()
#        data=self.data.select_code(code)
        code_zhangting=data.data[data.close==data.high_limit].reset_index()[['date','code']]
        code_xingu=[]
        for i in code_zhangting.date:
            pass
            list_date_=(i - datetime.timedelta(days=list_date)).strftime("%Y-%m-%d")
            code_=stock_list[stock_list['list_date']>list_date_].code.to_list()
            for j in code_:
                code_xingu.append([i,j])
        code_xingu=pd.DataFrame(code_xingu)
        code_xingu.columns=['date','code']  
#        code_=stock_list[~stock_list['name'].str.contains('ST')].code.to_list()
            
        def 均线速度(DataFrame):
            '''
            计算波动率
            '''
            #DataFrame=data_min.select_code('000004').data
            HIGH = DataFrame.high
            LOW = DataFrame.low
            CLOSE = DataFrame.close
            OPEN = DataFrame.open
            C=CLOSE
            list_=[5,13,21,34,55,89,144,233]
            res=pd.DataFrame(C>C)+0
            for i in list_:
                res+=pd.DataFrame(C>MA(C,i))+0
            均线速度1=(MA(C,13)-REF(MA(C,13),1))/REF(MA(C,13),1)*100
            res_=(res>=7)+0
           
            均线速度2=pd.DataFrame(均线速度1)
              
            return 均线速度2*res_  


        #data2=data.data
        ind_min=data.add_func(均线速度)
        ind_min2=ind_min.reset_index().pivot_table(index='date',columns=['code'],values='close')
        ind_=[]
        for i in ind_min2.index:
            pass
            ls=ind_min2.loc[i,:]>0
            ls2=pd.DataFrame(ind_min2.loc[i,:][ls])
            ls3=ls2.rank().sort_values(by=ls2.columns[0]).reset_index().code.to_list()
            ls4=code_zhangting[code_zhangting['date']==i].code.to_list() #去掉涨停的股票
            ls5=code_xingu[code_xingu['date']==i].code.to_list() #去掉涨停的股票
            ls3=list(set(ls3).difference(set(ls4)))
            ls3=list(set(ls3).difference(set(ls5)))[:20]            
            ind_.append([i,ls3])
        ls2=pd.DataFrame(ind_) 
        ls2.columns=['date','code']
        
        hold_=[]
        for i in ls2.index:
            pass
            for j in ls2.loc[i,:].code:
                pass
                hold_.append([ls2.loc[i,:].date,j])
        hold=pd.DataFrame(hold_)
        try:
            hold.columns=['date','code']  
        except:
            pass
        self.hold=hold        
        #hold=self.hold
        #code_to_buy=hold[hold['date']==hold.date[-1:].values[0]].code.to_list()      
        code_to_buy=hold[hold['date']==current_day].code.to_list()      
        
        res=stock_list[stock_list.code.isin(code_to_buy)][['code','name']].reset_index().drop('index',axis=1)
        res=res.rename(columns={"name": "namea"})
        res['price']=self.data_new.select_code(code_to_buy).data.reset_index()['close']
        res['changepercent']=self.data_realtime[self.data_realtime.code.isin(code_to_buy)].reset_index().changepercent.apply(lambda x:round(x,2))
        title ='下单提醒，策略:{}'.format(self.account_cookie) #消息标题，最长为256，必填。
        #消息内容，最长64Kb，可空，支持MarkDown。
        res_buy_stock=""
        for i in res.index:
            pass
            #print(i)
            ls=res.loc[i,:]
            res_buy_stock=res_buy_stock+">-{}--{}--{}--{}--{}\n\n".format(qz_util_change_len(i+1),
                                           qz_util_change_len(ls.code,6),
                                           qz_util_change_len(ls.namea,8),
                                           qz_util_change_len(ls.price,6),
                                           qz_util_change_len(str(ls.changepercent)+'%'),3)
        content ="### 策略：日线趋势 \n\n"+\
              "### 下单提醒：买入\n\n"+\
              ">**序号**---**代码**------**名称**-----**价格**---**涨跌幅** \n\n"+res_buy_stock     
        data_ = {"title":title,"text":content}
        data__ = {"msgtype": "markdown","markdown": data_}    
        qz.qz_send_dingding(data__,'股海捞金')
        now=datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        print(now+' 买卖信号发送钉钉完成。。。')     

                    
    def update_data(self):
        
        now=datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        print(now+' 正在更新盘中数据。。。')        
        code=self.code
        data_=ts.get_today_all()
        self.data_realtime=data_
        data=data_[['code','trade','open','high','low','volume','amount']]
        data['date']=pd.to_datetime(datetime.datetime.now().strftime("%Y-%m-%d"))
        data.code.apply(str)
        data.rename(columns={'trade':'close'}, inplace=True)
        data=data[data.code.isin(code)]
        data_new=QA_DataStruct_Stock_day(data.set_index(['date', 'code'], drop=True),if_fq='qfq')  
        code_new=data_new.code.to_list()
        code_old=self.data.code.to_list()
        code_=list(set(code_old).intersection(set(code_new)))
        self.data_new=data_new.select_code(code_)
        #self.data=self.data.select_code(code_)
        self.data=self.data_old.__add__(data_new)
        now=datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        print(now+' 更新盘中数据完成。。。')           
#        code=self.code
#        #code='159915'
#        end=datetime.datetime.now().strftime("%Y-%m-%d")#'2021-02-19'
#        start=end      
#        for i in code:
#            pass
#            try:
#                res=pd.DataFrame()
#                res_=QA.QAFetch.QATdx.QA_fetch_get_stock_day(code=i, 
#                                                                 start_date=start,
#                                                                 end_date=end,
#                                                                 frequence=self.frequence)
#    #            res=pd.concat([res,res_],axis=0)
#    #            return res 
#                #res=data_()
#                res_.date=pd.to_datetime(res_.date)
#                data_new=QA_DataStruct_Stock_day(res_.set_index(['date', 'code'], drop=True),if_fq='qfq')        
#                self.data=self.data_old.__add__(data_new)
#            except:
#                pass
    def hold(self):
        buy=self.buy
        sell=self.sell        
        if int(dt.datetime.now().strftime("%H%M"))==1500 and self.signal_hold==1:
            try:    
                res=[]
                for i in self.code:
                    pass
                    if sell[sell['code']==i]['datetime'].tolist()[-1]<buy[buy['code']==i]['datetime'].tolist()[-1]:
                        res.append('持仓')
                    else:
                        res.append('空仓')                        
                title ='持仓，策略:{}'.format(self.account_cookie) #消息标题，最长为256，必填。
                #消息内容，最长64Kb，可空，支持MarkDown。
                content = "{}持仓情况分别为{}".format(self.code,res)
                data_ = {"title":title,"text":content}
                data = {"msgtype": "markdown","markdown": data_}    
                qz.qz_send_dingding(data)
                self.signal_hold=self.signal_hold-1  
            except:
                pass                 

        
                                    
    def if_trade_time(self):
        _time=datetime.datetime.now()
        _time = datetime.datetime.strptime(str(_time)[0:19], '%Y-%m-%d %H:%M:%S')
        if QA_util_if_trade(str(_time.date())[0:10]):
            if _time.hour in [10, 13, 14]:
                return True
            elif _time.hour in [
                    9
            ] and _time.minute >= 15:  # 修改成9:15 加入 9:15-9:30的盘前竞价时间
                return True
            elif _time.hour in [11] and _time.minute <= 30:
                return True
            else:
                return False
        else:
            return False

        
    def load_data(self):  
        now=datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        print(now+' 正在载入盘前数据。。。')
        self.end=datetime.datetime.now().strftime("%Y-%m-%d")
        self.start=(datetime.date.today() - datetime.timedelta(days=self.days_in_advance)).strftime("%Y-%m-%d")
                      
        data = QA.QA_quotation(self.code, self.start, self.end, source=QA.DATASOURCE.MONGO,
                               frequence=self.frequence, market=self.market_type, output=QA.OUTPUT_FORMAT.DATASTRUCT)        
        try:
            self.data=data.to_qfq()
        except:
            self.data=data
        self.data_old=self.data
        now=datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        print(now+' 载入盘前数据完成。。。')  
        
    def load_account(self):
        '''
        载入账号数据
        '''
        self.account = puppet.Account(title='')          
    def update_data_hexo():
        '''
        更新数据,需要先运行qz_hexo文件 实时储存数据，但是由于天总的数据只包含股票的 没有指数的数据 
        而本人后边又想做etf 所以该接口 实际用处不大，建议采用新浪接口
        '''
#        code=['000001']
#        aa=QA.QA_fetch_stock_min_adv(code, '2021-02-19','2021-02-19',frequence='5min')
#        aaa=QA.QA_fetch_stock_min(code,'2021-01-19 09:30:00','2021-01-19  15:00:00',format='pd',
#    frequence='5min')
        res=self.fetch_get_realtime_hexo(code=self.code,type_='5min')
        res.datetime=pd.to_datetime(res.datetime)
        res=res[res['datetime']>pd.to_datetime(datetime.datetime.now().strftime("%Y-%m-%d"))]
        data_new=QA_DataStruct_Stock_min(res.set_index(['datetime', 'code'], drop=True)) 
        data_new=data_new.add_func(QA_data_min_to_day).sort_index().reset_index()
        data_new.rename(columns={'datetime':'date'}, inplace=True)
        data_new=QA_DataStruct_Stock_day(data_new.set_index(['date', 'code'], drop=True),if_fq='qfq')
        self.data=self.data_old.__add__(data_new)
    def fetch_get_realtime_hexo(self,code=['000001'],type_='1min'):
        '''
        从数据库中读取hexo存储的数据
        '''
        code2=[QA.get_stock_market(str(x))+str(x) for x in code] #将6位代码转换为hexo存储的8位格式
        mg = pymongo.MongoClient('mongodb://127.0.0.1:27017')
#        res=mg.qa['realtime_{}'.format(datetime.date.today())].find(
#            {'code': {'$in': code2},
#             'frequence': type_},
#            {"_id": 0},
#            batch_size=10000)
        date_=datetime.datetime.now().strftime("%Y-%m-%d")
        res=mg.qa['realtime_{}'.format(date_)].find(
            {'code': {'$in': code2},
             'frequence': type_},
            {"_id": 0},
            batch_size=10000)        
        res=pd.DataFrame([i for i in res])
        res = res.assign(
                code2=res['code'].apply(
                    lambda x: x[2:]
                    )
                )
        res = res.loc[:,
                      [
                          'code2',
                          'open',
                          'high',
                          'low',
                          'close',
                          'volume',
                          'datetime',
                          'frequence'
                      ]]
        res['amount']=0
        res=res.rename(columns={"code2": "code", "frequence":"type" })
        return res   
    def select_code(self):
        '''
        盘前进行选股
        '''
        pass  
    def update_account(self):
        '''
        盘前进行账号确认
        '''
        pass                
    def before_trade(self):
        '''
        开盘前所做准备，需要读取数据库数据
        '''
        self.load_data()
        self.select_code()
        self.update_account()
        content =datetime.datetime.now().strftime("%Y-%m-%d")+ " 马上开盘，数据载入正常，祝愿大家股票涨不停，牛年发发发！！！"
        data_ = {"title":'开盘提醒',"text":content}
        data = {"msgtype": "markdown","markdown": data_}    
        qz.qz_send_dingding(data)
        now=datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        print(now+' 发送盘前钉钉消息完成。。。')        
    def trade(self):
        '''
        盘中需要运行的函数，包括：1.从数据库中读取实时数据，并与旧数据合同形成总数据
                                2.计算策略指标
                                3.根据指标进行买卖
        '''
        try:
            #self.update_data_hexo()
            self.update_data()
            self.on_bar()
        except:
            pass
    def after_trade(self):
        '''
        收盘后所做工作，将账户信息发送给钉钉群
        '''
        content = datetime.datetime.now().strftime("%Y-%m-%d")+" 收盘啦，恭喜发财，大吉大利！"
        data_ = {"title":'收盘提醒',"text":content}
        data = {"msgtype": "markdown","markdown": data_}    
        qz.qz_send_dingding(data)
        now=datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        print(now+' 发送盘后钉钉消息完成。。。')         
        pass    
    def run_(self):
        self.signal_before_trade=1
        self.signal_after_trade=1   
        while 1:            
            date=datetime.datetime.now().strftime("%Y-%m-%d")
            mini=datetime.datetime.now().strftime("%H%M")
            time_=datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            if QA_util_if_trade(date):
                if mini=='0925' and self.signal_before_trade==1: 
                    self.before_trade()
                    self.signal_before_trade-=1
                if self.if_trade_time() and mini in self.frequence_:
                    self.trade()
                if mini=='1500' and self.signal_after_trade==1:
                    self.after_trade()
                    self.signal_after_trade-=1
                if mini=='1502':
                    self.signal_before_trade=1
                    self.signal_after_trade=1 
            if mini[-2:]=='00':
                now=datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                print(now+' 策略：'+self.account_cookie+' 正在运行中（心跳提醒）。。。')                  
            time.sleep(60)
    def run(self):            
        tt=QA_util_random_with_topic('trade' )
        now=datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        print(now+' 策略：'+self.account_cookie+' 启动。。。')         
        tt=threading.Thread(target=self.run_)
        tt.start()
    def run_debug_(self):
        self.signal_before_trade=1
        self.signal_after_trade=1         
        while 1:            
            date=datetime.datetime.now().strftime("%Y-%m-%d")
            mini=datetime.datetime.now().strftime("%H%M")
            time_=datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            if self.signal_before_trade==1: 
                self.before_trade()
                self.signal_before_trade-=1
            if mini in self.frequence_:
                    self.trade()
                # if self.signal_before_trade==1:
                #     self.after_trade()
                #     self.signal_aftor_trade-=1
            time.sleep(30)
    def run_debug(self):            
        tt=QA_util_random_with_topic('trade' )
        now=datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        print(now+' 策略：'+self.account_cookie+' 启动。。。')        
        tt=threading.Thread(target=self.run_debug_)
        tt.start()        
if __name__=='__main__':
    #上证指数 000001
    #上证50  000016
    #中证500 399905
    #沪深300 000300
    #创业板  399006

#    etf_list=QA.QA_fetch_etf_list()
#    etf_list[etf_list.name.str.contains('创业板')]
#    list_etf=['50ETF','300ETF','500ETF','创业板','800ETF']
#    #code=etf_list[etf_list.name.isin(list_etf)].code.tolist()[0] 
#    name='ETF'#etf_list[etf_list.name==aa].name.tolist()[0]
#    list_etf_code=['510050','510300','510500','159915','515800']

    #end_date=QA_util_get_real_date(dt.date.today().strftime("%Y-%m-%d"), towards=-1)
    #start_date='2016-01-01'#QA_util_get_last_day(end_date,700) #得到上一个(n)交易日
    #data = QA.QA_fetch_index_min_adv(code, start_date, end_date,frequence='60min')#.to_qfq()
    code=qz.qz_fetch_stock_list_tushare().code.to_list()[:100]
    self=stock_trade_base(code=code)
    self.load_data()
#    t1=time.time()
#    self.update_data()
#    print(time.time()-t1)
#    self.run()
    #self.run_debug()


