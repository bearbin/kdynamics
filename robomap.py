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
    return Map([(0, 0, 0, 168),      # a
                (0, 168, 84, 168),   # b
                (84, 126, 84, 210),  # c
                (84, 210, 168, 210), # d
                (168, 210, 168, 84), # e
                (168, 210, 210, 84), # f
                (210, 84, 210, 0),   # g
                (210, 0, 0, 0)])     # h
