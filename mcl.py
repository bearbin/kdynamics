#!/usr/bin/env python3

import sys
from common import *
from robomap import *
from math import cos, sin, radians, acos, sqrt, hypot

STD_DEV = 2.5
PRE_NORM_FACTOR = 0.5
ROBUSTNESS_K = 0.04
MAX_SENSIBLE_SONAR_ANGLE = radians(45)

# gets distance to wall
def get_dist_to_wall(x, y, theta, wall):  
  (ax, ay, bx, by) = wall

  numerator = ((by - ay) * (ax - x) - (bx - ax) * (ay - y)) 
  denominator = ((by - ay) * cos(theta) - (bx - ax) * sin(theta))
  dist = numerator / denominator if not denominator == 0 else -1

  #print("The wall is ", wall, " with distance ", dist)
  return dist

def intersects_wall(x, y, wall): 
  u = 0.02
  (ax, ay, bx, by) = wall
  left_x = min(ax, bx) - u
  right_x = max(ax, bx) + u
  top_y = max(ay, by) + u
  bottom_y = min(ay, by) - u

  return left_x <= x and x <= right_x and bottom_y <= y and y <= top_y

def find_closest_wall(x, y, theta):
  mymap = Map.draw_robot_wars_map()
  
  # Get list of (wall, distance) pairs
  wms = [(wall, get_dist_to_wall(x, y, theta, wall)) for wall in mymap.walls]

  # Filter out walls behind or to the side of us
  filtered_wms = filter(lambda wm: wm[1] >= 0 and intersects_wall(x + wm[1] * cos(theta), y + wm[1] * sin(theta), wm[0]), wms) 

  l = list(filtered_wms)
  if len(l) <= 0:
    return ((), 10000000)
  closest_wall_and_distance = min(l, key = lambda wm: wm[1])


  # Return wall with min distance m
  return closest_wall_and_distance

def calculate_pz(m, z):
  gaussian = math.exp((-(z-m)**2) / (2 * (STD_DEV ** 2)))
  return gaussian + ROBUSTNESS_K 

def is_incidence_angle_acceptable(wall, theta):
  (ax, ay, bx, by) = wall
  dy = ay - by
  dx = bx - ax
  numerator = cos(theta) * dy + sin(theta) * dx
  denominator = hypot(dy, dx)                          # sqrt((ay - by)**2 + (bx - ax)**2)
  return acos(numerator / denominator) <= MAX_SENSIBLE_SONAR_ANGLE

def calculate_likelihood(x, y, degrees, z):
  (_, m) = find_closest_wall(x, y, radians(degrees))
  pz = calculate_pz(m, z) 
  return pz
 
