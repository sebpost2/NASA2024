import cv2
import mediapipe as mp

# Función que inicia la detección de pose
def iniciar_deteccion():
    # Inicializar MediaPipe para la detección de poses
    mp_drawing = mp.solutions.drawing_utils
    mp_pose = mp.solutions.pose

    # Iniciar la captura de video desde la cámara web
    cap = cv2.VideoCapture(0)

    # Configuración del modelo de pose
    with mp_pose.Pose(static_image_mode=False, 
                      model_complexity=2, 
                      enable_segmentation=False,
                      min_detection_confidence=0.5,
                      min_tracking_confidence=0.5) as pose:

        while cap.isOpened():
            ret, frame = cap.read()
            if not ret:
                break

            # Convertir la imagen de BGR a RGB
            image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            image.flags.writeable = False  # Marca la imagen como no editable

            # Realizar la detección de la pose
            results = pose.process(image)

            # Marcar la imagen como editable nuevamente
            image.flags.writeable = True
            image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)

            # Dibujar las anotaciones de la pose en la imagen
            if results.pose_landmarks:
                for landmark in results.pose_landmarks.landmark:
                    h, w, _ = image.shape
                    cx, cy = int(landmark.x * w), int(landmark.y * h)
                    cv2.circle(image, (cx, cy), 5, (0, 255, 0), -1)

                mp_drawing.draw_landmarks(image, results.pose_landmarks, mp_pose.POSE_CONNECTIONS)

            # Mostrar el video en tiempo real
            cv2.imshow('Pose Estimation', image)

            if cv2.waitKey(5) & 0xFF == 27:  # Presiona 'Esc' para salir
                break

    # Liberar la captura y cerrar ventanas
    cap.release()
    cv2.destroyAllWindows()

# Ejecutar directamente la función de detección
if __name__ == "__main__":
    iniciar_deteccion()
