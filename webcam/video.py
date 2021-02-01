import cv2

class Camera:
    cam = None
    client = None

    def __init__(self, id, client):
        self.cam = cv2.VideoCapture(id)
        self.client = client

    def capture(self):
        self.client.send(b'hello')
    
    def collapse(self):
        cv2.release()
        cv2.destroyAllWindows()