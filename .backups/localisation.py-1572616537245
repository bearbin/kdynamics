import math
import random
from collections import namedtuple

STD_DEV_E = 0.05
STD_DEV_F = 0.01
STD_DEV_G = 0.01
MEAN_OF_E = 0.00
MEAN_OF_F = 0.00
MEAN_OF_G = 0.00
NUMBER_OF_PARTICLES = 100

def _next_point_from_distance(point, distance):
	noise_e = random.gauss(MEAN_OF_E, STD_DEV_E)
	noise_f = random.gauss(MEAN_OF_F, STD_DEV_F)

	return StatePoint(
		point.x + (distance + noise_e) * math.cos(point.angle),
		point.y + (distance + noise_e) * math.sin(point.angle),
		point.angle + noise_f,
		point.weight
	)

def _next_point_from_angle(point, angle):
	noise_g = random.gauss(MEAN_OF_G, STD_DEV_G)
	return StatePoint(point.x, point.y, point.angle + angle + noise_g, point.weight)

class StatePoint(namedtuple('StatePoint', ('x', 'y', 'angle', 'weight'))):
	__slots__ = ()

	def __add__(self, rhs):
		return StatePoint(self.x + rhs.x, self.y + rhs.y, self.angle + rhs.angle, self.weight + rhs.weight)

	def __mul__(self, rhs):
		return StatePoint(self.x * rhs, self.y * rhs, self.angle, self.weight)

	def __str__(self):
		return "(%f, %f, %f)" % (self.x, self.y, self.angle)

class PointCloud:
	def __init__(self, x=0, y=0, angle=0, weight=1/NUMBER_OF_PARTICLES):
		self.state_points = [StatePoint(x, y, angle, weight)] * NUMBER_OF_PARTICLES

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

	def get_mean(self):
		return sum([point * point.weight for point in self.state_points])

	def __getitem__(self, item):
		return (self.state_points[item].x, self.state_points[item].y, self.state_points[item].angle, 1)

	def __str__(self):
		return "[%s]" % ", ".join([str(point) for point in self.state_points])
