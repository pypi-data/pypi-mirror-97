# -*- coding: utf-8 -*-
"""
Created on Sun Feb 24 22:54:03 2019

@author: ZSL
"""

import smtplib  #加载smtplib模块
from email.mime.text import MIMEText
from email.utils import formataddr
   
def qz_send_email(title,data,sender,sender_pass,user,sender_name='ziyu',user_name='dear'):
    ret=True
    msg=MIMEText(data,'plain','utf-8') 
    msg['Subject']=title #邮件的主题   
    msg['From']=formataddr([sender_name,sender])   #括号里的对应发件人邮箱昵称、发件人邮箱账号
    msg['To']=formataddr([user_name,user])   #括号里的对应收件人邮箱昵称、收件人邮箱账号
    
    try:
        server=smtplib.SMTP("smtp.163.com",25)  #发件人邮箱中的SMTP服务器，端口是25
        server.login(sender,sender_pass)    #括号中对应的是发件人邮箱账号、邮箱密码
        server.sendmail(sender,[user,],msg.as_string())   #括号中对应的是发件人邮箱账号、收件人邮箱账号、发送邮件
        server.quit()   #关闭连接
    except Exception as e:
        print(e)
        ret=False
        
    if ret:
        print("send email success") #如果发送成功则会返回ok，稍等20秒左右就可以收到邮件
    else:
        print("send email fail")  #如果发送失败则会返回filed

if __name__ == '__main__':
    sender="13269319786@163.com" #发件人邮箱账号
    sender_pass="zsl303466906"  #发件人密码
    
    title='你好测试邮件'
    data = "你好，这是一份测试邮件666666" #邮件正文
    
    user="303466906@qq.com" #收件人邮箱账号

    qz_send_mail(title,data,sender,sender_pass,user,sender_name='ziyu',user_name='dear')



#ret=mail()
#if ret:
#    print("ok") #如果发送成功则会返回ok，稍等20秒左右就可以收到邮件
#else:
#    print("filed")  #如果发送失败则会返回filed
#    



    
#from email.mime.application import MIMEApplication
#添加附件
#注意这里的文件路径是斜杠
#xlsxpart = MIMEApplication(open('C:/Users/zhangjunhong/Desktop/这是附件.xlsx', 'rb').read())
#xlsxpart.add_header('Content-Disposition', 'attachment', filename='这是附件.xlsx')
#msg.attach(xlsxpart) 
    
#msg.attach(MIMEText(body, 'plain', 'utf-8'))  

