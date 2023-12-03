import cv2
import numpy as np
from moviepy.editor import ImageSequenceClip

def melt_image_animation1(image_path, fps=30, duration=10):
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

        frames.append(background)
        # cv2.imshow('Animation', background)
        cv2.waitKey(1)

    clip = ImageSequenceClip(frames, fps=fps)

    melting_animation_relative_path = "output.mp4"
    clip.write_videofile(melting_animation_relative_path)
    # cv2.destroyAllWindows()
    return melting_animation_relative_path

import cv2
import numpy as np
from moviepy.editor import ImageSequenceClip

def melt_image_animation(image_path, fps=30, duration=10):
    image = cv2.imread(image_path)
    height, width, _ = image.shape

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
        scaled_image = cv2.resize(rotated_image, None, fx=scale, fy=scale,interpolation=cv2.INTER_CUBIC)

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

    clip = ImageSequenceClip(frames, fps=fps)

    melting_animation_relative_path = image_path.split('.')[0] + '_melted.mp4'
    clip.write_videofile(melting_animation_relative_path)

    return melting_animation_relative_path

if __name__ == "__main__":
    melt_image_animation("bear.jpg")