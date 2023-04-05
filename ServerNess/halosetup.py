import os
import sys
import getpass
import socket

def color(text):
    return "\033[1;32m"+text+"\033[0m"

if getpass.getuser() == 'root':
    apply = input('这是Halo2博客简易安装程序,确认要运行吗?[yes=>运行,other=>退出]')
    if apply == 'yes':
        print(color('第一步:更新apt软件包'))
        os.system('apt update')
        os.system('apt upgrade')
        print(color('第二步:安装常用软件包'))
        os.system('apt install nginx python3 wget git curl nano')
        os.system('systemctl start nginx')
        os.system('systemctl enable nginx')
        print(color('第三步:安装Docker环境'))
        os.system('wget -qO- get.docker.com | bash')
        os.system('systemctl start docker')
        os.system('systemctl enable docker')
        print(color('第四步:安装Halo2博客前准备'))
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM);
        s.connect(('8.8.8.8', 80));
        host = s.getsockname()[0];
        s.close()
        domain = input('请输入访问域名(今后不可更改，留空则选择'+ip+'): ')
        if domain == '':
            domain = ip
        port = input('请输入Halo将要占用的端口: ')
        username = input('请输入Halo超级管理员账号(不可大写): ')
        password = input('请输入'+username+'的密码: ')
        print('准备就绪,你的Halo博客访问地址将为http://'+ip+':'+port)
        print(color('第五步:安装Halo2博客程序'))
        command = 'docker run -it -d --name halo -p '+port+':8090 -v ~/.halo2:/root/.halo2 halohub/halo:2.4.0 --halo.external-url=https://'+domain+':'+port+'/ --halo.security.initializer.superadminusername='+username+' --halo.security.initializer.superadminpassword='+password
        os.system(command)
        print(color('安装完成,脚本已自动退出'))
        sys.exit()
else:
    print(color('请使用root用户执行Halo安装脚本!'))