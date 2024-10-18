import tkinter as tk
from tkinter import Label
from constants import BEIGE_COLOR

def create_main_window(root):
    root.title("EI4work - Detector de Postura")
    root.configure(bg=BEIGE_COLOR)
    root.geometry("400x350")

def create_main_frame(root):
    main_frame = tk.Frame(root, bg=BEIGE_COLOR)
    main_frame.pack(fill=tk.BOTH, expand=True)
    return main_frame

def create_video_label(parent):
    label = Label(parent, bg=BEIGE_COLOR)
    label.pack(pady=10)
    return label

def create_result_label(parent):
    result_label = Label(parent, text="", font=("Helvetica", 10), bg=BEIGE_COLOR, fg="black")
    result_label.pack(pady=5)
    return result_label