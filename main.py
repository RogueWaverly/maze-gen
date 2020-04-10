from maze import Maze

width = 512
height = 512
maze = Maze(width, height)
maze.set_shape('Rectangle', 16, 16)
maze.set_background('rgb_gradient')
maze.draw_random_maze()
maze.save_maze_as_png("MAZE")
