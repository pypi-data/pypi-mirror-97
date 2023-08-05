# -*- coding: utf-8 -*-
"""
Created on Thu Feb 25 21:10:06 2021

@author: Administrator
"""
if __name__ == '__main__':

    import platform
    import time  
    import puppet
    
    # 自动登录账户, comm_pwd 是可选参数
    # accinfo = {
    #     'account_no': 'mo_233469636',
    #     'password': 'Zsl303466906',
    #     'comm_pwd': True,  # 模拟交易端必须为True
    #     'client_path': r'C:\同花顺软件\同花顺\xiadan.exe'
    # }
    # accinfo2 = {
    #     'account_no': 'mx_566629785',
    #     'password': 'Zsl303466906',
    #     'comm_pwd': True,  # 模拟交易端必须为True
    #     'client_path': r'C:\同花顺软件\同花顺\xiadan.exe'
    # } 
    # accinfo3 = {
    #     'account_no': '35202548',
    #     'password': 'Zsl303466906',
    #     'comm_pwd': True,  # 模拟交易端必须为True
    #     'client_path': r'C:\同花顺软件\同花顺\xiadan.exe'
    # }      
    #acc = puppet.login(accinfo)
    
    # 绑定已登录账户
    acc = puppet.Account(title='')
#    acc=acc.switch_account(1)
    dir(acc)
    acc.buy('000001', 12.68, 200)
#    acc.sell('000001', 12.68, 100)
    acc.cancel_buy('000001')    
    acc.cancel_all('000001')
    
    
    undone=acc.query('undone') 
    delivery_order=acc.query('delivery_order') 
    bingo=acc.query('bingo')  
    #margin=acc.query('margin')
    discount=acc.query('discount')     
    margin_pos=acc.query('margin_pos')    
    discount=acc.query('discount')    
    position=acc.query('position') 
    deal=acc.query('deal')    
    historical_deal=acc.query('historical_deal')
    position=acc.query('position')  
    summary=acc.query('summary')    
    acc.query()
    acc. query.__doc__
