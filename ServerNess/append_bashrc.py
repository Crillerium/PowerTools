import os

# 获取用户的home目录
home_dir = os.path.expanduser('~')

# 定义.bashrc文件的路径
bashrc_path = os.path.join(home_dir, '.bashrc')

# 提示用户输入要追加的内容
user_input = input("请输入要追加到.bashrc的内容: ")

# 检查.bashrc文件是否存在
if not os.path.isfile(bashrc_path):
    print(".bashrc文件不存在，将创建一个新的.")
    with open(bashrc_path, 'w') as file:
        file.write("# 新创建的.bashrc文件\n")
else:
    print(".bashrc文件已存在.")

# 追加用户输入的内容到.bashrc文件
with open(bashrc_path, 'a') as file:
    file.write('\n' + user_input + '\n')

print("内容已追加到.bashrc文件.")
