#!/usr/bin/env python3

import time
import sys
from math import atan, cos, sin, degrees, radians
from common import *

x = 0
y = 0
angle = 0

BP.reset_motor_encoder(PORT_B)
BP.reset_motor_encoder(PORT_C)

set_limit_at(35)

try:
  while True:
    [wx, wy] = map(float, input().split())

    deltay = wy - y
    deltax = wx - x

    if not deltax == 0:
      wangle = degrees(atan(deltay / deltax))
    else:
      wangle = 90 if deltay > 0 else -90 
    
    print("delta y = ", deltay)
    print("delta x = ", deltax)
    print("wangle = ", wangle)
    print("angle = ", angle)

    turn_left(wangle - angle)
    time.sleep(2)
    reset_encoders()

    distance = ((wx - x) * 1000) / cos(radians( wangle )) 
    print(distance)
    move( distance )
    time.sleep(2)
    reset_encoders()

    angle += wangle
    x += wx
    y += wy

except KeyboardInterrupt:
  BP.reset_all()
  
