#!/usr/bin/python
# -*- coding: UTF-8 -*-

import os, sys, stat

# 假定 /tmp/foo.txt 文件存在，设置文件可以通过用户组执行

os.chmod("/tmp/foo.txt", stat.S_IXGRP)

# 设置文件可以被其他用户写入
os.chmod("/tmp/foo.txt", stat.S_IWOTH)

print "修改成功!!"
