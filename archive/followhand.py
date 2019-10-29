#!/usr/bin/env python3

import time
import sys
from common import *

TARGET_DISTANCE = 300
BASE_SPEED = 400

total_reset()
BP.set_sensor_type(SONAR_PORT, BP.SENSOR_TYPE.NXT_ULTRASONIC)
set_limit_at(100)

try:

  while True:
    reading = get_sonar_mm() 
    if reading < 0:
      continue

    dist_error_ratio = (TARGET_DISTANCE - reading) / TARGET_DISTANCE
    print((reading, dist_error_ratio))
    speed = dist_error_ratio * BASE_SPEED
    move_with_speed(speed)
    time.sleep(0.02)

except KeyboardInterrupt:
  BP.reset_all()
