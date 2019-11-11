from rendering import drawLineXY

class Map:
  # walls = [(x0, y0, x1, y1), ...]
  def __init__(self, walls):
    self.walls = walls

  def draw(self):
    for wall in self.walls:
      drawLineXY(wall)

  @staticmethod
  def draw_robot_wars_map():
    return Map([(0, 0, 0, 168),      # O-A
                (0, 168, 84, 168),   # A-B
                (84, 168, 84, 126),  # B-C
                (84, 126, 84, 210),  # C-D
                (84, 210, 168, 210), # D-E
                (168, 210, 168, 84), # E-F
                (168, 84, 210, 84),  # F-G
                (210, 84, 210, 0),   # G-H
                (210, 0, 0, 0)])     # H-O
