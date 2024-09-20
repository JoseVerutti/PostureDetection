import tkinter as tk
from PIL import Image, ImageTk
import cv2
import mediapipe as mp
import numpy as np
import tensorflow as tf
from sklearn.preprocessing import StandardScaler

# Configuración de MediaPipe
mp_drawing = mp.solutions.drawing_utils
mp_pose = mp.solutions.pose

# Inicializar la captura de video
cap = cv2.VideoCapture(0)

# Inicializar el modelo de pose
pose = mp_pose.Pose(min_detection_confidence=0.5, min_tracking_confidence=0.5)

# Cargar el modelo pre-entrenado
model = tf.keras.models.load_model('Modelo.h5')

# Crear el escalador
scaler = StandardScaler()
# Ajustar el escalador con datos de ejemplo (esto deberías hacerlo con tus datos de entrenamiento)
example_data = np.random.rand(1000, 7)  # 1000 ejemplos con 7 características
scaler.fit(example_data)

# Crear la ventana principal de Tkinter
root = tk.Tk()
root.title("EI4work - Detector de Postura")
root.configure(bg="#2A475E")
root.geometry("800x750")

# Crear un frame para contener la imagen y el botón
main_frame = tk.Frame(root, bg="#2A475E")
main_frame.pack(fill=tk.BOTH, expand=True)

# Crear un widget Label para mostrar el video
label = tk.Label(main_frame)
label.pack(pady=10)

# Crear un widget Label para mostrar el resultado
result_label = tk.Label(main_frame, text="", font=("Helvetica", 16), bg="#2A475E", fg="white")
result_label.pack(pady=10)

# Variable para controlar si la detección está activa
detection_active = True

def update_frame():
    ret, frame = cap.read()
    if ret:
        frame = cv2.flip(frame, 1)
        frame = cv2.resize(frame, (640, 480))
        image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        image.flags.writeable = False
        
        if detection_active:
            results = pose.process(image)
            image.flags.writeable = True

            if results.pose_landmarks:
                mp_drawing.draw_landmarks(image, results.pose_landmarks, mp_pose.POSE_CONNECTIONS,
                                          mp_drawing.DrawingSpec(color=(200, 180, 150), thickness=2, circle_radius=2), 
                                          mp_drawing.DrawingSpec(color=(150,180,200), thickness=2, circle_radius=2))
                
                # Obtener los puntos de referencia necesarios
                landmarks = results.pose_landmarks.landmark
                nose = landmarks[mp_pose.PoseLandmark.NOSE]
                left_shoulder = landmarks[mp_pose.PoseLandmark.LEFT_SHOULDER]
                right_shoulder = landmarks[mp_pose.PoseLandmark.RIGHT_SHOULDER]
                left_hip = landmarks[mp_pose.PoseLandmark.LEFT_HIP]
                right_hip = landmarks[mp_pose.PoseLandmark.RIGHT_HIP]

                # Verificar si algún punto de referencia no fue detectado
                required_landmarks = [nose, left_shoulder, right_shoulder, left_hip, right_hip]
                if any(landmark.visibility < 0.5 for landmark in required_landmarks):
                    cv2.putText(image, "Advertencia: No se detectaron todos los puntos", 
                                (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 255), 2)
                    result_label.config(text="No se pueden detectar todos los puntos necesarios")
                else:
                    # Calcular las posiciones medias y diferencias
                    shoulder_avg_x = (left_shoulder.x + right_shoulder.x) / 2
                    shoulder_avg_y = (left_shoulder.y + right_shoulder.y) / 2
                    hip_avg_x = (left_hip.x + right_hip.x) / 2
                    hip_avg_y = (left_hip.y + right_hip.y) / 2
                    shoulder_hip_y_diff = shoulder_avg_y - hip_avg_y
                    nose_shoulder_y_diff = nose.y - shoulder_avg_y
                    nose_hip_y_diff = nose.y - hip_avg_y

                    # Preparar los datos para la predicción
                    input_data = np.array([[
                        shoulder_avg_x, shoulder_avg_y,
                        hip_avg_x, hip_avg_y,
                        shoulder_hip_y_diff,
                        nose_shoulder_y_diff,
                        nose_hip_y_diff
                    ]])

                    # Escalar los datos
                    input_data_scaled = scaler.transform(input_data)

                    # Realizar la predicción
                    prediction = model.predict(input_data_scaled)
                    posture = "Mala" if prediction[0][0] > 0.1 else "Buena"
                    result_label.config(text=f"Postura detectada: {posture}, Confianza: {prediction[0][0]:.2f}")

            else:
                cv2.putText(image, "No se detectó postura", 
                            (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 255), 2)
                result_label.config(text="No se detectó postura")

        # Convertir la imagen para Tkinter
        image = Image.fromarray(image)
        photo = ImageTk.PhotoImage(image=image)
        label.config(image=photo)
        label.image = photo
    
    # Programar la próxima actualización
    root.after(10, update_frame)

def toggle_detection():
    global detection_active
    detection_active = not detection_active
    button.config(text="Detener detección" if detection_active else "Iniciar detección")

# Crear botones
button = tk.Button(main_frame, text="Detener detección", command=toggle_detection, 
                   bg="#4A90E2", fg="white", font=("Helvetica", 12), 
                   relief="raised", bd=2)
button.pack(pady=10)

def on_closing():
    cap.release()
    root.destroy()

root.protocol("WM_DELETE_WINDOW", on_closing)

update_frame()
root.mainloop()