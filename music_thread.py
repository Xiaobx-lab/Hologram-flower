import threading
import time

import pygame

class music_play_thread(threading.Thread):
    def __init__(self, audio_path):
        super().__init__()
        self.audio_path = audio_path
        self.state  = None

    def run(self, ):
        filename = self.audio_path
        if self.state == "MELTING":
            # play once: melting
            pygame.mixer.init()
            pygame.mixer.music.load(filename)
            pygame.mixer.music.play(loops=-1)
            while self.state == "MELTING":
                time.sleep(1)
                pass
            pygame.mixer.music.stop()
            time.sleep(1)
        elif self.state == "UPLOAD_AGAIN":
            # 循环播放
            pygame.mixer.init()
            pygame.mixer.music.load(filename)
            pygame.mixer.music.play(loops=-1)
            while self.state == "UPLOAD_AGAIN":
                time.sleep(1)
                pass
            pygame.mixer.music.stop()
            time.sleep(1)
        elif self.state == "UPLOAD_DONE":
            pygame.mixer.init()
            pygame.mixer.music.load(filename)
            pygame.mixer.music.play(loops=-1)
            while self.state == "UPLOAD_DONE":
                time.sleep(1)
                pass
            pygame.mixer.music.stop()
            time.sleep(1)
        elif self.state == "RENDERING":
            pygame.mixer.init()
            pygame.mixer.music.load(filename)
            pygame.mixer.music.play(loops=-1)
            while self.state == "RENDERING":
                time.sleep(1)
                pass
            pygame.mixer.music.stop()
            time.sleep(1)
