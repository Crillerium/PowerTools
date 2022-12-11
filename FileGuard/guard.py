# -*- coding: utf-8 -*-
import os;
import sys;
import base64;

def menu(path):
    print("""
\033[1;32;40mGlad to see you again, I will run in the form of FTP server.
The FTP Username: guard
The FTP Password: guard

Press Ctrl + C to exit
\033[0m
""");
    from pyftpdlib.handlers import FTPHandler;
    from pyftpdlib.servers import FTPServer;
    from pyftpdlib.authorizers import DummyAuthorizer;
    authorizer = DummyAuthorizer();
    authorizer.add_user('guard','guard',path,perm='elradfmwM');
    handler = FTPHandler;
    handler.authorizer = authorizer;
    
    server = FTPServer(('0.0.0.0', 8888), handler);
    server.serve_forever();
        
if __name__  == '__main__':
    if os.path.exists('.guard/'):
        print("\033[1;32;40mWelcome to Use File Guard again!\033[0m");
        print("\033[1;32;40mIn order to protect your file security, you need to verify your identity.\033[0m");
        put = base64.b16encode(input('\033[1;32;40mPlease enter your password: \033[0m').encode()).decode();
        f = open('.guard/.keychain','r');
        chain = f.read();
        parts = chain.split('%');
        if put == parts[0]:
            menu('.guard/realspace');
        elif put == parts[1]:
            menu('.guard/fakespace');
        else:
            print('The Key you put was wrong.');
    else:
        print("\033[1;32;40mWelcome to Use File Guard to Protect Your Code Security.\033[0m");
        print("\033[1;32;40mUse for the first time? Sign up for further use.\033[0m");
        print("\033[1;31;40mRemember: You only have the opportunity to set the password once!\033[0m");
        pwd = input('\033[1;32;40mSet Your Password: \033[0m');
        print("\033[1;32;40mTo avoid unnecessary trouble, please set another password to create a fake space\033[0m");
        fpwd = input('\033[1;32;40mSet your fake password: \033[0m');
        chain = base64.b16encode(pwd.encode()).decode()+'%'+base64.b16encode(fpwd.encode()).decode();
        os.makedirs('.guard/realspace');
        os.makedirs('.guard/fakespace');
        f = open('.guard/.keychain','x');
        f.write(chain);
        f.close();
        print("\033[1;32;40mSuccess! Now run this script again for further use.\033[0m");
