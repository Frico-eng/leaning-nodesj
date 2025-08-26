import cv2
import numpy as np

# Define HSV ranges for cube colors
COLOR_RANGES = {
    "white":  ((0, 0, 200),   (180, 50, 255)),
    "yellow": ((20, 100, 100), (30, 255, 255)),
    "red1":   ((0, 100, 100),  (10, 255, 255)),
    "red2":   ((160, 100, 100), (180, 255, 255)),  # red wraps around
    "blue":   ((100, 150, 0),  (140, 255, 255)),
    "green":  ((40, 70, 70),   (80, 255, 255)),
    "orange": ((10, 100, 100), (20, 255, 255))
}

def detect_colors(face_img):
    """
    Detects colors of the 9 stickers on a single cube face.
    Returns a list of color names in row-major order.
    """
    stickers = []
    img = cv2.resize(face_img, (300, 300))  # standardize size
    hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)

    step = 100  # 300 / 3
    for row in range(3):
        for col in range(3):
            x1, y1 = col*step, row*step
            x2, y2 = (col+1)*step, (row+1)*step
            roi = hsv[y1:y2, x1:x2]
            avg_hsv = np.mean(roi.reshape(-1, 3), axis=0)
            color_name = classify_color(avg_hsv)
            stickers.append(color_name)
    return stickers

def classify_color(hsv_pixel):
    h, s, v = hsv_pixel
    for color, (lower, upper) in COLOR_RANGES.items():
        if color == "red1" or color == "red2":  # handle red separately
            if (lower[0] <= h <= upper[0]) and (lower[1] <= s <= upper[1]) and (lower[2] <= v <= upper[2]):
                return "red"
        else:
            if all(lower[i] <= hsv_pixel[i] <= upper[i] for i in range(3)):
                return color
    return "unknown"
