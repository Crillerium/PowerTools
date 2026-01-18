# PowerTools
A Toolbox that has lots of amazing features.  
充满无限可能的强力工具箱。  
**(README中仅详细介绍部分供大众使用的工具)**

## 1.File Guard 「文件守卫」
### 功能
(与Android Termux搭配使用体验更佳)  
File Guard 可以在脚本所在目录下生成专属文件夹,  
并支持双空间双密码,互不干扰  
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
Server.py 基于官方开源的http.server进行修改
### 使用
直接运行
```
python3 server.py 
```
(参数配置与http.server相同)
### 特性
美化原版http.server输出, 自动按照状态码为输出信息标记颜色，资源问题一眼洞察！
## 其他项目
`ServerNess/ftpd.py` 在本机运行一个FTP服务端的脚本  
`ServerNess/openport.py` 一键放行使用端口的脚本  
`ServerNess/halosetup.py` 可以安装 Halo 博客的一键脚本  
`GeneEncrypt/encrypt.py` 按照 “嘌呤嘧啶” 对文本进行加解密的脚本  
`OhMyData/easyjson.db` 更加简单的基于json的数据库

## 2.CourseSchedule 「课程表助手」
### 介绍
面向 CSUST 教务系统，模拟登录并展示验证码，支持自动重试；抓取课表页面并解析为 Markdown 表格与详细信息。
### 依赖
```
pip install requests beautifulsoup4 pillow
```
### 使用
作为模块使用示例（在交互式或脚本中）：
```
from CourseSchedule.Courseschedule_v1 import CSUSTSystem

sys = CSUSTSystem()
if sys.auto_login_with_retry("学号", "密码"):
	courses = sys.get_course_schedule_directly(academic_year="2025-2026-1")
	sys.format_course_schedule_markdown(courses)
```
验证码会弹窗显示，并在当前目录保存为 verify_code.png。

## 3.GeneEncrypt 「嘌呤嘧啶加解密」
### 介绍
将文本按二进制分组映射为“嘌/呤/嘧/啶”，支持加密与解密，示例脚本会直接演示。
### 使用
```
python GeneEncrypt/encrypt.py
```
也可在其他脚本中调用：`encrypt(text)` 与 `decrypt(cc_text)`。

## 4.ImageResizer 「图片背景扩展」
### 介绍
将图片居中铺底，扩展到指定画布尺寸（透明背景），适合统一头像或贴图尺寸。
### 依赖
```
pip install pillow
```
### 使用
```
python ImageResizer/main.py <输入文件> <输出文件> [宽度] [高度]
示例: python ImageResizer/main.py input.png output.png 2000 2000
```

## 5.m3u8/ 媒体与下载
### 5.1 音乐检索下载器（m3u8/dl.py）
- 介绍：输入关键词检索音频，选择序号即可下载 mp3。
- 依赖：
```
pip install requests
```
- 使用：
```
python m3u8/dl.py
```
按提示输入关键词与序号后自动保存文件。

### 5.2 FFmpeg 封装合并（m3u8/m3u8.py）
- 介绍：对流媒体（如 m3u8/ts）进行封装合并为 mp4。
- 前置：本机需安装并配置 ffmpeg 到 PATH。
- 使用：
```
python m3u8/m3u8.py <输入文件> [输出文件]
示例: python m3u8/m3u8.py input.ts output.mp4
```

## 6.OhMyData 「轻量 JSON 数据库」
### 介绍
简洁的二维表存储，提供 `table/insert/fetch/delete/save` 等操作，适合小型数据快速记录。
### 使用示例
```
from OhMyData.easydb import EasyDB

db = EasyDB('data.json')
db.table(['id', 'name'])
db.insert([1, 'Alice'])
print(db.fetch_all())
print(db.fetch({'name': 'Alice'}))
db.save()
```
依赖：标准库，无需额外安装。

## 7.ServerNess/ 工具集
### ftpd.py 本机 FTP 服务端
#### 依赖
```
pip install pyftpdlib
```
#### 使用
```
python ServerNess/ftpd.py
```
默认用户/密码均为 ftpd，端口 8888，目录为当前工作路径。

### openport.py 一键放行端口
#### 说明
在 Linux root 环境下关闭防火墙策略，开放所有端口（请谨慎使用）。
#### 使用
```
sudo python ServerNess/openport.py
```

### halosetup.py Halo 博客一键安装
#### 说明
在 Debian/Ubuntu + Docker 环境下交互式安装 Halo 2，按提示输入域名、端口与管理员信息。
#### 使用
```
sudo python ServerNess/halosetup.py
```

### BirdClock.py 定时执行器
#### 依赖
```
pip install fire
```
#### 使用
```
python ServerNess/BirdClock.py run --time=HH:MM --task="要执行的命令"
示例: python ServerNess/BirdClock.py run --time=23:30 --task="echo hello"
```

### chmod.py 权限示例脚本
演示修改 `/tmp/foo.txt` 权限（适用于类 Unix 环境）。

### left.py 日期倒计时
计算距离目标日期的天数，默认目标为 2025-01-01；可按需修改脚本内日期后运行。

### spell.py 简易回显
循环读取输入并回显，输入 `quit` 退出。

### append_bashrc.py 追加 .bashrc
在类 Unix 环境下将用户输入追加到 `~/.bashrc`，用于快捷添加环境变量或别名。

### server.py 彩色静态服务器
增强版 http.server，按状态码高亮输出，便于快速定位资源问题。
```
python ServerNess/server.py
```

## 8.TypeWriter 「自动打字机」
### 介绍
收集多行输入，5 秒倒计时后自动在当前焦点窗口打字。
### 依赖
```
pip install pyautogui
```
### 使用
```
python TypeWriter/typewriter.py
逐行输入待打字内容，最后输入 ok 开始
```
注意：请将光标焦点置于目标编辑器，脚本执行期间不要切换窗口。
 
