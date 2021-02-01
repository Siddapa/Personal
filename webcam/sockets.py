import socket
import keyboard
import cv2
import numpy as np
from datetime import datetime

class Client:
    HOST = ''
    PORT = 0

    def __init__(self, host, port):
        self.HOST = host
        self.PORT = port

    
    def send(self, message):
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.connect((self.HOST, self.PORT))
            while 1:
                keyboard.wait('esc')
                s.sendall(message)


class Server:
    HOST = ''
    PORT = 0


    def __init__(self, host, port):
        self.HOST = host
        self.PORT = port


    def listen(self):
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.bind((self.HOST, self.PORT))
            s.listen()
            conn, _ = s.accept()
            while 1:
                data = conn.recv(5000000) # 5 Megabytes
                nparr = np.fromstring(data, np.uint8)
                img_decode = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
                time = datetime.now().strftime('%m-%d-%Y-%H-%M-%S')
                cv2.imwrite(f'webcam/photos/{time}.jpg', img_decode)
