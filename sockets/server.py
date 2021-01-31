import socket

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
            conn, addr = s.accept()
            while 1:
                data = conn.recv(1024)
                print(f"Received {data}")
                # conn.sendall(data)
