import socket

class Client:
    HOST = ''
    PORT = 0

    def __init__(self, host, port):
        self.HOST = host
        self.PORT = port

    
    def send(self, message):
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.connect((HOST, PORT))
            s.sendall(message)
            data = s.recv(1024)
