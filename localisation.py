import math
import random
from collections import namedtuple

STD_DEV_E = 1
STD_DEV_F = 1
STD_DEV_G = 1
StatePoint = namedtuple('StatePoint', ('x', 'y', 'angle'))

def _next_point_from_distance(point, distance):
	noise_e = random.gauss(0, STD_DEV_E)
	noise_f = random.gauss(0, STD_DEV_F)

	return StatePoint(
		point.x + (distance + noise_e) * math.cos(point.angle),
		point.y + (distance + noise_e) * math.sin(point.angle),
		point.angle + noise_f
)

def _next_point_from_angle(point, angle):
	noise_g = random.gauss(0, STD_DEV_G)
	return StatePoint(point.x, point.y, point.angle + angle + noise_g)

class PointCloud:
	def __init__(self):
		self.state_points = [StatePoint(0, 0, 0)] * 100

	def move(self, distance):
		self.state_points = [
			_next_point_from_distance(point, distance)
			for point in self.state_points
		]

	def rotate(self, angle):
		self.state_points = [
			_next_point_from_angle(point, angle)
			for point in self.state_points
		]

	def __str__(self):
			return str(self.state_points)