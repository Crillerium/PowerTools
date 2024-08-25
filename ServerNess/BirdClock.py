import time
import datetime
import sys
import fire
import os

class ScheduleTask:
    def __init__(self, time, task):
        self.time = time
        self.task = task

    def run(self):
        # 将时间字符串转换为datetime.time对象
        run_time = datetime.datetime.strptime(self.time, '%H:%M').time()

        # 获取当前时间
        now = datetime.datetime.now()

        # 计算执行任务的时间点
        next_run = now.replace(hour=run_time.hour, minute=run_time.minute, second=0, microsecond=0)
        if next_run < now:
            # 如果时间已经过了，就设置到下一天的这个时间
            next_run += datetime.timedelta(days=1)

        # 计算等待时间
        to_wait_time = (next_run - now).total_seconds()

        # 打印等待时间
        print(f"任务将在 {to_wait_time} 秒后执行。")

        # 等待直到执行时间
        time.sleep(to_wait_time)

        # 执行任务
        print(f"执行任务: {self.task}")
        os.system(self.task)

if __name__ == '__main__':
    fire.Fire(ScheduleTask)
