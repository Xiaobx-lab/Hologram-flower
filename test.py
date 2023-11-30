import cv2
from screeninfo import get_monitors
import numpy as np

video = cv2.VideoCapture('vids/holo-QRCode.mp4')

frame_width = int(video.get(cv2.CAP_PROP_FRAME_WIDTH))
frame_height = int(video.get(cv2.CAP_PROP_FRAME_HEIGHT))

monitor_width = get_monitors()[0].width
monitor_height = get_monitors()[0].height

scale = min(monitor_width/frame_width, monitor_height/frame_height)
new_width = int(frame_width*scale)
new_height = int(frame_height*scale)

cv2.namedWindow('Video', cv2.WINDOW_NORMAL)
cv2.setWindowProperty('Video', cv2.WND_PROP_FULLSCREEN, cv2.WINDOW_FULLSCREEN)

while True:
    ret, frame = video.read()

    if ret == True:
        # 根据视频的原始长宽比调整帧的大小
        frame = cv2.resize(frame, (new_width, new_height), interpolation = cv2.INTER_LINEAR)

        # 创建一个与显示器大小相同的黑色背景
        background = np.zeros((monitor_height, monitor_width, 3), dtype=np.uint8)

        # 将帧放在背景的中央
        x_offset = (monitor_width - new_width) // 2
        y_offset = (monitor_height - new_height) // 2
        background[y_offset:y_offset+new_height, x_offset:x_offset+new_width] = frame

        cv2.imshow('Video', background)

        if cv2.waitKey(25) & 0xFF == ord('q'):
            break
    else:
        break

# 释放视频和关闭所有窗口
video.release()
cv2.destroyAllWindows()