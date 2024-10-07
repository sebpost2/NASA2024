import cv2
import numpy as np
import random

nameFile = "5"
img = cv2.imread(f"shapes/{nameFile}.png", cv2.IMREAD_GRAYSCALE)

ret, thresh = cv2.threshold(img, 127, 255, cv2.THRESH_BINARY_INV)

contours, hierarchy = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

img_contour = cv2.cvtColor(img, cv2.COLOR_GRAY2BGR) 

for i, contour in enumerate(contours):
    
    color = (random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))
    

    cv2.drawContours(img_contour, contours, i, color, 2)


    print("Color ", i, ": ",color)


cv2.imshow("Contornos", img_contour)
cv2.waitKey(0)
cv2.destroyAllWindows()

for i, contour in enumerate(contours):
    
    print(f"Contorno {i+1}: {contour.reshape(-1, 2)}")


chosenContour = 0


epsilon = 0.005 * cv2.arcLength(contours[chosenContour], True)
approx = cv2.approxPolyDP(contours[chosenContour], epsilon, True)

print(approx.reshape(-1, 2))

with open(f"shapeCoords/{nameFile}.txt",'w') as f:
    for point in approx.reshape(-1, 2):
        f.write(f"{point[0]} {point[1]}\n")

