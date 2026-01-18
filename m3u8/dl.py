import requests
import sys

def download(url, local_filename):
    with requests.get(url, stream=True) as response:
        response.raise_for_status()
        with open(local_filename, 'wb') as file:
            # 按块写入文件，减少内存使用
            for chunk in response.iter_content(chunk_size=8192):
                # 如果chunk是None，跳过
                if chunk:
                    file.write(chunk)

    print(f"文件已下载并保存为：{local_filename}")
query = input("请输入查询关键词: ")
url = "https://api.csm.sayqz.com/search"
params = {'keywords': query}
response = requests.get(url, params=params)
responseMap = response.json()

if 'result' in responseMap and 'songs' in responseMap['result']:
    songs = responseMap['result']['songs']
    i = 1
    for song in songs:
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