import requests
import sys

def download(url, local_filename):
    with requests.get(url, stream=True) as response:
        # 确保请求成功
        response.raise_for_status()
        
        # 打开本地文件进行写入
        with open(local_filename, 'wb') as file:
            # 按块写入文件，减少内存使用
            for chunk in response.iter_content(chunk_size=8192):
                # 如果chunk是None，跳过
                if chunk:
                    file.write(chunk)

    print(f"文件已下载并保存为：{local_filename}")

# 1. 获取用户输入
query = input("请输入查询关键词: ")

# 2. 发送请求到API
url = "https://api.csm.sayqz.com/search"
params = {'keywords': query}
response = requests.get(url, params=params)

# 3. 将获取的数据转为字典
responseMap = response.json()

# 4. 遍历responseMap中的'result'下的'songs'列表
if 'result' in responseMap and 'songs' in responseMap['result']:
    songs = responseMap['result']['songs']
    i = 1
    for song in songs:
        # 这里留空，你可以添加你需要的代码
        # 例如，打印每首歌曲的信息
        print("["+str(i)+"]","ID:",song['id'],"歌名:",song['name'],"歌手:",song['artists'][0]['name'])
        i+=1
else:
    print("没有找到歌曲信息。")
    sys.exit()

order = input('请输入序号:')
url = "https://api.csm.sayqz.com/song/url"
params = {'id': responseMap['result']['songs'][int(order)-1]['id']}
response = requests.get(url, params=params)
download(response.json()['data'][0]['url'],responseMap['result']['songs'][int(order)-1]['name']+" - "+responseMap['result']['songs'][int(order)-1]['artists'][0]['name']+".mp3")