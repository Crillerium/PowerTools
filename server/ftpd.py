# -*- coding: utf-8 -*-
import os;
import base64;
import socket;

if __name__  == '__main__':
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM);
    s.connect(('8.8.8.8', 80));
    ip = s.getsockname()[0];
    path = os.getcwd();
    print("""
\033[1;32;40mThe FTP Username: pi
The FTP Password: pi
The FTP Address: """+ip+""":8888
The FTP Directory: """+path+"""

Press Ctrl + C to exit
\033[0m
""");
    try:
        from pyftpdlib.handlers import FTPHandler;
        from pyftpdlib.servers import FTPServer;
        from pyftpdlib.authorizers import DummyAuthorizer;
    except:
        os.system('pip install pyftpdlib');
    authorizer = DummyAuthorizer();
    authorizer.add_user('pi','pi',path,perm='elradfmwM');
    handler = FTPHandler;
    handler.authorizer = authorizer;
    
    server = FTPServer(('0.0.0.0', 8888), handler);
    server.serve_forever();