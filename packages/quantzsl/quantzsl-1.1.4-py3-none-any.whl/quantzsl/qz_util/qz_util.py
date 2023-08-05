# -*- coding: utf-8 -*-
"""
Created on Thu Sep 19 22:31:09 2019

@author: Administrator
"""

from selenium import webdriver
from PIL import Image
import pytesseract
import os,time
import socket
import threading
import time
import requests
import datetime

def qz_util_change_len(i,n=2):
    i=str(i)  #数字占、字母占1个 汉子2个
    if len(i.encode('gbk'))<n and len(i.encode('gbk'))==1:
        res=str(i)+'-'*(n-len(i))
    elif len(i.encode('gbk'))<n and len(i.encode('gbk'))!=1:
        res=str(i)+'-'*(n-len(i.encode('gbk')))

    else:
        pass
        res=i
    return res

