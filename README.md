# PowerTools
A Toolbox that has lots of amazing features.  
充满无限可能的强力工具箱。  

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
