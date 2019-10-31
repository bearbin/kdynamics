import math
import random
from collections import namedtuple

STD_DEV_E = 0.05
STD_DEV_F = 0.01
STD_DEV_G = 0.01
POINT_CNT = 100

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

class StatePoint(namedtuple('StatePoint', ('x', 'y', 'angle'))):
	__slots__ = ()

	def __str__(self):
		return "(%f, %f, %f)" % (self.x, self.y, self.angle)

class PointCloud:
	def __init__(self, x=0, y=0, angle=0):
		self.state_points = [StatePoint(x, y, angle)] * POINT_CNT

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

	def __getitem__(self, item):
		return (self.state_points[item].x, self.state_points[item].y, self.state_points[item].angle, 1)

	def __str__(self):
		return "[%s]" % ", ".join([str(point) for point in self.state_points])
