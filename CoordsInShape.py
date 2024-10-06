import cv2
import numpy as np
import random
import time

# Dibujar silueta cargada
def draw_silhouette(frame):
    pts = np.loadtxt("shapeCoords/sil04.txt", dtype=int)
    pts = pts.reshape((-1, 1, 2))
    cv2.polylines(frame, [pts], isClosed=True, color=(0, 0, 255), thickness=5) #DIbuja en rojo
    mask = np.zeros(frame.shape[:2], dtype=np.uint8) #máscara en escala de grises
    cv2.fillPoly(mask, [pts], 255)
    return pts, mask

# Función para calcular el porcentaje de puntos dentro de la silueta
def calculate_points_inside_shape(pts_silhouette, points):
    inside_count = 0
    for point in points:
        # Utilizamos pointPolygonTest para comprobar si el punto está dentro (resultado > 0)
        result = cv2.pointPolygonTest(pts_silhouette, (point[0], point[1]), False)
        if result >= 0:
            inside_count += 1
    return inside_count

# Puntos aleatorios
def generate_random_points(num_points, width, height):
    return [(random.randint(0, width), random.randint(0, height)) for _ in range(num_points)]

# Captura de la cámara en tiempo real
cap = cv2.VideoCapture(0)

ret, frame = cap.read()
if ret:
    height, width = frame.shape[:2]

# Inicializar los puntos (simulando que se actualizan en tiempo real)
points = generate_random_points(10, width, height)  # 10 puntos al azar

# Variable para controlar el tiempo de actualización
last_update_time = time.time()

while True:
    # Leer el frame de la cámara
    ret, frame = cap.read()

    if not ret:
        print("Error al acceder a la cámara.")
        break

    # Dibujar la silueta en el frame
    pts_silhouette, silhouette_mask = draw_silhouette(frame)

    # Comprobar cuántos puntos están dentro de la silueta
    inside_count = calculate_points_inside_shape(pts_silhouette, points)
    
    # Calcular el porcentaje de puntos que están dentro
    total_points = len(points)
    if total_points > 0:
        match_percentage = (inside_count / total_points) * 100
        cv2.putText(frame, f"Coincidencia: {match_percentage:.2f}%", (10, 30), 
                    cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)

    # Dibujar los puntos en el frame (para visualización)
    for point in points:
        cv2.circle(frame, point, 5, (255, 255, 0), -1)  # Dibuja los puntos en color azul

    cv2.imshow("Hole in the Wall", frame)

    # Actualizar los puntos cada segundo
    current_time = time.time()
    if current_time - last_update_time >= 1:
        points = generate_random_points(10, width, height)  # 10 nuevos puntos aleatorios
        last_update_time = current_time

    # Presiona 'q' para salir
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Liberar la cámara y cerrar ventanas
cap.release()
cv2.destroyAllWindows()
