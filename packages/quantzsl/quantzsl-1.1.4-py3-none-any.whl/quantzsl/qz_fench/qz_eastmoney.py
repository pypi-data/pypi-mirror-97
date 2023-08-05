# -*- coding: utf-8 -*-
"""
Created on Sun Nov  1 20:52:56 2020

@author: ZSL
"""

import requests
import re
import pandas as pd
import json
import time
import datetime
from retrying import retry
from QUANTAXIS.QAUtil import (
                              QA_util_get_real_date,
                              QA_util_get_last_day,
                              QA_util_get_next_day,
                              QA_util_date_stamp,
                              QA_util_time_stamp,
                              QA_util_code_tostr,
                              QA_util_code_tolist
                              ) 
from random import randint
import random
import QUANTAXIS as QA
@retry(stop_max_attempt_number=10, wait_random_min=50, wait_random_max=100)
def qz_fetch_get_block_eastmoney(): 
    '''    
    从东方财富网站爬取各个板块的分类，返回值为dic格式，包含概念板块、地域板块和行业板块的
    分类的代码
    '''    
    url="http://quote.eastmoney.com/center/api/sidemenu.json"   
    red=requests.get(url)
    data=red.text
    沪深板块=json.loads(data)[5]['next']
       #aa=data.split(a1)
    list_=['概念板块','地域板块','行业板块']
    j=0
    res___={}
    for i in list_:
        pass
        res_= 沪深板块[j]['next']
        j=j+1
        res_name=[]
        res_code=[]        
        for k in res_:
            pass
            #print(j)
            res_name.append(k['title'])
            res_code.append(k['key'][11:])
        res_=pd.concat([pd.DataFrame(res_name),pd.DataFrame(res_code)],axis=1)  
        res_.columns=['name','code']
        res___[list_[j-1]]=res_
#    概念板块=res___['概念板块']#pd.DataFrame(res___['概念板块'])
#    地域板块=res___['地域板块']
#    行业板块=res___['行业板块']     
    return res___  
@retry(stop_max_attempt_number=10, wait_random_min=50, wait_random_max=100)    
def qz_fetch_get_block_stock_eastmoney_(code='BK0619'): 
    '''
    从东方财富网站爬取各个板块包含的股票
    f12--代码
    f14--名称
    '''
    #原始网址
#    url='http://17.push2.eastmoney.com/api/qt/clist/get?cb=jQuery112408566791782023113_1604239545381&'+\
#    'pn=1&pz=20&po=1&np=1&ut=bd1d9ddb04089700cf9c27f6f7426281&fltt=2&invt=2&fid=f3&'+\
#    'fs=b:BK0619+f:!50&fields=f1,f2,f3,f4,f5,f6,f7,f8,f9,f10,f12,f13,f14,f15,f16,f17,'+\
#    'f18,f20,f21,f23,f24,f25,f22,f11,f62,f128,f136,f115,f152,f45&_=1604239545382'
    #精简后
    url='http://17.push2.eastmoney.com/api/qt/clist/get?cb='+\
    'jQuery'+random_rt(22,22)+'_'+random_rt(13,13)+'&'+\
    'pn=1&pz=200&po=1&np=1&'+\
    'ut=bd1d9ddb04089700cf9c27f6f7426281&'+\
    'fltt=2&invt=2&fid=f3&'+\
    'fs=b:'+code+'+f:!50&fields=f14,f12'+\
    '_='+random_rt(13,13)
    red=requests.get(url)
    data=red.text
    data1=re.split('[()]',data)[1]
    try:
        data2=json.loads(data1)['data']['diff']
        res=[]
        for i in data2:
            pass   
            res.append([i['f14'],i['f12']])
        #res_=pd.DataFrame(res)        
        return res
    except:
        return []                

def qz_fetch_get_block_stock_eastmoney(block_name='概念板块'): 
    '''
    获得东方财富板块的个股信息
    输入为：
    qz_fetch_get_block_stock_eastmoney('概念板块')
    qz_fetch_get_block_stock_eastmoney('地域板块')
    qz_fetch_get_block_stock_eastmoney('行业板块')
    输出为：
    DataFrame格式
    '''    
    block_eastmoney=qz_fetch_get_block_eastmoney()
    code_list=block_eastmoney[block_name]
    
    res=[]
    for item in range(len(code_list['code'])):
        pass
        name=code_list['name'][item]
        code=code_list['code'][item]
        print(
            '{} The {} of Total {}, {} {}-{},'.format(
                    datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                    item+1, 
                    len(code_list),
                    str(float((item+1) / len(code_list) * 100))[0:4] + '%',
                    block_name,
                    str(name),
                ) )                  
        res_=qz_fetch_get_block_stock_eastmoney_(code)
        for j in res_:
            pass
            j.append(name)
            j.append(code)
            res.append(j)   
    res=pd.DataFrame(res) 
    res.columns=['name','code','block','block_code'] 
    res=res[['block','block_code','name','code']]                   
    return res


@retry(stop_max_attempt_number=10, wait_random_min=50, wait_random_max=100)
def qz_fetch_get_block_day_eastmoney(code='BK0714',start='20200101',end='20201001',frequence='day'):         
    '''
    获取东方财富板块的日线级别以上数据
    klt参数：
    101 日线
    102 周线
    103 月线
    104 季线
    105 年线
    '''
    #由于东财数据结果为不包含关系，需要处理一下
    if len(start)==8:
        start=start[:4]+'-'+start[4:6]+'-'+start[6:]
    start=QA_util_get_real_date(start,towards=1)
    start=start.replace('-', '')
    if len(end)==8:
        end=end[:4]+'-'+end[4:6]+'-'+end[6:]
    end=QA_util_get_real_date(end,towards=-1)
    end=end.replace('-', '')
    if isinstance(code, list):
        code=code[0]
        
    if frequence in ['day', 'd', 'D', 'DAY', 'Day']:
        frequence = '101'
    elif frequence in ['w', 'W', 'Week', 'week']:
        frequence = '102'
    elif frequence in ['month', 'M', 'm', 'Month']:
        frequence = '103'
    elif frequence in ['quarter', 'Q', 'Quarter', 'q']:
        frequence = '104'
    elif frequence in ['y', 'Y', 'year', 'Year']:
        frequence = '105'
    url='http://push2his.eastmoney.com/api/qt/stock/kline/get?cb='+\
    'jQuery'+random_rt(22,22)+'_'+random_rt(13,13)+'&'+\
    'secid=90.'+code+'&'+\
    'ut=fa5fd1943c7b386f172d6893dbfba10b&'+\
    'fields1=f1%2Cf2%2Cf3%2Cf4%2Cf5&'+\
    'fields2=f51%2Cf52%2Cf53%2Cf54%2Cf55%2Cf56%2Cf57%2Cf58&'+\
    'klt='+frequence+'&'+\
    'fqt=0&'+\
    'beg='+start+'&'+\
    'end='+end+'&'+\
    '_='+random_rt(13,13)

    red=requests.get(url)
    data=red.text    
    data1=re.split('[()]',data)[1]    
    data2=json.loads(data1)['data']
    try:
        name=data2['name']
        klines=data2['klines']
        res=[]
        for i in klines:
            pass
            res.append(i.split(','))
        res=pd.DataFrame(res)  
        res.columns=['date','open','close','high','low','vol','amount','zhenfu']
        res=res.drop(['zhenfu'],axis=1)
        
        res = res.assign(
                    code=str(code),
                    name=str(name),
                    date_stamp=res['date'].apply(
                        lambda x: QA_util_date_stamp(str(x)[0:10])
                        )
                    ) 
        for i in res.columns:
            pass
            try:
                res[i]=res[i].apply(float)
            except:
                pass
        return res
    except:
        return None
    
#分钟线
#http://push2his.eastmoney.com/api/qt/stock/kline/get?cb=jQuery112407431892860225657_1604760798438&secid=90.BK0714&ut=fa5fd1943c7b386f172d6893dbfba10b&fields1=f1%2Cf2%2Cf3%2Cf4%2Cf5&fields2=f51%2Cf52%2Cf53%2Cf54%2Cf55%2Cf56%2Cf57%2Cf58&klt=30&fqt=0&beg=19900101&end=20220101&_=1604760799425


@retry(stop_max_attempt_number=10, wait_random_min=50, wait_random_max=100)
def QZ_get_moneyflow_realtime_from_eastmoney(): 
    url='http://nufm.dfcfw.com/EM_Finance2014NumericApplication/'+\
    'JS.aspx?type=ct&st=(BalFlowMain)&sr=-1&p=2&ps=10000&js=var%20AToYFfkt={pages:(pc)'+\
    ',date:%222014-10-22%22,data:[(x)]}&token='+\
    '894050c76af8597a853f5b408b759f5d'+\
    '&cmd=C._AB&sty=DCFFITA&rt=52016132' 
    
    url='http://nufm.dfcfw.com/EM_Finance2014NumericApplication/'+\
    'JS.aspx?type=ct&st=(BalFlowMain)&sr=-1&p=2&ps=10000&js=var%20AToYFfkt={pages:(pc)'+\
    ',date:%222014-10-22%22,data:[(x)]}&token='+\
    '894050c76af8597a853f5b408b759f5d'+\
    '&cmd=C._AB&sty=DCFFITA&rt='+random_rt()           
    red=requests.get(url)
    data=red.text
    data1=data[46:]
    data2=data1[:-2]
    data3=re.split('","',data2)
    data3[0]=data3[0][1:]
    data3[-1]=data3[-1][:-1]    
    res=[]
    for i in data3:
        pass
        res.append(i.split(','))
    res_=pd.DataFrame(res)
    list_columns=['沪深属地','代码','名称','价格','涨跌幅','主力净流入额','主力净流入占比',
                  '超大单净流入额','超大单净流入占比','大单净流入额','大单净流入占比','中单净流入额',
                  '中单净流入占比','小单净流入额','小单净流入占比','时间','不知','不知','不知']
    res_.columns=list_columns[:len(res_.columns)]
    for i in res_.columns:
        try:
            res_[i]=res_[i].apply(float)
        except:
            pass
    return res_          

def random_taken(lens=32):
    '''
    生成一个指定长度的由数字和字母组成的随机数
    '''
    import random 
    list_ =[chr(i) for i in range(97,123)] + [str(i) for i in range(10)]
    num = random.sample(list_, lens) 
    res=''.join(num)
    return res 
   
def random_rt(n1=13,n2=13):
    

    start = 10**(n1-1)
    end = (10**(n2-1))*2    
    return str(randint(start, end)) 


@retry(stop_max_attempt_number=10, wait_random_min=50, wait_random_max=100)
def qz_fetch_get_stock_day_eastmoney(code='000858',start='20210101',end='20211001',frequence='day'):         
    '''
    获取东方财富板块的日线级别以上数据
    klt参数：
    101 日线
    102 周线
    103 月线
    104 季线
    105 年线
    '''
    #由于东财数据结果为不包含关系，需要处理一下
    if len(start)==8:
        start=start[:4]+'-'+start[4:6]+'-'+start[6:]
    start=QA_util_get_real_date(start,towards=1)
    start=start.replace('-', '')
    if len(end)==8:
        end=end[:4]+'-'+end[4:6]+'-'+end[6:]
    end=QA_util_get_real_date(end,towards=-1)
    end=end.replace('-', '')
    if isinstance(code, list):
        code=code[0]
    if frequence in ['day', 'd', 'D', 'DAY', 'Day']:
        frequence = '101'
    elif frequence in ['w', 'W', 'Week', 'week']:
        frequence = '102'
    elif frequence in ['month', 'M', 'm', 'Month']:
        frequence = '103'
    elif frequence in ['quarter', 'Q', 'Quarter', 'q']:
        frequence = '104'
    elif frequence in ['y', 'Y', 'year', 'Year']:
        frequence = '105'
    url='http://push2his.eastmoney.com/api/qt/stock/kline/get?cb='+\
    'jQuery'+random_rt(21,21) +'_'+random_rt(13,13)+\
    '&fields1=f1%2Cf2%2Cf3%2Cf4%2Cf5%2Cf6'+\
    '&fields2=f51%2Cf52%2Cf53%2Cf54%2Cf55%2Cf56%2Cf57%2Cf58%2Cf59%2Cf60%2Cf61'+\
    '&ut='+random_taken(lens=32)+\
    '&klt='+frequence+\
    '&fqt=1'+\
    '&secid=0.'+code+\
    '&beg='+start+\
    '&end='+end+\
    '&smplmt=460&lmt=1000000&_='+random_rt(13,13)    
    
    red=requests.get(url)
    data=red.text    
    data1=re.split('[()]',data)[1]    
    data2=json.loads(data1)['data']
    try:
        name=data2['name']
        klines=data2['klines']
        res=[]
        for i in klines:
            pass
            res.append(i.split(','))
        res=pd.DataFrame(res)  
        res.columns=['date','open','close','high','low','vol','amount','zhenfu','zhangdiefu','zhangdiee','huanshoulv']
        res=res.drop(['zhenfu','zhangdiefu','zhangdiee','huanshoulv'],axis=1)
        
        res = res.assign(
                    code=str(code),
                    name=str(name),
                    date_stamp=res['date'].apply(
                        lambda x: QA_util_date_stamp(str(x)[0:10])
                        )
                    ) 
        for i in res.columns:
            pass
            if i!='code':
                try:
                    res[i]=res[i].apply(float)
                except:
                    pass
        return res
    except:
        return None
@retry(stop_max_attempt_number=10, wait_random_min=50, wait_random_max=100)
def qz_fetch_get_stock_min_eastmoney(code='000858',start='20210101',end='20211001',frequence='60min'):         
    '''
    获取东方财富板块的分钟级别数据
    '''
    #由于东财数据结果为不包含关系，需要处理一下
    if len(start)==8:
        start=start[:4]+'-'+start[4:6]+'-'+start[6:]
    start=QA_util_get_real_date(start,towards=1)
    start=start.replace('-', '')
    if len(end)==8:
        end=end[:4]+'-'+end[4:6]+'-'+end[6:]
    end=QA_util_get_real_date(end,towards=-1)
    end=end.replace('-', '')
    if isinstance(code, list):
        code=code[0]
    if frequence in ['5', '5m', '5min', 'five']:
        frequence = '5'
    elif frequence in ['1', '1m', '1min', 'one']:
        frequence = '1'
    elif frequence in ['15', '15m', '15min', 'fifteen']:
        frequence = '15'
    elif frequence in ['30', '30m', '30min', 'half']:
        frequence = '30'
    elif frequence in ['60', '60m', '60min', '1h']:
        frequence = '60'
    url='http://push2his.eastmoney.com/api/qt/stock/kline/get?cb='+\
    'jQuery'+random_rt(21,21) +'_'+random_rt(13,13)+\
    '&fields1=f1%2Cf2%2Cf3%2Cf4%2Cf5%2Cf6'+\
    '&fields2=f51%2Cf52%2Cf53%2Cf54%2Cf55%2Cf56%2Cf57%2Cf58%2Cf59%2Cf60%2Cf61'+\
    '&ut='+random_taken(lens=32)+\
    '&klt='+frequence+\
    '&fqt=1'+\
    '&secid=0.'+code+\
    '&beg='+start+\
    '&end='+end+\
    '&smplmt=460&lmt=1000000&_='+random_rt(13,13)    
    
    red=requests.get(url)
    data=red.text    
    data1=re.split('[()]',data)[1]    
    data2=json.loads(data1)['data']
    try:
        name=data2['name']
        klines=data2['klines']
        res=[]
        for i in klines:
            pass
            res.append(i.split(','))
        res=pd.DataFrame(res)  
        res.columns=['datetime','open','close','high','low','vol','amount','zhenfu','zhangdiefu','zhangdiee','huanshoulv']
        res=res.drop(['zhenfu','zhangdiefu','zhangdiee','huanshoulv'],axis=1)
        
        res = res.assign(
                    code=str(code),
                    name=str(name),
                    date_stamp=res['datetime'].apply(
                        lambda x: QA_util_time_stamp(str(x))
                        )
                    ) 
        for i in res.columns:
            pass
            if i!='code':
                try:
                    res[i]=res[i].apply(float)
                except:
                    pass
        return res
    except:
        return None    

if __name__ == '__main__':
    t=time.time()
    板块分类=qz_fetch_get_block_eastmoney()
    概念个股=qz_fetch_get_block_stock_eastmoney('概念板块')
    地域个股=qz_fetch_get_block_stock_eastmoney('地域板块')
    行业个股=qz_fetch_get_block_stock_eastmoney('行业板块')
    data=qz_fetch_get_block_day_eastmoney(code='BK0714',start='20100101',end='20201001')    
    #查看某一股票都属于哪个行业
    res1=概念个股[概念个股['code']=='000008']
    #查看某一行业的股票
    res2=概念个股[概念个股['block']=='稀土永磁']
    res3=行业个股[行业个股['block']=='材料行业'] 
    
    
    stock_list=QA.QA_fetch_stock_list().code.to_list()[:1]
    delta=5
    freq='15min'
    end=datetime.datetime.now().strftime("%Y-%m-%d")
    start=(datetime.date.today() - datetime.timedelta(days=delta)).strftime("%Y-%m-%d")
#仅支持单个股票爬取，如有多个股票请for循环爬取    
    data1=qz_fetch_get_stock_min_eastmoney(code=stock_list,start=start,end=end,frequence=freq)
    data2=qz_fetch_get_stock_day_eastmoney(code=stock_list,start=start,end=end,frequence='day')
##字符数串转换为数组              
#str = '1,2,3'
#arr = str.split(',')
#数组转换为字符串
#arr = ['a','b']
#str = ','.join(arr)
    
