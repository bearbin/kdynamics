#!/usr/bin/env python3

import time
import sys
from math import atan, cos, sin, degrees, radians, sqrt
from common import *

x = 0.0
y = 0.0
angle = 0.0


total_reset()

set_limit_at(25)

try:
  while True:
    print("Insert WX and WY")
    [target_x, target_y] = map(float, input().split())

    delta_y = target_y - y
    delta_x = target_x - x

    if delta_x == 0.0:
      target_angle = 90.0 if delta_y > 0.0 else -90.0
    else:
      target_angle = degrees(atan(delta_y / delta_x))

    delta_angle = target_angle - angle

    print("delta y = ", delta_y)
    print("delta x = ", delta_x)
    print("delta angle = ", delta_angle)
    print("target_angle = ", target_angle)
    print("angle = ", angle)

    turn_left(delta_angle)
    time.sleep(2)

    distance = sqrt((delta_x * 1000) ** 2 + (delta_y * 1000) ** 2)
    print("distance = ", distance)
    move(distance)
    time.sleep(1)

    angle += delta_angle
    x += delta_x
    y += delta_y

except KeyboardInterrupt:
  BP.reset_all()

