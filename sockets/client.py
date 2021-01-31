import socket
import keyboard

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
