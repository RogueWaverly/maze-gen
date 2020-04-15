import math
from colors import colors

### CALCULATE BACKGROUND FUNCTIONS ###

def rgb_gradient(width, height, x, y):
  base_color = colors['white']
  center_x = width/2
  center_y = height/2
  x_radius = width/4
  y_radius = height/4
  start_angle = 30
  length = max(width, height)
  subradius = length/16
  diffuse = length

  def x_length(angle):
    return math.sin(math.radians(angle))*x_radius

  def y_length(angle):
    return math.cos(math.radians(angle))*y_radius

  return (
    base_color[0] - round(
        (x - (center_x + x_length(start_angle)))**2
        + (y - (center_y + y_length(start_angle)))**2
        - subradius**2
      ) // diffuse,
    base_color[1] - round(
        (x - (center_x + x_length(start_angle + 120)))**2
        + (y-(center_y + y_length(start_angle + 120)))**2
        - subradius**2
      ) // diffuse,
    base_color[2] - round(
        (x - (center_x + x_length(start_angle + 240)))**2
        + (y-(center_y + y_length(start_angle + 240)))**2
        - subradius**2
      ) // diffuse,
  )

def sunset(width, height, x, y):
  base_color = colors['red']
  length = min(width, height)
  return (
    base_color[0]-round((length/3*2-y)/4*3),
    base_color[1]-round((length/8*7-y)/4*3),
    base_color[2]-round(length/8+y/5),
  )

backgrounds = {
  'rgb_gradient': rgb_gradient,
  'sunset': sunset,
}


### DRAW BACKGROUND FUNCTIONS ###
def validate_background(background):
  if not background in backgrounds.keys():
    error_msg = '{} is not a valid background.'.format(background)
    raise ValueError(error_msg)

def draw_background(background, img, **kwargs):
  validate_background(background)
  width, height = img.size
  pixels = img.load()
  for x in range(width):
    for y in range(height):
      pixels[x, y] = backgrounds[background](width, height, x, y, **kwargs)

def draw_random_background(img):
  import random
  background = random.choice(list(backgrounds.keys()))
  draw_background(background, img)
