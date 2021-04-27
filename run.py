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

def recover(st): 
    codes = {"ZERO":0,"ONE":1,"TWO":2,"THREE":3,"FOUR":4,"FIVE":5,"SIX":6,"SEVEN":7,"EIGHT":8,"NINE":9}
    final = ""
    jump_flag = False
    for index, char in enumerate(st):
        jump_flag = False
        for i in range(index, 6):
            if jump_flag == True:
                break
            tester = st[int(index): int(index) + int(i)]
            for key in codes.keys():
                accuracy = 0
                for test_char in tester:
                    if test_char in key:
                        accuracy += 1
                if accuracy == len(key):
                    final += str(codes[key])
                    jump_flag = True
    print(final)
    return final

def 

if __name__ == '__main__':
    recover("NEOTWONEINEIGHTOWSVEEN")
