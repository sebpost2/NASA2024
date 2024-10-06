import cv2
import mediapipe as mp
import torch

# Cargar el modelo YOLOv5
yolo_model = torch.hub.load('ultralytics/yolov5', 'yolov5s')
yolo_model.classes = [0]  # Solo detectar personas

mp_drawing = mp.solutions.drawing_utils
mp_pose = mp.solutions.pose

# Captura desde la cámara (0 para la cámara predeterminada)
cap = cv2.VideoCapture(0)

frame_count = 0  # Contador de fotogramas
# Bucle para procesar los fotogramas en tiempo real
with mp_pose.Pose(min_detection_confidence=0.3, min_tracking_confidence=0.3) as pose:
    while cap.isOpened():
        ret, frame = cap.read()
        if not ret:
            break

        frame_count += 1  # Incrementar contador de fotogramas
        if frame_count % 2 != 0:  # Procesar solo cada segundo fotograma
            continue

        # Convertir el marco de BGR a RGB
        image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        image.flags.writeable = False

        # Realizar detección de personas usando YOLOv5
        result = yolo_model(image)

        image.flags.writeable = True
        image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)

        MARGIN = 10

        # Procesar cada detección de personas
        for (xmin, ymin, xmax, ymax, confidence, clas) in result.xyxy[0].tolist():
            if confidence > 0.5:  # Procesar solo si la confianza es alta
                crop_image = image[int(ymin) + MARGIN:int(ymax) + MARGIN, int(xmin) + MARGIN:int(xmax) + MARGIN]
                crop_rgb = cv2.cvtColor(crop_image, cv2.COLOR_BGR2RGB)
                results = pose.process(crop_rgb)

                if results.pose_landmarks:
                    mp_drawing.draw_landmarks(crop_image, results.pose_landmarks, mp_pose.POSE_CONNECTIONS,
                                              mp_drawing.DrawingSpec(color=(245, 117, 66), thickness=2, circle_radius=2),
                                              mp_drawing.DrawingSpec(color=(245, 66, 230), thickness=2, circle_radius=2))

                # Volver a colocar la imagen recortada con landmarks en el marco original
                image[int(ymin) + MARGIN:int(ymax) + MARGIN, int(xmin) + MARGIN:int(xmax) + MARGIN] = crop_image

        # Mostrar la imagen con los resultados
        cv2.imshow('Detección de Personas y Pose en Tiempo Real', image)

        # Salir al presionar 'q'
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

# Liberar los recursos
cap.release()
cv2.destroyAllWindows()
