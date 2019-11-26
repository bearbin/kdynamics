#!/usr/bin/env python3

import sys
from common import *
from robomap import *
from math import cos, sin, radians, acos, sqrt, hypot

HUXLEY_MAP = Map.draw_robot_wars_map()
STD_DEV = 2.5
ROBUSTNESS_K = 0.04
MAX_SENSIBLE_SONAR_ANGLE = radians(45)

# gets distance to wall
def get_dist_to_wall(x_cm, y_cm, theta_rad, wall):
  (ax, ay, bx, by) = wall

  numerator = ((by - ay) * (ax - x_cm) - (bx - ax) * (ay - y_cm))
  denominator = ((by - ay) * cos(theta_rad) - (bx - ax) * sin(theta_rad))
  dist = numerator / denominator if not denominator == 0 else -1

  #print("The wall is ", wall, " with distance ", dist)
  return dist

def intersects_wall(x_cm, y_cm, wall):
  u = 0.01  # Wall epsilon
  (ax, ay, bx, by) = wall
  left_x = min(ax, bx) - u
  right_x = max(ax, bx) + u
  top_y = max(ay, by) + u
  bottom_y = min(ay, by) - u

  return left_x <= x_cm and x_cm <= right_x and bottom_y <= y_cm and y_cm <= top_y

def find_closest_wall(x_cm, y_cm, theta_rad):
  # Get list of (wall, distance) pairs
  wms = [(wall, get_dist_to_wall(x_cm, y_cm, theta_rad, wall)) for wall in HUXLEY_MAP.walls]

  # Filter out walls behind or to the side of us
  filtered_wms = filter(lambda wm: wm[1] >= 0 and intersects_wall(x_cm + wm[1] * cos(theta_rad), y_cm + wm[1] * sin(theta_rad), wm[0]), wms)
  assert(filtered_wms)

  l = list(filtered_wms)
  if len(l) <= 0:
    return ((), 10000000)
  closest_wall_and_distance = min(l, key = lambda wm: wm[1])

  # Return wall with min distance m
  return closest_wall_and_distance

def calculate_pz(m, z):
  gaussian = math.exp((-(z-m)**2) / (2 * (STD_DEV ** 2)))
  return gaussian + ROBUSTNESS_K

def is_incidence_angle_acceptable(wall, theta_rad):
  (ax, ay, bx, by) = wall
  dy = ay - by
  dx = bx - ax
  numerator = cos(theta_rad) * dy + sin(theta_rad) * dx
  denominator = hypot(dy, dx)                          # sqrt((ay - by)**2 + (bx - ax)**2)
  return acos(numerator / denominator) <= MAX_SENSIBLE_SONAR_ANGLE

def calculate_likelihood(x_cm, y_cm, degrees, z):
  (_, m) = find_closest_wall(x_cm, y_cm, radians(degrees))
  pz = calculate_pz(m, z)
  return pz

