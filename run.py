import threading
from time import sleep
import keyboard
import sys

from webcam.sockets import Server
from webcam.sockets import Client
from webcam.video import Camera


def run_server():
    server = Server('127.0.0.1', 54321)
    server.listen()


def capture_camera():
    camera = Camera(0, Client('127.0.0.1', 54321))
    camera.capture()


def halt():
    while 1:
        if keyboard.is_pressed('ctrl+c'):
            raise KeyboardInterrupt

if __name__ == '__main__':
    x = threading.Thread(target=run_server)
    y = threading.Thread(target=capture_camera)
    z = threading.Thread(target=halt)
    x.start()
    y.start()
    z.start()
