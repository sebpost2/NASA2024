import cv2
import numpy as np
import random
import time

def draw_silhouette(frame):
    pts = np.loadtxt("shapeCoords/sil04.txt", dtype=int)
    pts = pts.reshape((-1, 1, 2))
    cv2.polylines(frame, [pts], isClosed=True, color=(0, 0, 255), thickness=5) 
    mask = np.zeros(frame.shape[:2], dtype=np.uint8)
    cv2.fillPoly(mask, [pts], 255)
    return pts, mask

def calculate_points_inside_shape(pts_silhouette, points):
    inside_count = 0
    for point in points:
        result = cv2.pointPolygonTest(pts_silhouette, (point[0], point[1]), False)
        if result >= 0:
            inside_count += 1
    return inside_count

def generate_random_points(num_points, width, height):
    return [(random.randint(0, width), random.randint(0, height)) for _ in range(num_points)]

cap = cv2.VideoCapture(0)

ret, frame = cap.read()
if ret:
    height, width = frame.shape[:2]

points = generate_random_points(10, width, height)
last_update_time = time.time()

while True:
    ret, frame = cap.read()

    if not ret:
        print("Error al acceder a la cámara.")
        break

    pts_silhouette, silhouette_mask = draw_silhouette(frame)

    inside_count = calculate_points_inside_shape(pts_silhouette, points)
    
    total_points = len(points)
    if total_points > 0:
        match_percentage = (inside_count / total_points) * 100
        cv2.putText(frame, f"Coincidencia: {match_percentage:.2f}%", (10, 30), 
                    cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)

    for point in points:
        cv2.circle(frame, point, 5, (255, 255, 0), -1)  

    cv2.imshow("Hole in the Wall", frame)

    current_time = time.time()
    if current_time - last_update_time >= 1:
        points = generate_random_points(10, width, height) 
        last_update_time = current_time

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
