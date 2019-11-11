#!/usr/bin/env python3

import time
import sys
from math import atan2, cos, sin, degrees, radians, sqrt, hypot
from common import *
from localisation import *
from mcl import *
from rendering import *

WAYPOINTS = [
[84,30],

# [100,30],

[180,30],
[180,54],
[138,54],
[138,168],
[114,168],
[114,84],
[84,84],
[84,30]
]

INITIAL_X = 84
INITIAL_Y = 30
INITIAL_ANGLE = 0

def sign(number):
    return -1 if number < 0 else 1

x_cm = INITIAL_X
y_cm = INITIAL_Y
angle = INITIAL_ANGLE
points = PointCloud(x_cm, y_cm, angle)


def get_sonar_reading():
  x = -1
  while x == 255 or x < 0:
    x = get_sonar_cm()
  return x

def normalise_rads(angle):
  return atan2(sin(angle), cos(angle))

def navigateToWaypoint(target_x_metres, target_y_metres):
    global x_cm, y_cm, angle


    target_x_cm = target_x_metres * 100
    target_y_cm = target_y_metres * 100   
    
    delta_y = target_y_cm - y_cm
    delta_x = target_x_cm - x_cm

    if delta_x == 0 and delta_y == 0:
      return

    target_angle = degrees(atan2(delta_y, delta_x))

    delta_angle = (target_angle - angle)
    if delta_angle < -180:
      delta_angle += 360
    elif delta_angle > 180:
      delta_angle -= 360

    print()
    print()
    print()
    print("I need to move in y by = ", delta_y)
    print("I need to move in x by = ", delta_x)
    print("I need to rotate by angle = ", delta_angle)
    print("Final absolute angle I need to get to = ", target_angle)
    print("My current absolute angle = ", angle)

    turn_left(delta_angle)
    points.rotate_degrees_left(delta_angle)

    #time.sleep(2)

    distance = hypot(delta_x, delta_y)
    print("Distance I need to travel = ", distance)
    move_cm(distance)
    points.move(distance)

    #time.sleep(1)

    angle = degrees(normalise_rads(points.get_mean().angle))
    x_cm = points.get_mean().x
    y_cm = points.get_mean().y

    print("After move, my estimated position is: ")
    print("x = ", x_cm)
    print("y = ", y_cm)
    print("angle = ", angle)

    print()
    print("Performing MCL resampling")

    BP.reset_all()

    sonar_reading = get_sonar_reading()
    for i in range(0,100):
        print("My sonar reading is ", get_sonar_reading())    

    points.fuse_sonar(sonar_reading)
    new_mean = points.get_mean()
    angle = degrees(normalise_rads(new_mean.angle))
    x_cm = new_mean.x
    y_cm = new_mean.y

    print("After performing MCL, my estimated position is: ")
    print("x = ", x_cm)
    print("y = ", y_cm)
    print("angle = ", angle)
    drawParticlesStateful(points)
    time.sleep(15)


drawCoordinateFrame(1)

total_reset()

set_limit_at(25)
i = 0
try:
  while i < 9:
    # print("Insert WX and WY")
    # [target_x, target_y] = map(float, input().split())
    print(points.get_mean())
    
    [target_x, target_y] = map(lambda x: x / 100, WAYPOINTS[i])
    i = (i + 1) # % len(WAYPOINTS) 
    navigateToWaypoint(target_x, target_y)

except KeyboardInterrupt:
  BP.reset_all()

