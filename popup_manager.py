from tkinter import Toplevel, Label, Button, messagebox
from PIL import Image, ImageTk
import time
import os
from constants import BEIGE_COLOR, BUTTON_STYLE

class PopupManager:
    def __init__(self, root):
        self.root = root
        self.mala_postura_inicio = None
        self.alerta_mostrada = False
        self.ultimo_popup_postura = 0
        self.image_folder = './images'
        self.image_files = [os.path.join(self.image_folder, f) for f in os.listdir(self.image_folder) if f.endswith('.jpeg')]
        self.image_index = 0
        self.schedule_popup()
        
    def show_postura_popup(self):
        current_time = time.time()
        if current_time - self.ultimo_popup_postura < 30:  # No mostrar si se mostró hace menos de 30 segundos
            return

        popup = Toplevel(self.root)
        popup.title("Instrucciones de Postura")
        popup.geometry("600x600")
        popup.configure(bg=BEIGE_COLOR)
        
        img_path = "postura.png"
        img = Image.open(img_path)
        img = img.resize((550, 470))
        photo = ImageTk.PhotoImage(img)
        
        img_label = Label(popup, image=photo, bg=BEIGE_COLOR)
        img_label.image = photo
        img_label.pack(pady=10)
        
        close_button = Button(popup, text="Cerrar", command=popup.destroy, **BUTTON_STYLE)
        close_button.pack(pady=10)
        
        self.ultimo_popup_postura = current_time
        
    def show_pause_popup(self):
        if self.image_index >= len(self.image_files):
            self.image_index = 0
        
        popup = Toplevel(self.root)
        popup.title("Pausa Activa")
        popup.geometry("600x600")
        popup.configure(bg=BEIGE_COLOR)
        
        pause_text_label = Label(popup,
                                 text="¡Es momento de realizar la pausa activa!",
                                 font=("Helvetica", 14),
                                 fg="#4A90E2",
                                 bg=BEIGE_COLOR)
        pause_text_label.pack(pady=10)
        
        img = Image.open(self.image_files[self.image_index])
        img = img.resize((550, 430))
        photo = ImageTk.PhotoImage(img)
        
        img_label = Label(popup, image=photo, bg=BEIGE_COLOR)
        img_label.image = photo
        img_label.pack(pady=10)
        
        close_button = Button(popup, text="Pausa Activa Realizada", command=popup.destroy, **BUTTON_STYLE)
        close_button.pack(pady=10)
        
        self.image_index += 1
        
    def schedule_popup(self):
        self.show_pause_popup()
        self.root.after(60000, self.schedule_popup)
        
    def check_posture(self, posture):
        current_time = time.time()
        if posture =="Por favor acomódese de perfil":
            messagebox.showwarning("Alerta de Postura", 
                                       "Posicionate de perfil para poder empezar con la medición")

        if posture == "Mala":
            if self.mala_postura_inicio is None:
                self.mala_postura_inicio = current_time
            elif not self.alerta_mostrada and (current_time - self.mala_postura_inicio) > 20:
                messagebox.showwarning("Alerta de Postura", 
                                       "Has mantenido una mala postura durante más de 20 segundos. Por favor corrígela.")
                self.alerta_mostrada = True
        elif posture == "No detectada":
            self.show_postura_popup()
        else:
            self.mala_postura_inicio = None
            self.alerta_mostrada = False