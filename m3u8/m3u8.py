import sys
import os
print(sys.argv)
try:
    in_put = sys.argv[1] if len(sys.argv) >= 2 else sys.exit()
    out_put = sys.argv[2] if len(sys.argv) >= 3 else 'output.mp4'
    os.system('ffmpeg -i '+in_put+' -vcodec copy -acodec copy -absf aac_adtstoasc '+out_put) #使用ffmpeg命令行工具进行转换
except Exception as e:
    print(e)
