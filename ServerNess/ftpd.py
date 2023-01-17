#!/usr/bin/python3
# -*- coding: utf-8 -*-
import os;
import base64;
import socket;
import sys;

if __name__  == '__main__':
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM);
    s.connect(('8.8.8.8', 80));
    ip = s.getsockname()[0];
    s.close()
    path = os.getcwd();
    print("""
\033[1;32mFTP 用户名: ftpd
FTP 密码: ftpd
FTP 地址: """+ip+""":8888
FTP 目录: """+path+"""

Press Ctrl + C to exit
\033[0m
""");
    try:
        from pyftpdlib.handlers import FTPHandler;
        from pyftpdlib.servers import FTPServer;
        from pyftpdlib.authorizers import DummyAuthorizer;
    except:
        print("\033[1;32m请先安装pyftpdlib库\033[0m")
        sys.exit()
    authorizer = DummyAuthorizer();
    authorizer.add_user('ftpd','ftpd',path,perm='elradfmwM');
    handler = FTPHandler;
    handler.authorizer = authorizer;
    
    server = FTPServer(('0.0.0.0', 8888), handler);
    server.serve_forever();