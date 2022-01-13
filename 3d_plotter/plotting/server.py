import socket
import pickle
import cv2 as cv
import numpy as np

from plotter import Plotter


if __name__ == '__main__':
    # Needs to run by sudo

    HOST = '127.0.0.1'
    PORT = 65432

    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.bind((HOST, PORT))
        s.listen()
        conn, addr = s.accept()
        with conn:
            contours = conn.recv(1000000) # Average file size is around 200 KB
            conn.sendall(b'Received!')
            
            contours = pickle.loads(contours)
            plotter = Plotter(contours) 
            plotter.calibrate()
            plotter.draw_image()
            