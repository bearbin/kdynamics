#!/usr/bin/env python3
#
# https://www.dexterindustries.com/BrickPi/
# https://github.com/DexterInd/BrickPi3
#
# Copyright (c) 2016 Dexter Industries
# Released under the MIT license (http://choosealicense.com/licenses/mit/).
# For more information, see https://github.com/DexterInd/BrickPi3/blob/master/LICENSE.md
#
# This code is an example for running a motor a target speed (specified in Degrees Per Second) set by the encoder of another motor.
# 
# Hardware: Connect EV3 or NXT motors to the BrickPi3 motor ports A and D. Make sure that the BrickPi3 is running on a 9v power supply.
#
# Results:  When you run this program, motor A speed will be controlled by the position of motor D. Manually rotate motor D, and motor A's speed will change.

from __future__ import print_function # use python 3 syntax but make it compatible with python 2
from __future__ import division       #                           ''

import time     # import the time library for the sleep function
import brickpi3 # import the BrickPi3 drivers

BP = brickpi3.BrickPi3() # Create an instance of the BrickPi3 class. BP will be the BrickPi3 object.

try:
    try:
        BP.offset_motor_encoder(BP.PORT_B, BP.get_motor_encoder(BP.PORT_B)) # reset encoder B
        BP.offset_motor_encoder(BP.PORT_C, BP.get_motor_encoder(BP.PORT_C)) # reset encoder C
    except IOError as error:
        print(error)
    
    BP.set_motor_power(BP.PORT_C, BP.MOTOR_FLOAT)                          # float motor C
    #BP.set_motor_limits(BP.PORT_B, 50)                                     # optionally set a power limit
    while True:
        # The following BP.get_motor_encoder function returns the encoder value
        try:
            target = BP.get_motor_encoder(BP.PORT_C)     # read motor C's position
        except IOError as error:
            print(error)
        
        BP.set_motor_dps(BP.PORT_B, target)             # set the target speed for motor B in Degrees Per Second
        
        print(("Motor B Target Degrees Per Second: %d" % target), "  Motor B Status: ", BP.get_motor_status(BP.PORT_B))
        
        time.sleep(0.02)

except KeyboardInterrupt: # except the program gets interrupted by Ctrl+C on the keyboard.
    BP.reset_all()        # Unconfigure the sensors, disable the motors, and restore the LED to the control of the BrickPi3 firmware.
