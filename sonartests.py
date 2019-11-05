#!/usr/bin/env python3

import time
from common import *



def measure_sonar(expected_dist):
    reading = -1
    while reading < 0:
        reading = get_sonar_mm() 

    print("got" + str(get_sonar_cm()))
    time.sleep(0.02)

measure_sonar(100)
measure_sonar(100)
measure_sonar(100)
measure_sonar(100)
measure_sonar(100)
measure_sonar(100)
measure_sonar(100)
