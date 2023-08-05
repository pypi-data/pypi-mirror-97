# -*- coding: utf-8 -*-
"""
Created on Tue Aug 27 20:00:47 2019

@author: ZSL
"""
import json
import requests
import sys

import time
import datetime
import hmac
import hashlib
import base64
import urllib.parse

#url = 'http://127.0.0.1:10086/puppet'
#data={'symbol': '000001', 'price': 10, 'quantity': 100, 'action': 'buy'}
#data={'title': '', 'action': 'bind'}
##data={'symbol':'000001','price':'12','quantity':'100','action':'buy'}
#r = requests.post(url,json=data)
#
#session = requests.Session()
#session.post(url,json=data).json()


def cal_secret(secret):
    timestamp = str(round(time.time() * 1000))
    secret_enc = secret.encode('utf-8')
    string_to_sign = '{}\n{}'.format(timestamp, secret)
    string_to_sign_enc = string_to_sign.encode('utf-8')
    hmac_code = hmac.new(secret_enc, string_to_sign_enc, digestmod=hashlib.sha256).digest()
    sign = urllib.parse.quote_plus(base64.b64encode(hmac_code))
    return timestamp,sign


# reminders 提醒
def qz_send_dingding(data,receiver='消息内测'):
    token_list={'股海捞金':{'token':'96e56b6945530f58db51e6a72578a9e8979ce429acff938f158ed69ab728310f',
                           'secret':'SEC12b29aaabf63738456e6cd1141eb80eb967805ee267735f5ac896ef96acda28d'},
                '消息内测':{'token':'52e7842d872cae231b7b22c353eb90628c4426bde5698c9310ab298d6d76a266',
                           'secret':'SEC5c59bb2a30739a27f84f58029963dc0141fc1a73a16b277f14448afca638246c'},
            }
    if receiver=='all':
        for i in token_list:
            pass
            qz_send_dingding_(data=data,token=token_list[i]['token'],secret=token_list[i]['secret'])
            #receiver='消息内测'
    elif receiver in token_list:
        i=receiver
        qz_send_dingding_(data=data,token=token_list[i]['token'],secret=token_list[i]['secret'])
    else:
        now=datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        print(now+' 钉钉消息发送失败，QZ没有该钉钉接收者，请检查输入是否输入错误或者添加该钉钉接收者信息') 
        

def qz_send_dingding_(data,token,secret):
    headers = {'Content-Type': 'application/json;charset=utf-8'}
    timestamp,sign=cal_secret(secret)
    url = 'https://oapi.dingtalk.com/robot/send?access_token='+token+'&timestamp='+timestamp+'&sign='+sign    
    r = requests.post(url,data=json.dumps(data),headers=headers)
if __name__ == '__main__':    
    title = "模拟下单"  
    content ="## 策略：日线趋势 \n\n"+\
          "### 下单提醒：买入\n\n"+\
          ">**序号**---**代码**------**名称**-----**价格**---**涨跌幅** \n\n"+\
          ">-1---000001--中国平安--10.34--5.34% \n\n"+\
          ">-1---000001--中国平安--10.34--5.34% \n\n"

         
            
    data_ = {"title":title,"text":content}
    data = {"msgtype": "markdown","markdown": data_}  
   # qz_send_dingding_(data=data,token=token_list[i]['token'],secret=token_list[i]['secret'])
    qz_send_dingding(data,'消息内测')
    token='52e7842d872cae231b7b22c353eb90628c4426bde5698c9310ab298d6d76a266'  
    #https://ding-doc.dingtalk.com/doc#/serverapi2/qf2nxq
    #https://blog.csdn.net/robertcid/article/details/90319570
    