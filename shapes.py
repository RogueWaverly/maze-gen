from abc import ABC, abstractmethod
from PIL import Image, ImageDraw
from colors import colors


class Node(ABC):

  def __init__(self, coordinates):
    self.coordinates = coordinates


class PathNode(Node):

  def __init__(self, coordinates):
    super().__init__(coordinates)
    self.parent = self
    self.rank = 0

  def find_parent(self):
    while self.parent != self.parent.parent:
      self.parent = self.parent.parent
    return self.parent


class WallNode(Node):
  pass


class Edge(ABC):

  def __init__(self, wall_node_1, wall_node_2):
    self.wall_nodes = [wall_node_1, wall_node_2]


class InnerEdge(Edge):

  def __init__(self, wall_node_1, wall_node_2, path_node_1, path_node_2):
    super().__init__(wall_node_1, wall_node_2)
    self.path_nodes = [path_node_1, path_node_2]


class OuterEdge(Edge):
  pass


class Shape(ABC):

  def __init__(self, phrase=""):
    self.phrase = phrase

  @abstractmethod
  def _init_nodes_and_edges(self):
    pass

  @abstractmethod
  def _init_phrase(self):
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

  def __init__(self, x_units, y_units, phrase=""):
    super().__init__(phrase)
    self.x_units = x_units
    self.y_units = y_units
    self._init_nodes_and_edges()
    self._init_phrase()

  def _add_path_node(self, path_node):
    self.path_nodes[path_node.coordinates] = path_node

  def _add_wall_node(self, wall_node):
    self.wall_nodes[wall_node.coordinates] = wall_node

  def _add_wall_nodes(self, wall_nodes):
    for wall_node in wall_nodes:
      self._add_wall_node(wall_node)

  def _add_inner_edge(self, inner_edge):
    self.inner_edges[frozenset(inner_edge.path_nodes)] = inner_edge

  def _init_nodes_and_edges(self):
    self.path_nodes = {}
    self.wall_nodes = {}
    self.outer_edges = set()
    self.inner_edges = {}

    last_wall_col = []
    last_wall_row = []
    
    # first cell
    if self.x_units >= 1 and self.y_units >= 1:
      # first path node
      start_path_node = PathNode((0,0))
      self._add_path_node(start_path_node)
      # first border corner
      start_nw_wall_node = WallNode((0,0))
      start_sw_wall_node = WallNode((0,1))
      start_ne_wall_node = WallNode((1,0))
      self._add_wall_nodes((
          start_nw_wall_node, start_sw_wall_node, start_ne_wall_node))
      self.outer_edges.update([
          OuterEdge(start_nw_wall_node, start_sw_wall_node),
          OuterEdge(start_nw_wall_node, start_ne_wall_node)])

    # first column
    prev_path_col = []
    prev_path_node = start_path_node
    prev_wall_col = []
    prev_wall_node = start_sw_wall_node
    for y in range(1, self.y_units):
      # path node
      new_path_node = PathNode((0,y))
      self._add_path_node(new_path_node)
      # left corner
      sw_wall_node = WallNode((0,y+1))
      ne_wall_node = WallNode((1,y))
      self._add_wall_nodes((sw_wall_node, ne_wall_node))
      self.outer_edges.add(OuterEdge(prev_wall_node, sw_wall_node))
      self._add_inner_edge(InnerEdge(
          prev_wall_node, ne_wall_node, prev_path_node, new_path_node))
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
      self._add_path_node(new_path_node)
      # top corner
      sw_wall_node = WallNode((x,1)) if x>1 else prev_wall_col[0]
      ne_wall_node = WallNode((x+1,0))
      self._add_wall_nodes((sw_wall_node, ne_wall_node))
      self._add_inner_edge(InnerEdge(
          prev_wall_node, sw_wall_node, prev_path_node, new_path_node))
      self.outer_edges.add(OuterEdge(prev_wall_node, ne_wall_node))
      # next
      start_path_row.append(new_path_node)
      prev_path_node = new_path_node
      start_wall_row.append(sw_wall_node)
      prev_wall_node = ne_wall_node
      # last
      if x == self.x_units-1:
        last_wall_col.append(ne_wall_node)

    # remaining grid
    prev_path_x = start_path_row[0] if len(start_path_row)>0 else None
    for x in range(1, self.x_units):
      new_path_col = []
      prev_path_y = prev_path_col[0] if len(prev_path_col)>0 else None
      new_wall_col = []
      prev_wall_sw = start_wall_row[x-1]
      for y in range(1, self.y_units):
        # path node
        new_path_node = PathNode((x,y))
        self._add_path_node(new_path_node)
        # wall corner
        nw_wall_node = prev_wall_sw
        sw_wall_node = prev_wall_col[y] \
            if y<self.y_units-1 else WallNode((x,y+1))
        ne_wall_node = WallNode((x+1,y)) \
            if y>1 or x==self.x_units-1 else start_wall_row[x]
        self._add_wall_nodes((sw_wall_node, ne_wall_node))
        self._add_inner_edge(InnerEdge(
            nw_wall_node, sw_wall_node, prev_path_y, new_path_node))
        self._add_inner_edge(InnerEdge(
            nw_wall_node, ne_wall_node, prev_path_x, new_path_node))
        # next y
        new_path_col.append(new_path_node)
        if y < self.y_units-1:
          prev_path_y = prev_path_col[y]
        prev_path_x = new_path_node
        new_wall_col.append(ne_wall_node)
        prev_wall_sw = sw_wall_node
        # last y
        if y == self.y_units-1:
          last_wall_row.append(sw_wall_node)
      # next x
      prev_path_col = new_path_col
      if x < self.x_units-1:
        prev_path_x = start_path_row[x] 
      prev_wall_col = new_wall_col
      # last x
      if x == self.x_units-1:
        last_wall_col.extend(new_wall_col)

    # last wall node
    last_wall_node = WallNode((self.x_units, self.y_units))
    self._add_wall_node(last_wall_node)

    # last border column
    n_wall_node = last_wall_col[0] if len(last_wall_col)>0 else None
    for s_wall_node in last_wall_col[1:]:
      self.outer_edges.add(OuterEdge(n_wall_node, s_wall_node))
      n_wall_node = s_wall_node
    if n_wall_node:
      self.outer_edges.add(OuterEdge(n_wall_node, last_wall_node))

    # last border row
    w_wall_node = last_wall_row[0] if len(last_wall_row)>0 else None
    for e_wall_node in last_wall_row[1:]:
      self.outer_edges.add(OuterEdge(w_wall_node, e_wall_node))
      w_wall_node = e_wall_node
    if w_wall_node:
      self.outer_edges.add(OuterEdge(w_wall_node, last_wall_node))

  def _assign_phrase_edge(self, path_node_0, path_node_1):
    path_nodes = frozenset((path_node_0, path_node_1))
    self.phrase_edges.add(self.inner_edges[path_nodes])
    del self.inner_edges[path_nodes]

  def _add_forward_diag_phrase_edge(self, path_node_0):
    # TODO: get wall nodes from path node coordinates
    # TODO: force empty wall nodes to not have any walls
    # TODO: figure this out
    pass

  def _init_char(self, char, start_node):
    # use x_units, y_units
    # move edges from inner edges to phrase edges
    # if adding a diagonal edge, remove the surrounding edges
    if char == 'O':
      start_x = start_node.coordinates[0]
      start_y = start_node.coordinates[1]
      for y in range(start_y+1, start_y+5):
        self._assign_phrase_edge(
            self.path_nodes[start_x-1, y], self.path_nodes[start_x, y])
        self._assign_phrase_edge(
            self.path_nodes[start_x+3, y], self.path_nodes[start_x+4, y])
      for x in range(start_x+1, start_x+3):
        self._assign_phrase_edge(
            self.path_nodes[x, start_y-1], self.path_nodes[x, start_y])
        self._assign_phrase_edge(
            self.path_nodes[x, start_y+5], self.path_nodes[x, start_y+6])
    else:
      error_msg = "'{}' is not a valid charactor.".format(char)
      raise ValueError(error_msg)

  def _init_phrase(self):
    self.phrase_edges = set()
    phrase_length = len(self.phrase)
    CHAR_WIDTH = 4
    CHAR_HEIGHT = 6
    CHAR_SPACING = 1
    phrase_width = phrase_length*CHAR_WIDTH + (phrase_length-1)*CHAR_SPACING
    start_x_0 = int(self.x_units/2 - phrase_width/2)
    start_y = int(self.y_units/2 - CHAR_HEIGHT/2)
    # TODO: error check for length of phrase and grid size
    # TODO: allow for new lines, longer phrases

    for char_index, char in enumerate(self.phrase):
      start_x = start_x_0 + char_index*(CHAR_WIDTH+CHAR_SPACING)
      start_node = self.path_nodes[(start_x, start_y)]
      self._init_char(char, start_node)

  def _calc_point(self, node, width, height):
    x, y = node.coordinates
    center_x = width//2
    center_y = height//2
    unit_length = min(width//(self.x_units+1), height//(self.y_units+1))
    start_x = center_x - ((self.x_units) * unit_length)//2
    start_y = center_y - ((self.y_units) * unit_length)//2
    return (start_x + x*unit_length, start_y + y*unit_length)

  def draw_nodes(self, img):
    width, height = img.size
    half_length = 2
    draw = ImageDraw.Draw(img)
    for node in self.wall_nodes.values():
      x, y = self._calc_point(node, width, height)
      draw.rectangle(
        (x-half_length, y-half_length, x+half_length, y+half_length),
        fill=colors['black']
      )

  def draw_edges(self, img, edges):
    width, height = img.size
    line_width = 5
    draw = ImageDraw.Draw(img)
    for edge in edges:
      points = [self._calc_point(node, width, height) for node in edge.wall_nodes]
      draw.line(points, fill=colors['black'], width=line_width)

  def draw_phrase_edges(self, img, edges):
    # draw edges but thicker
    width, height = img.size
    line_width = 8
    draw = ImageDraw.Draw(img)
    for edge in edges:
      points = [self._calc_point(node, width, height) for node in edge.wall_nodes]
      draw.line(points, fill=colors['black'], width=line_width)
