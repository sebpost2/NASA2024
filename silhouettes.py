import numpy as np
import cv2

def draw_silhouette(frame, shape_file, match_percentage, color=(0, 0, 255)):
    pts = np.loadtxt(shape_file, dtype=int)
    pts = pts.reshape((-1, 1, 2))
    cv2.polylines(frame, [pts], isClosed=True, color=color, thickness=5)
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
