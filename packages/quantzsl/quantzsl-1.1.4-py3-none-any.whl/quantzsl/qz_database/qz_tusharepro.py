# -*- coding: utf-8 -*-
"""
Created on Sat Feb  9 15:12:56 2019

@author: ZSL
"""
import tushare as ts
def qz_ts_pro():
    token='1e8b5efdd5a68b494a0787835eda96bf2674c6dad0bc050f42900858'  #你的tusharepro token
    pro=ts.pro_api(token)
    return pro

if __name__=='__main__':
    pro=qz_ts_pro()
    
    申万指数= pro.index_basic(market='SW') 
    中证指数 = pro.index_basic(market='CSI') 
    上交所指数 = pro.index_basic(market='SSE')     
    深交所指数 = pro.index_basic(market='SZSE') 
    MSCI指数 = pro.index_basic(market='MSCI')     
#    中金所指数 = pro.index_basic(market='CICC') 
#    国证指数 = pro.index_basic(market='CNI') 
#    其他指数 = pro.index_basic(market='OTH') 