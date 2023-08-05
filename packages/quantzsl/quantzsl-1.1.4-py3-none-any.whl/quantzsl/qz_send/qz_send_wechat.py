# -*- coding: utf-8 -*-
"""
Created on Mon Feb 25 00:00:32 2019

@author: ZSL
"""

import requests


def _send_wechat(data,api = "https://sc.ftqq.com/SCU45251Teeee72c400271f2a76cbd18e84b93a7f5c72bc97b9716.send"):
    
    '''
    通过service酱给微信发送消息
    '''
    req = requests.post(api,data = data)

def qz_send_wechat(data):
    mes=["https://sc.ftqq.com/{}.send".format('SCU45251Teeee72c400271f2a76cbd18e84b93a7f5c72bc97b9716')]
#            "https://sc.ftqq.com/{}.send".format('SCU45701T237610825e28b1577d7874513333c0fa5c7d233d387fa')
         
#            ]
    for i in mes: 
        pass
        _send_wechat(data,i)
        
    
    
        
if __name__ == '__main__':

    #详情请访问  http://sc.ftqq.com/3.version    
    title = "模拟下单"  #消息标题，最长为256，必填。
    #消息内容，最长64Kb，可空，支持MarkDown。
    content = """  
    # 000001,100,buy,6.25
    ## hehe2
    """
    data = {"text":title,"desp":content}    
    qz_send_wechat(data)
    
    
    
    import time
    import QUANTAXIS as QA
    code = QA.QA_fetch_stock_list_adv().code.tolist()[:10]
    code=QA.QAFetch.QA_fetch_get_stock_list('tdx') .code.tolist()
    x=QA.QA_Tdx_Executor(thread_num=6)
    t=time.time()
    data=x.get_realtime_concurrent(code)
    print(time.time()-t)
