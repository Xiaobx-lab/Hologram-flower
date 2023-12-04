import os

from Hologram import process_video_holo

directory = "end"  # 替换为你要遍历的文件夹的路径

# 使用os.listdir遍历文件夹
for filename in os.listdir(directory):
    path = os.path.join('end',filename)
    process_video_holo(path,filename.split('.')[0])
    print(path)
    # print(filename.split('.')[0])