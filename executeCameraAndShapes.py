import cv2
import numpy as np

# Definir función para dibujar la silueta sobre el feed en tiempo real
def draw_silhouette(frame):
    # Definir los puntos de la silueta (aquí un triángulo como ejemplo)
    #pts = np.array([[100, 300], [250, 100], [400, 300]], np.int32)
    pts =  np.loadtxt("sil02.txt",dtype=int)
    pts = pts.reshape((-1, 1, 2))

    # Dibujar la silueta (en blanco) sobre el frame (en este caso es rojo)
    cv2.polylines(frame, [pts], isClosed=True, color=(0, 0, 255), thickness=5)
    
    # Crear una máscara en escala de grises para la silueta
    mask = np.zeros(frame.shape[:2], dtype=np.uint8)
    cv2.fillPoly(mask, [pts], 255)
    
    return mask

# Captura de la cámara en tiempo real
cap = cv2.VideoCapture(0)

while True:
    # Leer el frame de la cámara
    ret, frame = cap.read()

    if not ret:
        print("Error al acceder a la cámara.")
        break

    # Dibujar la silueta en el frame
    silhouette_mask = draw_silhouette(frame)
    
    #Dibujar la silueta del player
    

    # Convertir frame a escala de grises y umbralizar (para detectar cuerpos)
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    ret, player_mask = cv2.threshold(gray, 127, 255, cv2.THRESH_BINARY_INV)

    # Comprobar si el cuerpo cubre la silueta (operación bitwise AND)
    covered_area = cv2.bitwise_and(player_mask, silhouette_mask)

    # Calcular el porcentaje de coincidencia entre el cuerpo y la silueta
    silhouette_pixels = cv2.countNonZero(silhouette_mask)
    matching_pixels = cv2.countNonZero(covered_area)

    if silhouette_pixels > 0:
        match_percentage = (matching_pixels / silhouette_pixels) * 100
        cv2.putText(frame, f"Coincidencia: {match_percentage:.2f}%", (10, 30), 
                    cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)

    # Mostrar el feed de la cámara con la silueta y la coincidencia
    cv2.imshow("Hole in the Wall", frame)

    cv2.imshow("Hole in the Wall", player_mask)

    # Presiona 'q' para salir
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Liberar la cámara y cerrar ventanas
cap.release()
cv2.destroyAllWindows()
