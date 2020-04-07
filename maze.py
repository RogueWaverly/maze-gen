from PIL import Image
from colors import colors
import backgrounds
import shapes

class Maze():

  def __init__(self, width, height):
    self.image = Image.new('RGB', (width, height), colors['white'])

  def set_shape(self, shape, *args):
    self.shape = getattr(shapes, shape)(*args)

  def set_background(self, background):
    self.background = background

  def _draw_background(self):
    backgrounds.draw_background(self.background, self.image)

  def _draw_nodes(self):
    self.shape.draw_nodes(self.image)

  def _reset_node_parents(self):
    # TODO
    pass

  def _is_maze_edge(self, edge):
    # TODO
    return True

  def _randomize_maze_edges(self):
    # TODO
    self._reset_node_parents()
    self.maze_edges = []
    for edge in self.shape.edges:
      if self._is_maze_edge(edge):
        self.maze_edges.append(edge)

  def _draw_maze_edges(self):
    self.shape.draw_edges(self.image, self.maze_edges)

  def draw_random_maze(self):
    self._draw_background()
    self._draw_nodes()
    self._randomize_maze_edges()
    self._draw_maze_edges()

  def draw_maze(self):
    self._draw_background()
    self._draw_nodes()
    self._draw_maze_edges()

  def save_maze_as_png(self, file_name):
    self.image.save(file_name + ".png", "PNG")
