# coding=utf-8
import smtplib
from email.mime.text import MIMEText
from email.utils import formataddr
import os
 
# 获取ifconfig命令内容
cmd='ifconfig'
m=os.popen(cmd)
t=m.read()
m.close()
 
# 设置发件人和收件人信息
my_sender='2583423523@qq.com'  # 自己的邮箱账号
my_pass = 'ecudzikschuzebad'   # 发件人邮箱密码(之前获取的授权码)
my_user='2583423523@qq.com'    # 自己的邮箱账号
 
def mail():
    ret=True
    try:
        msg=MIMEText(t,'plain','utf-8')
        msg['From']=formataddr(["Jack",my_sender])          # 括号里的对应发件人邮箱昵称、发件人邮箱账号
        msg['To']=formataddr(["Rose",my_user])              # 括号里的对应收件人邮箱昵称、收件人邮箱账号
        msg['Subject']="树莓派IP地址获取"                   # 邮件的主题，也可以说是标题
        server=smtplib.SMTP("smtp.qq.com", 587)             # 发件人邮箱中的SMTP服务器，端口是587
        server.login(my_sender, my_pass)                    # 括号中对应的是发件人邮箱账号、邮箱密码
        server.sendmail(my_sender,[my_user,],msg.as_string())  # 括号中对应的是发件人邮箱账号、收件人邮箱账号、发送邮件
        server.quit()  # 关闭连接
    except Exception:  # 如果 try 中的语句没有执行，则会执行下面的 ret=False
        ret=False
    return ret
ret=mail()
if ret:
    print("发送邮件成功")
else:
    print("发送邮件失败")