import cv2

class Camera:
    cam = None
    client = None

    def __init__(self, id, client):
        self.cam = cv2.VideoCapture(id)
        self.client = client

    def capture(self):
        _, frame = self.cam.read()
        byte_frame = cv2.imencode('.jpg', frame)[1].tostring()
        self.client.send(byte_frame)
    
    def collapse(self):
        cv2.release()
        cv2.destroyAllWindows()