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


class Server:
    HOST = ''
    PORT = 0


    def __init__(self, host, port):
        self.HOST = host
        self.PORT = port


    def connect(self):
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.bind((self.HOST, self.PORT))
            s.listen()
            conn, _ = s.accept()
            while 1:
                data = conn.recv(1024)
                print(f"Received {data}")
                # conn.sendall(data)
