from abc import ABC, abstractmethod
from PIL import Image, ImageDraw
from colors import colors


class PathNode:

  def __init__(self, coordinates):
    self.coordinates = coordinates
    self.parent = self
    self.rank = 0

  def find_parent(self):
    while self.parent != self.parent.parent:
      self.parent = self.parent.parent
    return self.parent


class WallNode:

  def __init__(self, coordinates):
    self.coordinates = coordinates


class Edge:

  def __init__(
      self, wall_node_1, wall_node_2, path_node_1=None, path_node_2=None):
    self.wall_node = [wall_node_1, wall_node_2]
    self.path_nodes = [path_node_1, path_node_2] \
      if path_node_1 is not None and path_node_2 is not None \
      else None

# TODO: convert drawn nodes into wall nodes and edges into Edges


class Shape(ABC):

  @abstractmethod
  def _init_nodes_and_edges(self):
    pass

  @abstractmethod
  def _calc_point(self, node):
    pass

  @abstractmethod
  def draw_nodes(self, img, width, height):
    pass

  @abstractmethod
  def draw_edges(self, img, edges):
    pass


class Rectangle(Shape):

  def __init__(self, x_units, y_units):
    self.x_units = x_units
    self.y_units = y_units
    self._init_nodes_and_edges()

  def _init_nodes_and_edges(self):
    self.path_nodes = set()
    self.wall_nodes = set()
    self.outer_edges = set()
    self.inner_edges = set()
    self.edges = set()

    last_wall_col = []
    last_wall_row = []
    
    # first cell
    if self.x_units >= 1 and self.y_units >= 1:
      # first path node
      start_path_node = PathNode((0,0))
      self.path_nodes.add(start_path_node)
      # first border corner
      start_nw_wall_node = WallNode((0,0))
      start_sw_wall_node = WallNode((0,1))
      start_ne_wall_node = WallNode((1,0))
      self.outer_edges.add(Edge(start_nw_wall_node, start_sw_wall_node))
      self.outer_edges.add(Edge(start_nw_wall_node, start_ne_wall_node))

    # first column
    prev_path_col = []
    prev_path_node = start_path_node
    prev_wall_col = []
    prev_wall_node = start_sw_wall_node
    for y in range(1, self.y_units):
      # path node
      new_path_node = PathNode((0,y))
      self.path_nodes.add(new_path_node)
      # left corner
      sw_wall_node = WallNode((0,y+1))
      ne_wall_node = WallNode((1,y))
      self.outer_edges.add(Edge(prev_wall_node, sw_wall_node))
      self.inner_edges.add(Edge(
          prev_wall_node, ne_wall_node, prev_path_node, new_path_node))
      self.edges.add(frozenset([new_path_node, prev_path_node]))
      # next
      prev_path_col.append(new_path_node)
      prev_path_node = new_path_node
      prev_wall_col.append(ne_wall_node)
      prev_wall_node = sw_wall_node
      # last
      if y == self.y_units-1:
        last_wall_row.append(sw_wall_node)

    # first row
    start_path_row = []
    prev_path_node = start_path_node
    start_wall_row = []
    prev_wall_node = start_ne_wall_node
    for x in range(1, self.x_units):
      # path node
      new_path_node = PathNode((x,0))
      self.path_nodes.add(new_path_node)
      # top corner
      sw_wall_node = WallNode((x,1)) if x>1 else prev_wall_col[0]
      ne_wall_node = WallNode((x-1,0))
      self.inner_edges.add(Edge(
          prev_wall_node, sw_wall_node, prev_path_node, new_path_node))
      self.outer_edges.add(Edge(prev_wall_node, ne_wall_node))
      self.edges.add(frozenset([new_path_node, prev_path_node]))
      # next
      start_path_row.append(new_path_node)
      prev_path_node = new_path_node
      start_wall_row.append(sw_wall_node)
      prev_wall_node = ne_wall_node
      # last
      if x == self.x_units-1:
        last_wall_col.append(ne_wall_node)

    # remaining grid
    prev_path_x = start_path_row[0] if len(start_path_row) > 0 else None
    prev_wall_nw = start_wall_row[0] if len(start_wall_row) > 0 else None
    for x in range(1, self.x_units):
      new_path_col = []
      prev_path_y = prev_path_col[0] if len(prev_path_col) > 0 else None
      new_wall_col = []
      # TODO:
      for y in range(1, self.y_units):
        # path node
        new_path_node = PathNode((x,y))
        self.path_nodes.add(new_path_node)
        # wall corner
        self.edges.add(frozenset([new_path_node, prev_path_x]))
        self.edges.add(frozenset([new_path_node, prev_path_y]))
        # next y
        new_path_col.append(new_path_node)
        if y < self.y_units-1:
          prev_path_y = prev_path_col[y]
        prev_path_x = new_path_node
        # last y
      # next x
      prev_path_col = new_path_col
      if x < self.x_units-1:
        prev_path_x = start_path_row[x] 
      # last x

    # last border column
    # last border row
    # last wall node

  def _calc_point(self, node, width, height):
    x, y = node.coordinates
    center_x = width//2
    center_y = height//2
    unit_length = min(width//self.x_units, height//self.y_units)
    start_x = center_x - ((self.x_units-1) * unit_length)//2
    start_y = center_y - ((self.y_units-1) * unit_length)//2
    return (start_x + x*unit_length, start_y + y*unit_length)

  def draw_nodes(self, img):
    width, height = img.size
    point_radius = 3
    draw = ImageDraw.Draw(img)
    for node in self.path_nodes:
      x, y = self._calc_point(node, width, height)
      draw.ellipse(
        (x-point_radius, y-point_radius, x+point_radius, y+point_radius),
        fill=colors['black']
      )

  def draw_edges(self, img, edges):
    width, height = img.size
    line_width = 3
    draw = ImageDraw.Draw(img)
    for edge in edges:
      points = []
      for node in edge:
        points.append(self._calc_point(node, width, height))
      draw.line(points, fill=colors['black'], width=line_width)
