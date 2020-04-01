from PIL import Image, ImageDraw
from colors import colors
import backgrounds
import shapes

length = 512
white = colors['white']
img = Image.new('RGB', (length, length), white)

backgrounds.draw_background('rgb_gradient', img)

rect = shapes.Rectangle(16, 16)
rect.draw_nodes(img)

# TODO: make maze

draw = ImageDraw.Draw(img)
# TODO: save with unique name
img.save("MAZE.png", "PNG")
