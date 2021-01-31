import socket

class Server:
    HOST = ''
    PORT = 0
    conn = None


    def __init__(self, host, port):
        self.HOST = host
        self.PORT = port


    def connect(self):
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.bind((self.HOST, self.PORT))
            s.listen()
            self.conn, addr = s.accept()
            
    
    def receive(self):
        while 1:
            with self.conn:
                data = conn.recv(1024)
                conn.sendall(data)


server = Server('127.0.0.1', 54321)
server.connect()
server.receive()
