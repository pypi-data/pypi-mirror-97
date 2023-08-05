# -*- coding: utf-8 -*-
"""
Created on Sun Sep  6 20:11:28 2020

@author: ZSL
"""
import pandas as pd
import numpy as np 
import time
import datetime
import threading
from QAPUBSUB.consumer import subscriber_routing,subscriber_topic
from QAPUBSUB.producer import publisher_routing,publisher_topic

sub_list=['1min','5min','15min','60min','day']
for i in sub_list:
    sub='qz_realtime_'+i
    z1 = subscriber_topic(exchange=sub, routing_key='')
    z1.callback = lambda a, b, c, x: print('{}订阅数据{}'.format(i,x))
    threading.Thread(target=z1.start).start()
    print(i)
    time.sleep(1)