import time

import cv2
import paho.mqtt.client as mqtt
import vlc
from screeninfo import get_monitors
import pygame

from music_thread import music_play_thread
from setting import loading_animation_path, melting_animation_path, holo_melting_animation

from utils import extract_main_colors, find_closest_color
import numpy as np


def state_machines():

    all_video_player_upload_again()
    all_video_player_loading()
    all_video_player_melting()
    all_video_player_blender()

def on_message(client, userdata, message):

    global state
    global image_path
    global playback_speed

    if message.topic == "test/state":
        state = f"{message.payload.decode()}"
        # music_melting_thread.state = state
        # music_loading_thread.state = state
        # music_upload_thread.state = state
    if message.topic == "IMAGE_PATH":
        image_path = f"{message.payload.decode()}"
    if message.topic == "speed":
        playback_speed = float(f"{message.payload.decode()}")

    print(f"received message: {message.payload.decode()} on topic {message.topic}")

def all_video_player_upload_again():

    global music_upload_thread
    music_upload_thread= music_play_thread('SFX/upload.wav')
    music_upload_thread.state = "UPLOAD_AGAIN"
    music_upload_thread.start()

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

def all_video_player_loading():

    cap = cv2.VideoCapture(loading_animation_path)
    monitor_width, monitor_height, new_width, new_height = set_full_screen_before(cap)

    music_upload_thread.state = "UPLOAD_DONE"
    music_upload_thread.join()

    global music_loading_thread
    music_loading_thread = music_play_thread('SFX/loading.wav')
    music_loading_thread.state = "UPLOAD_DONE"
    music_loading_thread.start()

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
        music_loading_thread.state = "MELTING"
        music_loading_thread.join()

        global music_melting_thread
        music_melting_thread = music_play_thread('SFX/melting.mp3')
        music_melting_thread.state = "MELTING"
        # music_melting_thread.state = "MEL"
        music_melting_thread.start()

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
    flower_video_name = 'holo_'+str(color[0])+'_' + str(color[1]) +'_' + str(color[2]) + '.mp4'

    music_rendering_thread = music_play_thread('SFX/growing.wav')
    music_rendering_thread.state = "RENDERING"
    music_melting_thread.state = "RENDERING"
    music_melting_thread.join()
    music_rendering_thread.start()


    cap = cv2.VideoCapture('flower/'+flower_video_name)
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
            # print("new_frame_interval now:", int(1000/(fps*playback_speed)))
            if cv2.waitKey(int(1000/(fps*playback_speed))) & 0xFF == ord('q'):
                break
        else:
            # play audio after flower
            # music_rendering_thread.state = "RENDERING_DONE"
            # music_rendering_thread.join()
            # filename = 'SFX/bingo.wav'
            # pygame.mixer.init()
            # pygame.mixer.music.load(filename)
            # pygame.mixer.music.play()
            # while pygame.mixer.music.get_busy() == True:
            #     continue
            # break
            music_rendering_thread.state = "RENDERING_DONE"
            music_rendering_thread.join()

            music_ending_thread = music_play_thread('SFX/end.mp3')
            music_ending_thread.state = "ENDING"
            music_ending_thread.start()

            cap = cv2.VideoCapture('res/'+flower_video_name)
            monitor_width, monitor_height, new_width, new_height = set_full_screen_before(cap)
            fps = cap.get(cv2.CAP_PROP_FPS)
            # new_frame_interval = int(1000/(fps*playback_speed))

            while True:
                # Capture frame-by-frame
                ret, frame = cap.read()
                if ret == True:
                    background = set_full_screen_middle(frame, new_width, new_height, monitor_height, monitor_width)
                    # Display the resulting frame
                    cv2.imshow('Frame', background)
                    if cv2.waitKey(int(1000 / (fps * 1))) & 0xFF == ord('q'):
                        break
                else:
                    music_ending_thread.state = "ENDING_DONE"
                    break
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





if __name__ == "__main__":

    state = "UPLOAD_AGAIN"



    playback_speed = 0.5
    pre_rgbs = [[16,13,50],[22,3,21],[27,152,110],[49,15,193],[71,224,91],[90,38,16],[108,226,223],[111,87,116],[117,8,0],[126,219,116],[139,141,216],[178,255,59],[190,38,172],[193,110,20],[221,255,216],[228,79,76],[235,221,104],[255,160,217]]




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