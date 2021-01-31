import cv2
from sockets.server import Server

cam = cv2.VideoCapture(0)
client = Client('127.0.0.1', 54321)

while 1:
    ret, frame = cam.read()
    print(type(frame))

    if not ret:
        print('failed')
        break

    client.send(frame)
    

cv2.release()
cv2.destroyAllWindows()