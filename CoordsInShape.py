import cv2
import numpy as np

# Definir función para dibujar la silueta sobre el feed en tiempo real
def draw_silhouette(frame):
    # Cargar los puntos de la silueta desde un archivo txt
    pts = np.loadtxt("sil01.txt", dtype=int)
    pts = pts.reshape((-1, 1, 2))

    # Dibujar la silueta (en rojo) sobre el frame
    cv2.polylines(frame, [pts], isClosed=True, color=(0, 0, 255), thickness=5)
    
    # Crear una máscara en escala de grises para la silueta
    mask = np.zeros(frame.shape[:2], dtype=np.uint8)
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

# Captura de la cámara en tiempo real
cap = cv2.VideoCapture(0)

# Lista de puntos de ejemplo (en un futuro estos puntos serán actualizados en tiempo real)
# Los puntos pueden ser cualquier conjunto de coordenadas que quieras comprobar
points = [(150, 200), (220, 250), (300, 400), (120, 100)]

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

    # Mostrar el feed de la cámara con la silueta y la coincidencia
    cv2.imshow("Hole in the Wall", frame)

    # Presiona 'q' para salir
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Liberar la cámara y cerrar ventanas
cap.release()
cv2.destroyAllWindows()
