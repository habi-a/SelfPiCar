import time

# Car modules
import car_dir
import motor
import video_dir


# Calibrate the car and enable
busnum = 1
def init(speed):
    global offset_x,  offset_y, offset, forward0, forward1
    offset_x = 0
    offset_y = 0
    offset = 0
    forward0 = 'True'
    forward1 = 'False'
    try:
        for line in open('config'):
            if line[0:8] == 'offset_x':
                offset_x = int(line[11:-1])
                print 'offset_x =', offset_x
            if line[0:8] == 'offset_y':
                offset_y = int(line[11:-1])
                print 'offset_y =', offset_y
            if line[0:8] == 'offset =':
                offset = int(line[9:-1])
                print 'offset =', offset
            if line[0:8] == "forward0":
                forward0 = line[11:-1]
                print 'turning0 =', forward0
            if line[0:8] == "forward1":
                forward1 = line[11:-1]
                print 'turning1 =', forward1
    except:
        print 'no config file, set config to original'
    video_dir.setup(busnum=busnum)
    car_dir.setup(busnum=busnum)
    motor.setup(busnum=busnum)
    video_dir.calibrate(offset_x, offset_y)
    car_dir.calibrate(offset)
    motor.setSpeed(speed)


# Drive functions
def moveForward():
    motor.forward()

def turn(angle_in_degree):
    car_dir.turn(angle_in_degree)


# Stop car modules
def stop():
    motor.stop()
