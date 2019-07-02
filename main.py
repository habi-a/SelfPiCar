#!/usr/bin/env python

import car
import cv2
import requests
import time
import trajectory

# HTTP Request info
SERVER_URL = '127.0.0.1:5000'
API_ENDPOINT = '/tournament/submitTime'
data = {"user_id": 1, "tournament_id": 1, "time": 0, "point": 0}

# Enable Car modules
car.init(40)

# Enable camera stream
camera = cv2.VideoCapture(-1)
camera.set(3, 640)
camera.set(4, 480)

# Start chrono
start = time.time()

# Start the car
car.moveForward()

# Main Loop
curr_steering_angle = 90
while (camera.isOpened()):
    ## Find the good trajectory
    _, frame = camera.read()
    lane_lines = trajectory.detect_lane(frame)
    new_steering_angle = trajectory.compute_steering_angle(frame, lane_lines)
    curr_steering_angle = trajectory.stabilize_steering_angle(curr_steering_angle, new_steering_angle, len(lane_lines))
    heading_line_image = trajectory.display_heading_line(frame, curr_steering_angle, (0, 0, 255), line_width=5, )

    ## Follow the new trajectory
    car.turn(curr_steering_angle)
    cv2.imshow("lane lines", heading_line_image)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Stop chrono
end = time.time()
data.time = end - start

# Stop process
car.stop()
cv2.destroyAllWindows()

# Send chrono to the server
print "[HTTP] Sending data..."
resp = requests.post(SERVER_URL + API_ENDPOINT, data = data)
