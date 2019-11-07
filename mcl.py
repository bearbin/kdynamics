#!/usr/bin/env python3

import sys
from common import *
from robomap import *
from math import cos, sin

MM_DISTANCE = float(sys.argv[1])

reset_encoders()

set_limit_at(35)

# gets distance to wall
def calculate_m(float x, float y, (float ax, float ay, float bx, float by)):
  return ((by - ay) * (ax - x) - (bx - ax) * (ay - y)) /
         ((by - ay) * cos(theta) - (bx - ax) * sin(theta))

def intersects_wall(float x, float y, (float ax, float ay, float bx, float by))
  left_x = min(ax, bx)
  right_x = max(ax, bx)
  top_y = max(ay, by)
  bottom_y = min(ay, by)

  return left_x <= x and x <= right_x and
         bottom_y <= y and y <= top_y

def find_closest_wall(float x, float y, float theta):
  mymap = Map.draw_robot_wars_map()
  return min(filter(lambda: m -> m >= 0 and
                    intersects_wall(x + m * cos(theta), y + m * sin(theta), wall),
                    [calculate_m(x, y, wall) for wall in mymap.walls]))


def calculate_likelihood(float x, float y, float theta, float z):
  m = find_closest_wall(x, y, theta)
  print m

