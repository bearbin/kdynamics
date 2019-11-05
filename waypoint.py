#!/usr/bin/env python3

import time
import sys
from math import atan2, cos, sin, degrees, radians, sqrt
from common import *
from localisation import *

def sign(number):
    return -1 if number < 0 else 1

x = 0.0
y = 0.0
angle = 0.0
points = PointCloud(0, 0, 0)

def navigateToWaypoint(target_x, target_y):
    global x, y, angle
    delta_y = target_y - y
    delta_x = target_x - x

    if delta_x == 0 and delta_y == 0:
      return

    target_angle = degrees(atan2(delta_y, delta_x))

    delta_angle = sign(delta_x) * (target_angle - angle)

    print("delta y = ", delta_y)
    print("delta x = ", delta_x)
    print("delta angle = ", delta_angle)
    print("target_angle = ", target_angle)
    print("angle = ", angle)

    turn_left(delta_angle)
    points.rotate_degrees_left(delta_angle)
    time.sleep(2)

    distance = sqrt((delta_x * 1000) ** 2 + (delta_y * 1000) ** 2)
    print("distance = ", distance)
    move(distance)
    points.move(distance / 10)
    time.sleep(1)

    angle = -points.get_mean().angle
    x = points.get_mean().x
    y = -points.get_mean().y

    print("Estimated position is: ")
    print("x = ", x)
    print("y = ", y)
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

