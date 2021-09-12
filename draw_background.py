from PIL import Image
import backgrounds
from colors import colors

width = 1920*3//4
height = 1080*3//4
img = Image.new('RGB', (width, height), colors['white'])
backgrounds.draw_background('rgb_gradient', img)
img.save("background.png", "PNG")
