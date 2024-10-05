import cv2
import numpy as np
import random

# Cargar la imagen que contiene la silueta (blanco sobre fondo negro)
img = cv2.imread('shapes/silueta01_test.png', cv2.IMREAD_GRAYSCALE)

# Umbralizar la imagen para obtener la silueta en blanco
ret, thresh = cv2.threshold(img, 127, 255, cv2.THRESH_BINARY_INV)

# Encontrar los contornos de la silueta
contours, hierarchy = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

# Dibujar los contornos sobre la imagen original (solo para visualización)
img_contour = cv2.cvtColor(img, cv2.COLOR_GRAY2BGR)  # Convertir a BGR para dibujar en color

# Dibujar cada contorno con un color diferente
for i, contour in enumerate(contours):
    # Generar un color aleatorio para cada contorno
    
    color = (random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))
    
    # Dibujar el contorno con su color correspondiente
    cv2.drawContours(img_contour, contours, i, color, 2)

    #Mostrar color
    print("Color ", i, ": ",color)


# Mostrar el contorno extraído
cv2.imshow("Contornos", img_contour)
cv2.waitKey(0)
cv2.destroyAllWindows()


# Si deseas imprimir las coordenadas de los contornos
for i, contour in enumerate(contours):
    
    print(f"Contorno {i+1}: {contour.reshape(-1, 2)}")


chosenContour = 0



# Reducir el número de puntos del contorno
epsilon = 0.005 * cv2.arcLength(contours[chosenContour], True)
approx = cv2.approxPolyDP(contours[chosenContour], epsilon, True)

# Imprimir los puntos reducidos
print(approx.reshape(-1, 2))

with open('shapeCoords/sil01.txt','w') as f:
    for point in approx.reshape(-1, 2):
        f.write(f"{point[0]} {point[1]}\n")

