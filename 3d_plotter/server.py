from connections import Server


if __name__ == '__main__':
    server = Server('127.0.0.1', 65432)
    server.await_receive()
    server.display_contours()