#!/usr/bin/env python3

import time
from common import *

def measure_sonar(expected_dist):
    print("got " + str(get_sonar_cm()))
    time.sleep(0.1)

while True:
  measure_sonar(100)

measure_sonar(100)
measure_sonar(100)
measure_sonar(100)
measure_sonar(100)
measure_sonar(100)
measure_sonar(100)
