import cv2
import os
import numpy as np
import math

import vlc
from moviepy.video.io.ImageSequenceClip import ImageSequenceClip

from setting import melting_animation_path


def extract_main_colors(image_path, num_colors = 1):

    image = cv2.imread(image_path)
    image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
    pixels = image.reshape(-1, 3).astype(np.float32)  # transfer to one-dimention
    # K-Means
    criteria = (cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_MAX_ITER, 10, 1.0)
    _, labels, centers = cv2.kmeans(pixels, num_colors, None, criteria, 10, cv2.KMEANS_RANDOM_CENTERS)
    colors = centers.astype(int)
    if num_colors == 1 :  # only return one main color
        return colors[0]

    return colors


# def melt_image_animation(image_path, fps=30, duration=20):
#     print('Begin melting!')
#     image = cv2.imread(image_path)
#     height, width, _ = image.shape
#     # cv2.namedWindow('Animation', cv2.WINDOW_NORMAL)
#     # cv2.setWindowProperty('Animation', cv2.WND_PROP_FULLSCREEN, cv2.WINDOW_FULLSCREEN)
#
#     frames = []
#     for i in range(fps * duration):
#         # 计算旋转角度和消融比例
#         angle = i / (fps * duration) * 360
#         melt_ratio = i / (fps * duration)
#
#         # 旋转图像
#         M = cv2.getRotationMatrix2D((width / 2, height / 2), angle, 1)
#         rotated_image = cv2.warpAffine(image, M, (width, height))
#
#         # 缩放图像
#         scale = 1 - melt_ratio
#         scaled_image = cv2.resize(rotated_image, None, fx=scale, fy=scale)
#
#         # 计算缩放后的图像位置
#         x_offset = int((width - scaled_image.shape[1]) / 2)
#         y_offset = int((height - scaled_image.shape[0]) / 2)
#
#         # 创建背景并将缩放后的图像放置在中心位置
#         background = np.zeros((height, width, 3), dtype=np.uint8)
#         background[y_offset:y_offset+scaled_image.shape[0], x_offset:x_offset+scaled_image.shape[1]] = scaled_image
#
#         frames.append(background)
#         # cv2.imshow('Animation', background)
#         # cv2.waitKey(1)
#
#     clip = ImageSequenceClip(frames, fps=fps)
#     clip.write_videofile('melting_animation.mp4')
#     flag = True
#     melting_animation_relative_path = "videos/melting_animation.mp4"
#     # cv2.destroyAllWindows()
#     print('Finished melting!')
#     return melting_animation_relative_path

def melt_image_animation(image_path, fps=30, duration=10):
    image = cv2.imread(image_path)
    height, width, _ = image.shape
    background = np.zeros((height, width, 3), dtype=np.uint8)

    frames = []
    for i in range(fps * duration):
        # 计算旋转角度和消融比例
        angle = i / (fps * duration) * 360
        melt_ratio = i / (fps * duration)

        # 旋转图像
        M = cv2.getRotationMatrix2D((width / 2, height / 2), angle, 1)
        rotated_image = cv2.warpAffine(image, M, (width, height))

        # 缩放图像
        scale = 1 - melt_ratio
        scaled_image = cv2.resize(rotated_image, None, fx=scale, fy=scale)

        # 计算缩放后的图像位置
        x_offset = int((width - scaled_image.shape[1]) / 2)
        y_offset = int((height - scaled_image.shape[0]) / 2)

        # 创建背景并将缩放后的图像放置在中心位置
        background = np.zeros((height, width, 3), dtype=np.uint8)
        background[y_offset:y_offset+scaled_image.shape[0], x_offset:x_offset+scaled_image.shape[1]] = scaled_image

        # 转换到HSV色彩空间并减小饱和度
        hsv = cv2.cvtColor(background, cv2.COLOR_BGR2HSV)
        hsv[:, :, 1] = hsv[:, :, 1] * (1.0 - melt_ratio)
        color_faded_image = cv2.cvtColor(hsv, cv2.COLOR_HSV2BGR)

        frames.append(color_faded_image)
        # cv2.imshow('Animation', background)
        cv2.waitKey(1)

    clip = ImageSequenceClip(frames, fps=fps)

    melting_animation_relative_path = melting_animation_path
    clip.write_videofile(melting_animation_relative_path)
    # cv2.destroyAllWindows()
    return melting_animation_relative_path


# 计算两个 RGB 值之间的欧几里得距离
def calculate_distance(rgb1, rgb2):
    r1, g1, b1 = rgb1
    r2, g2, b2 = rgb2

    distance = math.sqrt((r2 - r1) ** 2 + (g2 - g1) ** 2 + (b2 - b1) ** 2)
    return distance

# 比较一个 RGB 值和一组 RGB 值中哪个 RGB 值最接近
def find_closest_color(rgb, color_list):
    closest_color = None
    min_distance = float('inf')

    for color in color_list:
        distance = calculate_distance(rgb, color)

        if distance < min_distance:
            min_distance = distance
            closest_color = color

    return closest_color

def show_upLoadImage_full_screen(image_path):
    # 创建VLC实例
    instance = vlc.Instance()
    # 创建媒体播放器
    player = instance.media_player_new()
    # 加载图片文件
    media = instance.media_new_path(image_path)
    # 将媒体绑定到播放器
    player.set_media(media)
    # 设置全屏模式
    player.set_fullscreen(True)
    # 播放图片
    player.play()

    return player


if __name__ == "__main__":
    pre_rgbs = [[0,35,0],[11,26,77],[20,5,77],[33,35,6],[235,39,256],[256,0,9],[256,0,40],[256,53,112]]
    colors = extract_main_colors("bear.jpg")
    color = find_closest_color(colors,pre_rgbs)
    filename = str(color[0]) + '_' + str(color[1]) + '_' + str(color[2]) + '.avi'
    cap = cv2.VideoCapture(filename)
    print(color)

    # start_playing_video("holo_loading.mp4")
