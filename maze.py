from PIL import Image
import random
from colors import colors
import backgrounds
import shapes

class Maze():

  def __init__(self, width, height):
    self.image = Image.new('RGB', (width, height), colors['white'])
    self.shape = None
    self.background = None
    self.outer_edges = None
    self.inner_edges = None
    self.border_walls = None
    self.maze_walls = None

  def set_shape(self, shape, *args):
    try:
      self.shape = getattr(shapes, shape)(*args)
    except AttributeError:
      error_msg = '{} is not a valid Shape.'.format(shape)
      raise ValueError(error_msg)
    self.inner_edges = list(self.shape.inner_edges)
    self.outer_edges = list(self.shape.outer_edges)

  def set_background(self, background):
    backgrounds.validate_background(background)
    self.background = background

  def _draw_background(self):
    if self.background is not None:
      backgrounds.draw_background(self.background, self.image)
    else:
      self.background = backgrounds.draw_random_background(self.image)

  def _draw_nodes(self):
    self.shape.draw_nodes(self.image)

  def randomize_border_walls(self):
    random.shuffle(self.outer_edges)
    self.border_walls = self.outer_edges[2:]

  def randomize_maze_walls(self):
    if self.shape is None:
      error_msg = 'Shape has not been set. Call set_shape() to set shape.'
      raise AttributeError(error_msg)

    def _is_maze_wall(edge):
      node1, node2 = edge.path_nodes
      node1_parent = node1.find_parent()
      node2_parent = node2.find_parent()
      if node1_parent == node2_parent:
        return True
      else:
        # join sets
        if node1.rank < node2.rank:
          node1_parent.parent = node2_parent
        elif node1.rank > node2.rank:
          node2_parent.parent = node1_parent
        else:
          node1_parent.parent = node2_parent
          node2_parent.rank += 1
        return False

    # reset maze
    for node in self.shape.path_nodes:
      node.parent = node
    random.shuffle(self.inner_edges)
    self.maze_walls = []

    for edge in self.inner_edges:
      if _is_maze_wall(edge):
        self.maze_walls.append(edge)

  def _draw_maze_walls(self):
    if self.maze_walls is None:
      error_msg = 'Maze walls have not been set. Call randomize_maze_walls() to set maze walls.'
      raise AttributeError(error_msg)
    if self.border_walls is None:
      error_msg = 'Border walls have not been set. Call randomize_border_walls() to set border walls.'
      raise AttributeError(error_msg)
    self.shape.draw_edges(self.image, self.border_walls + self.maze_walls)

  def draw_maze(self):
    self._draw_background()
    self._draw_nodes()
    self._draw_maze_walls()

  def draw_random_maze(self):
    self.randomize_border_walls()
    self.randomize_maze_walls()
    self.draw_maze()

  def draw_graph(self):
    self._draw_background()
    self._draw_nodes()
    self.shape.draw_edges(self.image, self.inner_edges)

  def save_maze_as_png(self, file_name):
    self.image.save(file_name + ".png", "PNG")
