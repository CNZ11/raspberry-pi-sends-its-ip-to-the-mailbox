#!/bin/bash
while :
do
	ping -c 2 www.baidu.com  &>/dev/null
	[ $? -eq 0 ] && break
done

a=`ifconfig wlan0 | grep broadcast`
python3 /home/cnz/myrestart_sh/report_ip_mail/report_ip_mail.py "wlan0:$a"
echo "ok"

