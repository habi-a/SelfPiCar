# -*- coding: utf-8 -*-

import cv2
import numpy as np

def direction_to_take(frame):
    ## Crop the image
    crop_img = frame [0:60, 0:160]

    ## Convert to grayscale
    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

    ## Gaussian blur
    blur = cv2.GaussianBlur(hsv, (5, 5), 0)

    lower_orange = np.array([5, 40, 40])
    upper_orange = np.array([15, 255, 255])
    mask = cv2.inRange(blur, lower_orange, upper_orange)

    ## Find the contours of the frame
    contours, hierarchy = cv2.findContours(mask.copy(), 1, cv2.CHAIN_APPROX_NONE)

    ## Find the biggest contour (if detected)
    if len(contours) > 0:
        c = max(contours, key=cv2.contourArea)
        M = cv2.moments(c)
        if (M['m00'] != 0):
            cx = int(M['m10']/M['m00'])
            cy = int(M['m01']/M['m00'])
            cv2.line(crop_img,(cx,0),(cx,720),(255,0,0),1)
            cv2.line(crop_img,(0,cy),(1280,cy),(255,0,0),1)
            cv2.drawContours(crop_img, contours, -1, (0,255,0), 1)
        else:
            return 3

        cv2.imshow('frame',crop_img)

        if cx >= 120:
            return 2
        if cx < 120 and cx > 50:
            return 0
        if cx <= 50:
            return 1
    else:
        return 3
