# -*- coding: utf-8 -*-

import cv2
import numpy as np

def detect_finish(frame):
    # Crop the image
    crop_img = frame

    # Convert to grayscale
    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

    # Gaussian blur
    blur = cv2.GaussianBlur(hsv,(5,5),0)

    lower_blue = np.array([60, 40, 40])
    upper_blue = np.array([150, 255, 255])
    mask = cv2.inRange(hsv, lower_blue, upper_blue)

    # Find the contours of the frame
    contours,hierarchy = cv2.findContours(mask.copy(), 1, cv2.CHAIN_APPROX_NONE)

    # Find the biggest contour (if detected)
    if len(contours) > 0:
        return True
    else:
        return False