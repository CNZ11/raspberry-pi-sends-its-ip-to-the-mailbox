[TOC]

# 0. 前言：

由于我的树莓派刷了ubuntu20 LTS,每次使用又都是不插网线的，连接手机热点，电脑ssh来登录使用（因为没有便携显示屏）

大家都知道使用ssh连接需要知道树莓派的ip，如果是连接自己手机热点还好，部分品牌手机可以直接看到连接设备的ip

但是我的MIUI13不支持，这里大家可以手机下载终端模拟器，输入ip neight命令就可以看到连接设备的ip了

如果以后连接其他网络，又进不去路由器后台页面，又没有办法查看ip(或者觉得手动查看ip太麻烦)，就可以树莓派开机自动发送自己的ip到邮箱

# 1. 准备工作：

## 1.1 支持SMITP/IMAP的邮箱（本文以QQ邮箱为例）

开启QQ邮箱的SMTP协议

<img src="/home/cnz/myrestart_sh/report_ip_mail/assets/image-20240318145356440.png" alt="image-20240318145356440" />

![image-20240318145409459](/home/cnz/myrestart_sh/report_ip_mail/assets/image-20240318145409459.png)

安装指引操作，然后就能获取授权码，记下来，后面有用

## 1.2 树莓派安装Python3环境

可以直接使用树莓派的包管理器`apt`来安装Python3。打开终端，输入以下命令：

```bash
sudo apt-get update  
sudo apt-get install python3
```

安装完成后，你可以通过输入`python3 --version`来检查Python3是否成功安装以及安装的版本。

# 2. 编写Python脚本

```bash
sudo touch report_ip_mail.py
sudo vim report_ip_mail.py
```

```python
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
my_sender='xxx@xx.com'  # 自己的邮箱账号
my_pass = 'xxxxx'   # 发件人邮箱密码(之前获取的授权码)
my_user='xxx@xx.com'    # 自己的邮箱账号
 
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
```

接下来可以执行命令运行该脚本，前提是你已经ssh或者屏幕等方式登录上了你的树莓派，并且已经连接上网络

```bash
python3 report_ip_mail.py
```

等待几秒看到运行结果"发送邮件成功"，在邮箱里面看邮件就可以收到ip了。

# 3. 编写shell脚本

```bash
sudo touch report_ip_mail.sh
sudo vim report_ip_mail.sh
```

```shell
#!/bin/bash
while :
do
	ping -c 2 www.baidu.com  &>/dev/null
	[ $? -eq 0 ] && break
done

a=`ifconfig wlan0 | grep broadcast`
python3 /home/cnz/myrestart_sh/report_ip_mail/report_ip_mail.py "wlan0:$a"
echo "ok"
```

上面的 `python3 /path/report_ip_mail.py "wlan0:$a`记得填写你的py文件的绝对路径

例如我的是：`/home/cnz/myrestart_sh/report_ip_mail/report_ip_mail.py `

给予权限，并运行

```
sudo chmod 777 report_ip_mail.sh
./report_ip_mail.sh
```

等待几秒看到运行结果"发送邮件成功"，在邮箱里面看邮件就可以收到ip了。

# 4. 设置开机自动运行

上面的report_ip_mail.sh和report_ip_mail.py我都放在 ` /home/cnz/myrestart_sh/report_ip_mail`这个目录下面

编辑一下系统文件

```
sudo vim /etc/rc/local
```

```
# 在exit 0之前加入如图代码
bash /home/cnz/myrestart_sh/report_ip_mail/report_ip_mail.sh
exit 0
```

重启验证

如果不行的话，参考这篇博客 https://blog.csdn.net/weixin_43772810/article/details/126760777

# 5. 效果展示

![image-20240318152014635](/home/cnz/myrestart_sh/report_ip_mail/assets/image-20240318152014635.png)