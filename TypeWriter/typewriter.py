import pyautogui as pag
import time

if __name__=="__main__":
    totype = ""
    while True:
        text = input()
        if text == "ok":
            break
        elif totype=="":
            totype = totype+text
        else:
            totype = totype+"\n"+text
    if totype == "ok":
        exit(0)
    else:
        print("任务将在五秒后开启")
        for i in range(5,0,-1):
            print(i)
            time.sleep(1)
        print("任务开始")
        pag.typewrite(totype, interval=0.15)
        print("任务完成")