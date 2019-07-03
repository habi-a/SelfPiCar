#!/usr/bin/env python

import car
import cv2
import finish
import requests
import time
import trajectory

# HTTP Request info (To submit chronos)
SERVER_URL = '35.193.192.104:80'
API_ENDPOINT = '/tournament/submitTime'
data = {"user_id": 1, "tournament_id": 1, "time": 0, "point": 0}

# Enable Car modules
car.init(40)

# Enable camera stream
camera = cv2.VideoCapture(-1)
camera.set(3, 160)
camera.set(4, 120)

# Start chrono
finish_seen = False
laps_remaining = 3
chronos = []
start = time.time()

# Start the car
car.moveForward()

# Main Loop
curr_steering_angle = 90
while (camera.isOpened() and laps_remaining > 0):
    ## Find the good trajectory
    _, frame = camera.read()

    ## If Finish is raised
    if finish.detect_finish(frame):
        finish_seen = True
    elif finish_seen:
        finish_seen = False
        laps_remaining -= 1
        chronos.append(time.time() - start)
        start = time.time()
    
    ## Crop the image
    crop_img = frame[60:120, 0:160]

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
        cx = int(M['m10']/M['m00'])
        cy = int(M['m01']/M['m00'])
        cv2.line(crop_img,(cx,0),(cx,720),(255,0,0),1)
        cv2.line(crop_img,(0,cy),(1280,cy),(255,0,0),1)
        cv2.drawContours(crop_img, contours, -1, (0,255,0), 1)

        if cx >= 120:
           car.turnLeft()
        if cx < 120 and cx > 50:
            car.turn(90)
        if cx <= 50:
            car.turnRight()
    else:
        print("I don't see the line")

    ## Display the resulting frame
    cv2.imshow('frame', crop_img)

    ## Stop program if 'q' key is pressed
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Stop process
car.stop()
cv2.destroyAllWindows()

# Send chronos to the server
for chrono in chronos:
    data.time = chrono
    print "[HTTP] Sending data..."
    resp = requests.post(SERVER_URL + API_ENDPOINT, data = data)
