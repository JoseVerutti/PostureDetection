import tkinter as tk
from tkinter import Label, Button
from PIL import ImageTk
from video_processing import VideoProcessor
from posture_detection import PostureDetector
from ui_components import create_main_window, create_main_frame, create_video_label, create_result_label
from popup_manager import PopupManager
from constants import BEIGE_COLOR, BUTTON_STYLE

class MainApplication:
    def __init__(self, root):
        self.root = root
        self.detection_active = True
        
        create_main_window(root)
        self.main_frame = create_main_frame(root)
        self.video_label = create_video_label(self.main_frame)
        self.result_label = create_result_label(self.main_frame)
        
        self.video_processor = VideoProcessor()
        self.posture_detector = PostureDetector()
        self.popup_manager = PopupManager(root)
        
        self.create_buttons()
        self.update_frame()
        
        # Mostrar el popup de postura al inicio
        self.root.after(1000, self.popup_manager.show_postura_popup)
        
    def create_buttons(self):
        self.toggle_button = Button(
            self.main_frame, 
            text="Detener detección", 
            command=self.toggle_detection, 
            **BUTTON_STYLE
        )
        self.toggle_button.pack(pady=10)
        
    def toggle_detection(self):
        self.detection_active = not self.detection_active
        self.toggle_button.config(text="Detener detección" if self.detection_active else "Iniciar detección")
        
    def update_frame(self):
        frame = self.video_processor.get_frame()
        if frame is not None:
            if self.detection_active:
                processed_frame, posture, confidence = self.posture_detector.process_frame(frame)
                self.result_label.config(text=f"Postura detectada: {posture}, Confianza: {confidence:.2f}")
                self.popup_manager.check_posture(posture)
            else:
                processed_frame = frame
                posture = "No detectada"
                self.result_label.config(text="Detección en pausa")
                self.popup_manager.check_posture(posture)
            
            photo = ImageTk.PhotoImage(processed_frame)
            self.video_label.config(image=photo)
            self.video_label.image = photo
        
        self.root.after(10, self.update_frame)
        
    def on_closing(self):
        self.video_processor.release()
        self.root.destroy()

if __name__ == "__main__":
    root = tk.Tk()
    app = MainApplication(root)
    root.protocol("WM_DELETE_WINDOW", app.on_closing)
    root.mainloop()