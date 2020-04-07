from maze import Maze

length = 512
maze = Maze(length, length)
maze.set_shape('Rectangle', 16, 16)
maze.set_background('rgb_gradient')
maze.draw_random_maze()
maze.save_maze_as_png("MAZE")
