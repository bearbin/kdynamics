#!/usr/bin/env python3

import time
import sys
import brickpi3


def get_motor_power(port):
   return BP.get_motor_status(port)[1]

BP = brickpi3.BrickPi3()
BP.set_motor_power(BP.PORT_B, 15)
BP.set_motor_power(BP.PORT_C, 15)

scaling_factor = 360/229
DISTANCE = 10
scaled_distance = DISTANCE * scaling_factor

for i in range(0, 4):
   encoder_b_position = 0
   encoder_c_position = 0

   while True:
      encoder_b_position += BP.get_motor_encoder(BP.PORT_B)
      encoder_c_position += BP.get_motor_encoder(BP.PORT_C)
      BP.reset_motor_encoder(BP.PORT_B)
      BP.reset_motor_encoder(BP.PORT_C)

      if encoder_b_position > scaled_distance:
          BP.set_motor_power(BP.PORT_B, 0)
      if encoder_c_position > scaled_distance:
          BP.set_motor_power(BP.PORT_C, 0)
      if (get_motor_power(BP.PORT_B) == 0 and get_motor_power(BP.PORT_C) == 0):
          BP.set_motor_power(BP.PORT_B, 15)
          BP.set_motor_power(BP.PORT_C, -15)
          break

      time.sleep(0.02)
