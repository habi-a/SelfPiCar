#!/usr/bin/env python

import car
import cv2
import finish
import numpy as np
import requests
import time
import trajectory

# HTTP Request info (To submit chronos)
SERVER_URL = '35.193.192.104:80'
API_ENDPOINT = '/tournament/submitTime'
data = {"user_id": 1, "tournament_id": 1, "time": 0, "point": 0}

# Enable Car modules
car.init(20)

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

    direction = trajectory.direction_to_take(frame)

    if direction == 0:
        car.turn(90)
    elif direction == 1:
        car.turnLeft()
    elif direction == 2:
        car.turnRight()

    ## Stop program if 'q' key is pressed
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Stop process
car.stop()
cv2.destroyAllWindows()

# Send chronos to the server
for chrono in chronos:
    data["time"] = chrono
    print "[HTTP] Sending data..."
    resp = requests.post(SERVER_URL + API_ENDPOINT, data = data)
