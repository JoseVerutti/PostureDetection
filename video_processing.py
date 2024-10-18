import cv2
from PIL import Image, ImageTk

class VideoProcessor:
    def __init__(self):
        self.cap = cv2.VideoCapture(0)
        
    def get_frame(self):
        ret, frame = self.cap.read()
        if ret:
            frame = cv2.flip(frame, 1)
            frame = cv2.resize(frame, (300, 220))
            # Convertir el frame a RGB (OpenCV usa BGR por defecto)
            frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            # Crear una imagen PIL
            image = Image.fromarray(frame_rgb)
            return image
        return None
        
    def release(self):
        self.cap.release()