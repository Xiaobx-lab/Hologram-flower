import time

import cv2
import paho.mqtt.client as mqtt
import vlc
from screeninfo import get_monitors

from setting import loading_animation_path, melting_animation_path, holo_melting_animation
from state_holder import state
from utils import extract_main_colors, find_closest_color
import numpy as np


def on_message(client, userdata, message):

    global state
    global image_path
    global playback_speed

    if message.topic == "test/state":
        state = f"{message.payload.decode()}"
    if message.topic == "IMAGE_PATH":
        image_path = f"{message.payload.decode()}"
    if message.topic == "speed":
        playback_speed = float(f"{message.payload.decode()}")

    print(f"received message: {message.payload.decode()} on topic {message.topic}")

def state_machines():

    all_video_player_upload_again()
    all_video_player_loading()
    all_video_player_melting()
    all_video_player_blender()


def all_video_player_loading():

    cap = cv2.VideoCapture(loading_animation_path)
    monitor_width, monitor_height, new_width, new_height = set_full_screen_before(cap)

    while(state == "UPLOAD_DONE"):
        # Capture frame-by-frame
        print(state)
        ret, frame = cap.read()
        if ret == True:
            background = set_full_screen_middle(frame,new_width,new_height,monitor_height,monitor_width)
            # Display the resulting frame
            cv2.imshow('Frame', background)

            # Press Q on keyboard to exit
            if cv2.waitKey(25) & 0xFF == ord('q'):
                break
        # Break the loop
        else: 
            cap = cv2.VideoCapture(loading_animation_path)
            monitor_width, monitor_height, new_width, new_height = set_full_screen_before(cap)

def all_video_player_melting():
    print(state)
    cap = cv2.VideoCapture("vids/holo_melting.mp4")
    monitor_width, monitor_height, new_width, new_height = set_full_screen_before(cap)

    if(state == "MELTING"):
        # Capture frame-by-frame
        while True:
            ret, frame = cap.read()
            if ret == True:
                background = set_full_screen_middle(frame,new_width,new_height,monitor_height,monitor_width)
                # Display the resulting frame
                cv2.imshow('Frame', background)
                if cv2.waitKey(25) & 0xFF == ord('q'):
                    break
            else:
                break

def all_video_player_blender():
    print(state)
    global playback_speed
    colors = extract_main_colors(image_path)
    color = find_closest_color(colors,pre_rgbs)
    flower_video_name = 'res/'+'holo_'+str(color[0])+'_' + str(color[1]) +'_' + str(color[2]) + '.mp4'

    cap = cv2.VideoCapture(flower_video_name)
    monitor_width, monitor_height, new_width, new_height = set_full_screen_before(cap)
    fps = cap.get(cv2.CAP_PROP_FPS)
    # new_frame_interval = int(1000/(fps*playback_speed))


    while True:
        # Capture frame-by-frame
        ret, frame = cap.read()
        if ret == True:
            background = set_full_screen_middle(frame,new_width,new_height,monitor_height,monitor_width)

            # Display the resulting frame
            cv2.imshow('Frame', background)
            print("new_frame_interval now:", int(1000/(fps*playback_speed)))
            if cv2.waitKey(int(1000/(fps*playback_speed))) & 0xFF == ord('q'):
                break
        else:
            break

def set_full_screen_before(cap):

    frame_width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    frame_height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))

    monitor_width = get_monitors()[0].width
    monitor_height = get_monitors()[0].height

    scale = min(monitor_width / frame_width, monitor_height / frame_height)
    new_width = int(frame_width * scale)
    new_height = int(frame_height * scale)

    cv2.namedWindow('Frame', cv2.WINDOW_NORMAL)
    cv2.setWindowProperty('Frame', cv2.WND_PROP_FULLSCREEN, cv2.WINDOW_FULLSCREEN)

    return monitor_width,monitor_height,new_width, new_height

def set_full_screen_middle(frame, new_width, new_height,monitor_height,monitor_width):
    frame = cv2.resize(frame, (new_width, new_height), interpolation=cv2.INTER_LINEAR)

    background = np.zeros((monitor_height, monitor_width, 3), dtype=np.uint8)

    x_offset = (monitor_width - new_width) // 2
    y_offset = (monitor_height - new_height) // 2
    background[y_offset:y_offset + new_height, x_offset:x_offset + new_width] = frame
    return background

def all_video_player_upload_again():
    print(state)
    cap = cv2.VideoCapture('vids/holo-QRCode.mp4')
    monitor_width,monitor_height,new_width, new_height = set_full_screen_before(cap)

    while (state == "UPLOAD_AGAIN"):
        # Capture frame-by-frame
        ret, frame = cap.read()
        if ret == True:
            background = set_full_screen_middle(frame,new_width,new_height,monitor_height,monitor_width)
            cv2.imshow('Frame', background)
            if cv2.waitKey(25) & 0xFF == ord('q'):
                break
        else:
            cap = cv2.VideoCapture(r"vids/holo-QRCode.mp4")
            monitor_width, monitor_height, new_width, new_height = set_full_screen_before(cap)



if __name__ == "__main__":
    state = "UPLOAD_AGAIN"
    playback_speed = 0.5
    pre_rgbs = [[0, 35, 0], [11, 26, 77], [20, 5, 77], [33, 35, 6], [235, 39, 256], [256, 0, 9], [256, 0, 40],
                [256, 53, 112]]

    client = mqtt.Client()
    client.on_message = on_message
    client.connect("localhost", 1883, 60)

    client.subscribe("test/state")
    client.subscribe("IMAGE_PATH")
    client.subscribe("speed")

    client.loop_start()


    while True:

        state_machines()
        state = "UPLOAD_AGAIN"