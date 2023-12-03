import time
import tkinter as tk
import paho.mqtt.client as mqtt

from Hologram import process_video_holo
from utils import melt_image_animation


def on_message(client, userdata, message):

    global state
    global image_path

    if message.topic == "test/state":
        state = f"{message.payload.decode()}"
    if message.topic == "IMAGE_PATH":
        image_path = f"{message.payload.decode()}"

    print(f"received message: {message.payload.decode()} on topic {message.topic}")

def melting_process():
    # print(state)
    while(state != "UPLOAD_DONE"):
        # print(state)
        pass
    if(state == "UPLOAD_DONE") :
        print("BEGIN MELTING")
        melting_animation_path = melt_image_animation(image_path)
        process_video_holo(melting_animation_path, "melting")
        client.publish("test/state", "MELTING")
        time.sleep(2)
        # state = "UPLOAD_AGAIN"


if __name__ == "__main__":
    state = "UPLOAD_AGAIN"
    client = mqtt.Client()
    client.on_message = on_message
    client.connect("localhost", 1883, 60)
    client.subscribe("test/state")
    client.subscribe("IMAGE_PATH")
    client.loop_start()

    while True:
        melting_process()
        # state = "UPLOAD_AGAIN"
