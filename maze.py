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
    self.edge_list = None
    self.maze_edges = None
    self.node_parents = {}

  def set_shape(self, shape, *args):
    try:
      self.shape = getattr(shapes, shape)(*args)
    except AttributeError:
      error_msg = '{} is not a valid Shape.'.format(shape)
      raise ValueError(error_msg)
    self.edge_list = list(self.shape.edges)

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

  def randomize_maze_edges(self):
    if self.shape is None:
      error_msg = 'Shape has not been set. Call set_shape() to set shape.'
      raise AttributeError(error_msg)

    def _is_maze_edge(edge):
      nodes = [node for node in edge]
#      print('node[0].parent = {}\tnode[1].parent = {}'.format(nodes[0].find_parent(), nodes[1].find_parent()))
      if nodes[0].find_parent() == nodes[1].find_parent():
        return False
      else:
        # join sets
        # TODO: figure out why the we are returning false Trues here
        #       I suspect that sets are not being joined in place
        if nodes[0].rank < nodes[1].rank:
          nodes[0].parent = nodes[1]
        elif nodes[0].rank > nodes[1].rank:
          nodes[1].parent = nodes[0]
        else:
          nodes[0].parent = nodes[1]
          nodes[1].rank += 1
        return True

    # reset maze
    for node in self.shape.nodes:
      node.parent = node
    random.shuffle(self.edge_list)
    self.maze_edges = []

    for edge in self.edge_list:
      if _is_maze_edge(edge):
        self.maze_edges.append(edge)

  def _draw_maze_edges(self):
    if self.maze_edges is None:
      error_msg = 'Maze edges have not been set. Call randomize_maze_edges() to set maze edges.'
      raise AttributeError(error_msg)
    self.shape.draw_edges(self.image, self.maze_edges)

  def draw_maze(self):
    self._draw_background()
    self._draw_nodes()
    self._draw_maze_edges()

  def draw_random_maze(self):
    self.randomize_maze_edges()
    self.draw_maze()

  def save_maze_as_png(self, file_name):
    self.image.save(file_name + ".png", "PNG")
