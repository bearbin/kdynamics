#!/usr/bin/env python3

import time
import sys
from math import atan2, cos, sin, degrees, radians, sqrt, hypot
from common import *
from localisation import *

def sign(number):
    return -1 if number < 0 else 1

x_cm = 0.0
y_cm = 0.0
angle = 0.0
points = PointCloud(0, 0, 0)

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

total_reset()

set_limit_at(25)

try:
  while True:
    print("Insert WX and WY")
    [target_x, target_y] = map(float, input().split())
    navigateToWaypoint(target_x, target_y)

except KeyboardInterrupt:
  BP.reset_all()

