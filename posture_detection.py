import cv2
import mediapipe as mp
import numpy as np
import tensorflow as tf
import joblib
from PIL import Image, ImageDraw

class PostureDetector:
    def __init__(self):
        self.mp_drawing = mp.solutions.drawing_utils
        self.mp_pose = mp.solutions.pose
        self.pose = self.mp_pose.Pose(min_detection_confidence=0.5, min_tracking_confidence=0.5)
        self.model = tf.keras.models.load_model('Modelo4.h5')
        self.scaler = joblib.load('scaler.joblib')
        self.shoulder_distance_threshold = 0.15  # Umbral para detectar si los hombros están demasiado alejados

    def calculate_angle(self, a, b, c):
        a = np.array(a)
        b = np.array(b)
        c = np.array(c)
        radians = np.arctan2(c[1] - b[1], c[0] - b[0]) - np.arctan2(a[1] - b[1], a[0] - b[0])
        angle = np.abs(radians * 180.0 / np.pi)
        if angle > 180.0:
            angle = 360 - angle
        return angle

    def process_frame(self, frame):
        if isinstance(frame, np.ndarray):
            image = Image.fromarray(frame)
        elif isinstance(frame, Image.Image):
            image = frame
        else:
            print("Error: frame is not a valid numpy array or PIL Image")
            return frame, "No detectada", 0.0

        np_image = np.array(image)
        results = self.pose.process(np_image)

        if results.pose_landmarks:
            draw = ImageDraw.Draw(image)
            for landmark in results.pose_landmarks.landmark:
                x, y = int(landmark.x * image.width), int(landmark.y * image.height)
                draw.ellipse([x - 2, y - 2, x + 2, y + 2], fill='red', outline='red')

            for connection in self.mp_pose.POSE_CONNECTIONS:
                start_idx = connection[0]
                end_idx = connection[1]
                start_point = results.pose_landmarks.landmark[start_idx]
                end_point = results.pose_landmarks.landmark[end_idx]
                start_x, start_y = int(start_point.x * image.width), int(start_point.y * image.height)
                end_x, end_y = int(end_point.x * image.width), int(end_point.y * image.height)
                draw.line([start_x, start_y, end_x, end_y], fill='blue', width=2)

            landmarks = results.pose_landmarks.landmark

            left_shoulder = landmarks[self.mp_pose.PoseLandmark.LEFT_SHOULDER.value]
            right_shoulder = landmarks[self.mp_pose.PoseLandmark.RIGHT_SHOULDER.value]

            # Calcular la distancia horizontal entre los hombros
            shoulder_distance = abs(left_shoulder.x - right_shoulder.x)

            # Si la distancia entre los hombros es mayor que el umbral, solicitar que se acomode de perfil
            if shoulder_distance > self.shoulder_distance_threshold:
                return image, "Por favor acomódese de perfil", 0.0

            # Obtener coordenadas y calcular ángulos
            nose = landmarks[self.mp_pose.PoseLandmark.NOSE.value]
            left_hip = landmarks[self.mp_pose.PoseLandmark.LEFT_HIP.value]
            right_hip = landmarks[self.mp_pose.PoseLandmark.RIGHT_HIP.value]
            left_knee = landmarks[self.mp_pose.PoseLandmark.LEFT_KNEE.value]
            right_knee = landmarks[self.mp_pose.PoseLandmark.RIGHT_KNEE.value]

            shoulder = np.mean([left_shoulder.x, right_shoulder.x]), np.mean([left_shoulder.y, right_shoulder.y])
            hip = np.mean([left_hip.x, right_hip.x]), np.mean([left_hip.y, right_hip.y])
            knee = np.mean([left_knee.x, right_knee.x]), np.mean([left_knee.y, right_knee.y])

            angulo_cabeza_hombros_cadera = self.calculate_angle([nose.x, nose.y], shoulder, hip)
            angulo_hombros_cadera_rodilla = self.calculate_angle(shoulder, hip, knee)

            input_data = np.array([[angulo_cabeza_hombros_cadera, angulo_hombros_cadera_rodilla]])
            input_data_scaled = self.scaler.transform(input_data)
            prediction = self.model.predict(input_data_scaled)
            posture = "Buena" if prediction[0][0] > 0.7 else "Mala"

            return image, posture, prediction[0][0]

        return image, "No detectada", 0.0
