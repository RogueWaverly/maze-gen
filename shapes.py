from abc import ABC, abstractmethod
from PIL import Image, ImageDraw
from colors import colors


class Node:

  def __init__(self, coordinates=()):
    self.coordinates = coordinates


class Shape(ABC):

  @abstractmethod
  def init_nodes_and_edges(self):
    pass

  @abstractmethod
  def calc_point(self, node):
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
    self.init_nodes_and_edges()

  def init_nodes_and_edges(self):
    self.nodes = set()
    self.edges = set()
    
    # first node
    if self.x_units >= 1 and self.y_units >= 1:
      start_node = Node((0,0))
      self.nodes.add(start_node)

    # first row
    start_row = []
    prev_node = start_node
    for x in range(1, self.x_units):
      new_node = Node((x,0))
      self.nodes.add(new_node)
      self.edges.add(frozenset([new_node, prev_node]))
      start_row.append(new_node)
      prev_node = new_node

    # first column
    prev_col = []
    prev_node = start_node
    for y in range(1, self.y_units):
      new_node = Node((0,y))
      self.nodes.add(new_node)
      self.edges.add(frozenset([new_node, prev_node]))
      prev_col.append(new_node)
      prev_node = new_node

    # remaining grid
    prev_x = start_row[0] if len(start_row) > 0 else None
    for x in range(1, self.x_units):
      new_col = []
      prev_y = prev_col[0] if len(prev_col) > 0 else None
      for y in range(1, self.y_units):
        new_node = Node((x,y))
        self.nodes.add(new_node)
        self.edges.add(frozenset([new_node, prev_x]))
        self.edges.add(frozenset([new_node, prev_y]))
        new_col.append(new_node)
        if y < self.y_units-1:
          prev_y = prev_col[y]
        prev_x = new_node
      prev_col = new_col
      if x < self.x_units-1:
        prev_x = start_row[x] 

  def calc_point(self, node, width, height):
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
    for node in self.nodes:
      x, y = self.calc_point(node, width, height)
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
        points.append(self.calc_point(node, width, height))
      draw.line(points, fill=colors['black'], width=line_width)
