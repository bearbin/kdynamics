#!/usr/bin/env python3

import brickpi3
BP = brickpi3.BrickPi3()
BP.set_motor_power(BP.PORT_B, -60)
BP.set_motor_power(BP.PORT_C, -60)
