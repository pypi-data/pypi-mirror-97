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
from selenium.webdriver.common.action_chains import ActionChains

def 判断是否联网_(testserver):
  s=socket.socket()
  s.settimeout(1)
  try:
    status = s.connect_ex(testserver)
    if status == 0:
      s.close()
      return True
    else:
      return False
  except Exception as e:
    return False
 
def 判断是否联网(testserver=('www.baidu.com',443)):
  isOK = 判断是否联网_(testserver)
  return isOK




 
def relogin():
    url = "http://10.1.1.131"
    driver = webdriver.Chrome()
    time.sleep(1)
    driver.get(url)
    time.sleep(1)
    driver.maximize_window()
    driver.find_element_by_id('username').clear()
    driver.find_element_by_id('username').send_keys('8902012')
    driver.find_element_by_id('password').clear()
    driver.find_element_by_id('password').send_keys('zheng890209')
    location=driver.find_element_by_class_name('submit-group').location
    size=driver.find_element_by_class_name('submit-group').size
    left = location['x']
    top = location['y']
    right = location['x'] + size['width']
    bottom = location['y'] + size['height']
    x=(left+right)/2-150
    y=(top+bottom)/2
    def click_locxy(dr, x, y, left_click=True):
        '''
        dr:浏览器
        x:页面x坐标
        y:页面y坐标
        left_click:True为鼠标左键点击，否则为右键点击
        '''
        if left_click:
            ActionChains(dr).move_by_offset(x, y).click().perform()
        else:
            ActionChains(dr).move_by_offset(x, y).context_click().perform()
        ActionChains(dr).move_by_offset(-x, -y).perform()  # 将鼠标位置恢复到移动前
    click_locxy(driver, x, y) #
    time.sleep(3)
    driver.close()


def detect():
    a1=判断是否联网()
    if a1 is True:
        print(datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")+' 网络处于连接状态。')
    else:
        try:
            relogin()
        except:
            pass


while True:
    detect()
    time.sleep(6000)


