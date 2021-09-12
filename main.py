import constant
from maze import Maze

maze = Maze(constant.IMG_WIDTH, constant.IMG_HEIGHT)
maze.set_shape('Rectangle', constant.RECT_MAZE_WIDTH, constant.RECT_MAZE_HEIGHT)
#maze.set_phrase("OO")
maze.set_background('rgb_gradient')
maze.draw_random_maze()
maze.save_maze_as_png("MAZE")
