#!/usr/bin/env python3

import sys
from common import *
from robomap import *
from math import cos, sin, radians

reset_encoders()

set_limit_at(35)

# gets distance to wall
def get_dist_to_wall(x, y, theta, wall):  
  (ax, ay, bx, by) = wall

  numerator = ((by - ay) * (ax - x) - (bx - ax) * (ay - y)) 
  denominator = ((by - ay) * cos(theta) - (bx - ax) * sin(theta))
  dist = numerator / denominator if not denominator == 0 else -1

  print("The wall is ", wall, " with distance ", dist)
  return dist

def intersects_wall(x, y, wall): 
  (ax, ay, bx, by) = wall
  left_x = min(ax, bx)
  right_x = max(ax, bx)
  top_y = max(ay, by)
  bottom_y = min(ay, by)

  return left_x <= x and x <= right_x and bottom_y <= y and y <= top_y

def find_closest_wall(x, y, theta):
  mymap = Map.draw_robot_wars_map()
  
  # Get list of (wall, distance) pairs
  wms = [(wall, get_dist_to_wall(x, y, theta, wall)) for wall in mymap.walls]

  # Filter out walls behind or to the side of us
  filtered_wms = filter(lambda wm: wm[1] >= 0 and intersects_wall(x + wm[1] * cos(theta), y + wm[1] * sin(theta), wm[0]), wms) 

  # Return wall with min distance m
  return min(filtered_wms, key = lambda wm: wm[0])

def calculate_likelihood(x, y, degrees, z):
  m = find_closest_wall(x, y, radians(degrees))
  print(m)

