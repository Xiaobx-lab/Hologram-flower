import subprocess

# 定义你的python文件列表
python_files = ["upLoad_publisher.py", "state_publisher.py", "video_player_and_subscriber.py", "speed_calculate.py"]

# 创建一个空列表来保存子进程
processes = []

for python_file in python_files:
    # 使用subprocess.Popen来启动每一个python文件
    process = subprocess.Popen(["python", python_file])
    processes.append(process)

for process in processes:
    # 使用wait()函数等待每个进程完成
    process.wait()