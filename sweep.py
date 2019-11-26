#!/usr/bin/env python3

import time
from common import *
from waypoint import *
from math import radians

# Metres
scan_waypoint_a = (0.90, 0.30)
scan_waypoint_b = (0.90, 0.70)
scan_waypoint_c = (0.42, 0.30)

# Sigs are: (start angle, end_angle, dists at 5 degree intervals)

bottleless_a = (45, -45, [])

bottleless_b = (100, 0, [])

# TODO: write specific waypoint
c_signature = (180, 0, [51, 51, 51, 51, 51, 51, 52, 53, 53, 53, 53, 53, 54, 55, 97, 96, 95, 94, 93, 93, 93, 92, 92, 92, 92, 92, 92, 93, 93, 93, 94, 100, 100, 99, 100, 101, 102, 103, 166, 164, 164, 163, 163, 162, 162])

def measure_sonar():
    readings = get_sonar_cm()
    print("got " + str(readings))
    time.sleep(0.02)
    return readings

BP.set_motor_limits(PORT_A, 25)

# Returns tuple (avg absolute radians angle to bottle, avg distance to bottle)
def find_bottle(sonar_angle, signature):
  (start_angle, end_angle, bottleless_dists) = signature

  turn_sonar_left(start_angle - sonar_angle)
  sonar_angle = start_angle

  readings = []

  reading = measure_sonar()
  readings.append(reading)

  while sonar_angle > end_angle:
     turn_sonar_left(-5)
     time.sleep(0.2)
     sonar_angle -= 5 * 7.5 / 9
     reading = measure_sonar()
     readings.append(reading)

  print("Bottleless is ", bottleless_dists)
  print()
  print("Readings are ", readings)

  waypoints = []
  threshold = 15
  minimum_measurement = 20

  for i in range(len(readings)):
    if readings[i] < minimum_measurement:
      continue
    difference = bottleless_dists[i] - readings[i]
    if difference >= threshold:
      waypoints.append((180 - i * 5 * 7.5 / 9, readings[i]))

  print("Waypoints index are ", waypoints)
  bottle_pos = sorted(waypoints)[round(len(waypoints)/2)]
  print("Bottle at : ", bottle_pos)
  bottle_pos[0] = radians(bottle_pos[0])

  return bottle_pos

# waypoint_id is 'a', 'b' or 'c'
def find_angle_rotation_robot_left(curr_sonar_angle, waypoint_id):
    assert(waypoint == 'a' or waypoint == 'b' or waypoint == 'c')

    signature = bottleless_a if waypoint_id == 'a' else (bottleless_b if waypoint_id == 'b' else bottleless_c)

    return find_bottle(curr_sonar_angle, signature)[0]

