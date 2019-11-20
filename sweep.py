#!/usr/bin/env python3

import time
from common import *

def measure_sonar():
    readings = get_sonar_cm()
    print("got " + str(readings))
    time.sleep(0.02)
    return readings

BP.set_motor_limits(PORT_A, 25)
i = 0

turn_sonar_left(180)
time.sleep(0.5)
curr_angle = 180

signature = []

reading = measure_sonar()
signature.append(reading)

while curr_angle > 0:
   turn_sonar_left(-3)
   time.sleep(0.2)
   curr_angle -= 3
   reading = measure_sonar()
   signature.append(reading)

print()
print(signature)

