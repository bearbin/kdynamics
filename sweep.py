#!/usr/bin/env python3

import time
from common import *
from waypoint import *

bottleless = [87, 87, 87, 87, 87, 87, 87, 88, 88, 88, 89, 165, 165, 164, 164, 146, 145, 144, 143, 143, 143, 142, 142, 142, 142, 143, 143, 144, 146, 201, 201, 202, 203, 259, 259, 259, 259, 175, 126, 125, 124, 124, 88, 89, 88]

#write specific waypoint
bottleless_c = [51, 51, 51, 51, 51, 51, 52, 53, 53, 53, 53, 53, 54, 55, 97, 96, 95, 94, 93, 93, 93, 92, 92, 92, 92, 92, 92, 93, 93, 93, 94, 100, 100, 99, 100, 101, 102, 103, 166, 164, 164, 163, 163, 162, 162]

bottleless_a = []

bottleless_b = []

def measure_sonar():
    readings = get_sonar_cm()
    print("got " + str(readings))
    time.sleep(0.02)
    return readings

BP.set_motor_limits(PORT_A, 25)

def find_waypoint_angle(bottleless):
  curr_angle = 180

  signature = []

  reading = measure_sonar()
  signature.append(reading)

  while curr_angle > 0:
     turn_sonar_left(-5)
     time.sleep(0.2)
     curr_angle -= 5 * 7.5 / 9
     reading = measure_sonar()
     signature.append(reading)



  print("Bottleless is ", bottleless)
  print()
  print("Signature is ", signature)

  waypoints = []
  threshold = 15
  minimum_measurement = 30

  for i in range(len(signature)):
    if signature[i] < minimum_measurement:
      continue
    difference = bottleless[i] - signature[i]
    if difference >= threshold:
      waypoints.append(180 - i * 5 * 7.5 / 9)

  print("Waypoints index are ", waypoints)
  print(sorted(waypoints)[round(len(waypoints)/2)])

start_waypoint_c_x = 42 
start_waypoint_c_y = 30

navigateToWaypoint(start_waypoint_c_x, start_waypoint_c_y)

find_waypoint_angle(bottleless_c) 
