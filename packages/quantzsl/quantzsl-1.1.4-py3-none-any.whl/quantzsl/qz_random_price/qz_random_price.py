# -*- coding: utf-8 -*-
"""
Created on Sun Sep 13 14:31:36 2020

@author: ZSL
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import click
import random
import copy
import re
from QUANTAXIS.QAUtil.QADate_trade import QA_util_get_last_day,QA_util_get_trade_range
from QUANTAXIS.QAUtil.QADate import QA_util_date_int2str, QA_util_date_str2int
from QUANTAXIS.QAUtil.QAParameter import MARKET_TYPE


class OrnsteinUhlenbeckActionNoise:

    def __init__(self, mu=1, sigma=0.2, theta=0.15, dt=0.01,n=1, x0=None):
        self.theta = theta
        self.mu = np.array(mu)
        self.sigma = sigma
        self.dt = dt
        self.x0 = x0
        self.reset()
        self.n=n
        

    def __call__(self):
        x = self.x_prev + self.theta * (self.mu - self.x_prev) * self.dt + \
            self.sigma * np.sqrt(self.dt) * \
            np.random.normal(size=self.n)

        self.x_prev = x
        return x

    def reset(self):
        self.x_prev = self.x0 if self.x0 is not None else np.zeros_like(
            self.mu)

    def __repr__(self):
        return 'OrnsteinUhlenbeckActionNoise(mu={}, sigma={})'.format(self.mu, self.sigma)



class qz_random_price():
    
    def __init__(self, price, code='rb1905', start_day='2018-11-19',end_day='2018-11-22',
                 mu=0, sigma=0.2, theta=0.15, dt=0.01,n=1,weight=0.1,
                 freq='3000ms',ifprint=False,market_type=None):
        self.price=price
        self.code=code
        self.start_day=start_day
        self.end_day=end_day        

        self.mu = mu  #目标值  即最后价格为初始价格的n倍
        self.sigma = sigma  #回归过程中的扰动大小   
        self.theta = theta #回归速度     
        self.dt = dt
        self.n = n
        self.ifprint=ifprint
        self.market_type=market_type
        self.weight=weight
        self.freq=freq
        self.time_index_future = pd.timedelta_range('21:00:00.500000', '23:00:00', freq='500ms').tolist() +\
        pd.timedelta_range('09:00:00.500000', '10:15:00', freq='500ms').tolist() +\
        pd.timedelta_range('10:30:00.500000', '11:30:00', freq='500ms').tolist() +\
        pd.timedelta_range('13:30:00.500000', '15:00:00', freq='500ms').tolist()
       
        
    def __repr__(self):
        return 'qz_random_price(mu={}, sigma={})'.format(self.mu, self.sigma)
    
    def time_index_stock(self,start='2019-01-01',end='2019-01-20'): 

        freq=self.freq
        time_index_stock = pd.timedelta_range('09:30:00', '11:30:00', freq=freq).tolist() +\
        pd.timedelta_range('13:00:00', '15:00:00', freq=freq).tolist()  
        time_index_stock_=[]
        for item in time_index_stock:
            pass
            time_index_stock_.append(str(item).split()[2])
            
        trad_list=QA_util_get_trade_range(start,end)
        time_index_stock__=[]
        for i in trad_list:
            for j in time_index_stock_:
                pass
                time_index_stock__.append(i+' '+j)
        
        return  time_index_stock__       
                
         
        
    def get_random_price(self):
        data = []
        market_type=self.market_type
        code=self.code
        weight=self.weight
        price=self.price
        start_day=self.start_day
        end_day=self.end_day        
        if isinstance(code, list):
            code = code
        elif isinstance(code, str):
            code = [code]
        else:
            print('wrong code')
        
        
        ou_noise=OrnsteinUhlenbeckActionNoise(self.mu,self.sigma,self.theta,self.dt,n=len(code))

    
        if market_type is None:
            market_type = MARKET_TYPE.STOCK_CN
            
#             market_type = MARKET_TYPE.FUTURE_CN if re.search(
#                r'[a-zA-z]+', code) else MARKET_TYPE.STOCK_CN
    
        if market_type == MARKET_TYPE.FUTURE_CN:
            time_index = self.time_index_future
        else:
            time_index = self.time_index_stock(start_day,end_day)
        res=[]
        for item in time_index:
            p=ou_noise()* price + price
            res.append(list(p))
        res=pd.DataFrame(res)
        res.columns=code
        res=res.assign(datetime=time_index)
        res=res.set_index('datetime')
                
#            tick_pickle['Volume'] += random.randint(50, 5000)
##            tick_pickle['LastPrice'] = (ou_noise()+1) * \
##                weight*price + (1-weight)*price

        return res       
    
if __name__ == '__main__':
    self=qz_random_price(code=['000001','000003','000005'],start_day='2020-01-03',end_day='2020-01-05',freq='6min',
                         price=1,mu=2,sigma=0.2,theta=0.15,dt=0.01)
    self.get_random_price().plot()
    plt.show()        

        
     
#code=['000001','000002']

#
#
#@click.command()
#@click.option('--price', default=3600)
#@click.option('--code', default='rb1905')
#@click.option('--tradingday', default='20181119')
#@click.option('--mu', default=0)
#@click.option('--sigma', default=0.2)
#@click.option('--theta', default=0.15)
#@click.option('--dt', default=1e-2)
#@click.option('--ifprint', default=True)
#@click.option('--market_type', default=None)
#def generate(price, code, tradingday, mu, sigma, theta, dt, ifprint, market_type):
#    data = get_random_price(price, code, tradingday,
#                            mu, sigma, theta, dt, ifprint, market_type)
#    print(data)
#    data.LastPrice.plot()
#    plt.show()
#
#
#if __name__ == '__main__':
#    self=get_random_price(code='000001',price=10,mu=0,sigma=1,theta=0.15,dt=0.01)
#    self.LastPrice.plot()
#    plt.show()
#    #self.ou_noise.sigma  
##ou_noise = OrnsteinUhlenbeckActionNoise(mu=np.array(0),dt=1)
##ou_noise()
#    
#	ou_noise=OrnsteinUhlenbeckActionNoise(mu=np.zeros(1),dt=0.1)
#	plt.figure('data')
#	y=[]
#	t=np.linspace(0,100,1000)
#	for _ in t:
#		y.append(ou_noise())
#	plt.plot(t,y)
#

