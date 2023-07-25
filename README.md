# PowerTools
A Toolbox that has lots of amazing features.  
充满无限可能的强力工具箱。  
**(README中仅详细介绍部分好用的的工具)**

## 1.File Guard 「文件守卫」
### 功能
(与Android Termux搭配使用体验更佳)  
File Guard 可以在其所在目录下生成保密文件夹,  
且支持双空间双密码,互不干扰，工作生活两不误(doge),  
可根据密码在对应空间中启动ftp服务,防止上层目录文件泄露  
### 使用
1. 下载代码并cd至FileGuard文件夹;  
2. 安装依赖:
```
pip install pyftpdlib
```  
3. 运行命令:
```
python guard.py
```
4. 根据提示内容输入不同的密码;  
5. 重新运行命令并输入密码即可开始使用.

## Server.py 静态WEB服务器
### 介绍
Server.py 是基于官方开源的http.server进行修改的上位脚本
### 使用
直接运行
```
python3 server.py 
```
(参数配置与http.server相同)
### 特性
简化原版http.server输出, 自动按照状态码为输出信息标记颜色，资源问题一眼洞察！
## 其他项目

