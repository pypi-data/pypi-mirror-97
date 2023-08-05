# -*- coding: utf-8 -*-
"""
Created on Sat Feb  9 15:12:56 2019

@author: ZSL
"""
import pandas as pd
import numpy as np
import time
import datetime
import pymongo
from qaenv import mongo_ip, mongo_uri
def qz_mongo():
    client = pymongo.MongoClient(mongo_uri) 
    return client
