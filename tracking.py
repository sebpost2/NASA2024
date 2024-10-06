import cv2
import mediapipe as mp
import random
import time
from silhouettes import draw_silhouette, calculate_points_inside_shape

def iniciar_deteccion():
    mp_drawing = mp.solutions.drawing_utils
    mp_pose = mp.solutions.pose
    cap = cv2.VideoCapture(0)

    shape_files = ["shapeCoords/sil01.txt", "shapeCoords/sil02.txt", "shapeCoords/sil03.txt"]
    shape_file = random.choice(shape_files)
    start_time = time.time()
    score = 0
    score_incremented = False

    with mp_pose.Pose(static_image_mode=False, model_complexity=2, enable_segmentation=False,
                      min_detection_confidence=0.5, min_tracking_confidence=0.5) as pose:

        while cap.isOpened():
            ret, frame = cap.read()
            if not ret:
                print("Error al acceder a la cámara.")
                break

            frame = cv2.flip(frame, 1)
            image_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            image_rgb.flags.writeable = False
            results = pose.process(image_rgb)
            image_rgb.flags.writeable = True
            image_bgr = cv2.cvtColor(image_rgb, cv2.COLOR_RGB2BGR)

            if results.pose_landmarks:
                mp_drawing.draw_landmarks(image_bgr, results.pose_landmarks, mp_pose.POSE_CONNECTIONS)

            points = []
            if results.pose_landmarks:
                for landmark in results.pose_landmarks.landmark:
                    h, w, _ = image_bgr.shape
                    cx, cy = int(landmark.x * w), int(landmark.y * h)
                    points.append((cx, cy))

            pts_silhouette, silhouette_mask = draw_silhouette(image_bgr, shape_file, match_percentage=0)
            inside_count = calculate_points_inside_shape(pts_silhouette, points)
            total_points = len(points)
            match_percentage = (inside_count / total_points) * 100 if total_points > 0 else 0

            pts_silhouette, silhouette_mask = draw_silhouette(image_bgr, shape_file, match_percentage)

            if match_percentage >= 50 and not score_incremented:
                cv2.putText(image_bgr, "SUCCESS", (frame.shape[1] // 2 - 100, frame.shape[0] // 2),
                            cv2.FONT_HERSHEY_SIMPLEX, 2, (0, 255, 255), 5)
                cv2.imshow("Hole in the Wall", image_bgr)
                cv2.waitKey(2000)

                score += 1
                score_incremented = True
                shape_file = random.choice(shape_files)

            if match_percentage < 50:
                score_incremented = False

            cv2.putText(image_bgr, f"Puntaje: {score}", (10, frame.shape[0] - 20),
                        cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2)

            cv2.putText(image_bgr, f"Coincidencia: {match_percentage:.2f}%", (10, 30), 
                        cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)

            elapsed_time = time.time() - start_time
            countdown = max(0, 10 - int(elapsed_time))

            timer_text = f"{countdown}s"
            text_size = cv2.getTextSize(timer_text, cv2.FONT_HERSHEY_SIMPLEX, 2.5, 5)[0]
            text_x = (frame.shape[1] - text_size[0]) // 2
            cv2.putText(image_bgr, timer_text, (text_x, 60),
                        cv2.FONT_HERSHEY_SIMPLEX, 2.5, (0, 0, 255), 5)

            if countdown == 0:
                shape_file = random.choice(shape_files)
                start_time = time.time()

            cv2.imshow("Hole in the Wall", image_bgr)

            if cv2.waitKey(1) & 0xFF == ord('q'):
                break

    cap.release()
    cv2.destroyAllWindows()
