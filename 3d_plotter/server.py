from connections import Server


"""
File to be run on the 3D printer and will await for new files
Hosting IP is set the ip of the device
"""
if __name__ == '__main__':
    server = Server()
    server.await_receive()
    server.draw()
