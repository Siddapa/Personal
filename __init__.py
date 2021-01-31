import threading
from time import sleep
import keyboard

from sockets.server import Server
from sockets.client import Client
from camera.video import Camera


def run_server():
    server = Server('127.0.0.1', 54321)
    server.connect()


def capture_camera():
    camera = Camera(0, Client('127.0.0.1', 54321))
    camera.capture()

if __name__ == '__main__':
    x = threading.Thread(target=run_server)
    y = threading.Thread(target=capture_camera)
    x.start()
    y.start()