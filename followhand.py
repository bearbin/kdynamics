#!/usr/bin/env python3

import time
import sys
from common import *

TARGET_DISTANCE = 300
BASE_SPEED = 400

BP.reset_all()

BP.set_sensor_type(SONAR_PORT, BP.SENSOR_TYPE.NXT_ULTRASONIC)

BP.reset_motor_encoder(PORT_B)
BP.reset_motor_encoder(PORT_C)

set_limit_at(35)

try:

  while True:
    reading = get_sonar() * 10 # cm -> mm
    if reading < 0:
      continue

    dist_error_ratio = (TARGET_DISTANCE - reading) / TARGET_DISTANCE
    print((reading, dist_error_ratio))
    speed = dist_error_ratio * BASE_SPEED
    move_with_speed(speed)
    time.sleep(0.02)

except KeyboardInterrupt:
  BP.reset_all()
