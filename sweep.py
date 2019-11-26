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
bottleless_c = (45, -45, [43, 44, 138, 138, 137, 136, 136, 135, 134, 134, 134, 134, 133, 134, 134, 134, 134, 135, 135, 142, 143, 143, 144]   )

def measure_sonar():
    readings = get_sonar_cm()
    print("got " + str(readings))
    time.sleep(0.02)
    return readings

BP.set_motor_limits(PORT_A, 25)


def correct_sonar_turn(turn):
    return turn * 7.5 / 9


# Returns tuple (avg absolute radians angle to bottle, avg distance to bottle)
def find_bottle(signature):
  (start_angle, end_angle, bottleless_dists) = signature

  turn_sonar_left(start_angle)
  time.sleep(1)
  sonar_angle = start_angle

  readings = []

  reading = measure_sonar()
  readings.append(reading)

  while sonar_angle > end_angle:
     turn_sonar_left(-5)
     time.sleep(0.2)
     sonar_angle -= correct_sonar_turn(5)
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
      waypoints.append((180 - correct_sonar_turn(i * 5), readings[i]))

  print("Waypoints index are ", waypoints)
  bottle_pos = sorted(waypoints)[round(len(waypoints)/2)]
  print("Bottle at : ", bottle_pos)
  # bottle_pos[0] = radians(bottle_pos[0])
  # return bottle_pos

  turn_sonar_left(-end_angle)
  time.sleep(1)

  return radians(bottle_pos[0])

# waypoint_id is 'a', 'b' or 'c'
def find_angle_rotation_robot_left(waypoint_id):
    assert(waypoint_id == 'a' or waypoint_id == 'b' or waypoint_id == 'c')

    signature = bottleless_a if waypoint_id == 'a' else (bottleless_b if waypoint_id == 'b' else bottleless_c)

    return find_bottle(signature)

