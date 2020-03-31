from PIL import Image, ImageDraw
from colors import colors
from backgrounds import draw_background, rgb_gradient
from shapes import Rectangle

length = 512
white = colors['white']
img = Image.new('RGB', (length, length), white)

draw_background(rgb_gradient, img)

rect = Rectangle(16, 16)
rect.draw_rect(img)

# TODO: make maze

draw = ImageDraw.Draw(img)
# TODO: save with unique name
img.save("MAZE.png", "PNG")
