from PIL import Image, ImageDraw
from colors import colors
from backgrounds import draw_background, rgb_gradient

length = 512
white = colors['white']
img = Image.new('RGB', (length, length), white)

draw_background(rgb_gradient, img)

# TODO: make maze

draw = ImageDraw.Draw(img)
# TODO: save with unique name
img.save("MAZE.png", "PNG")
