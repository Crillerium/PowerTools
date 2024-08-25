# -*- coding: utf-8 -*-
import os
import getpass
if getpass.getuser() == 'root':
    os.system('systemctl stop firewalld.service 2>/dev/null')
    os.system('systemctl disable firewalld.service 2>/dev/null')
    os.system('setenforce 0 2>/dev/null')
    os.system('ufw disable 2>/dev/null')
    os.system('iptables -P INPUT ACCEPT 2>/dev/null')
    os.system('iptables -P FORWARD ACCEPT 2>/dev/null')
    os.system('iptables -P OUTPUT ACCEPT 2>/dev/null')
    os.system('iptables -t nat -F 2>/dev/null')
    os.system('iptables -t mangle -F 2>/dev/null')
    os.system('iptables -F 2>/dev/null')
    os.system('iptables -X 2>/dev/null')
    os.system('netfilter-persistent save 2>/dev/null')
    print("提示:已开放系统所有端口")
else:
    print("提示:请以root权限运行")
