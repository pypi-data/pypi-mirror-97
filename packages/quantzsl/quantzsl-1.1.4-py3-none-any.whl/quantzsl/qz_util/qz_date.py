# -*- coding: utf-8 -*-
"""
Created on Thu Sep 19 22:31:09 2019

@author: Administrator
"""

from PIL import Image
import pytesseract
import os,time
import socket
import threading
import time
import requests
import datetime

def qz_util_get_next_day(date, n=1):
    """
    explanation:
        得到下一个(n)自然日
        如需获取交易日,请用QA_util_get_next_day()
    params:
        * date->
            含义: 日期
            类型: str
            参数支持: []
        * n->
            含义: 步长
            类型: int
            参数支持: [int]
    """
    date = str(date)[0:10]
    ls=(datetime.datetime.strptime(date, "%Y-%m-%d") + datetime.timedelta(days=n)).strftime("%Y-%m-%d")
    return ls

def qz_util_get_last_day(date, n=1):
    """
    explanation:
        得到下一个(n)自然日
        如需获取交易日,请用QA_util_get_last_day()
    params:
        * date->
            含义: 日期
            类型: str
            参数支持: []
        * n->
            含义: 步长
            类型: int
            参数支持: [int]
    """
    date = str(date)[0:10]
    ls=(datetime.datetime.strptime(date, "%Y-%m-%d") - datetime.timedelta(days=n)).strftime("%Y-%m-%d")
    return ls


