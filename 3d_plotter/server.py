from connections import Server


if __name__ == '__main__':
    server = Server()
    server.await_receive()
    server.display_contours()