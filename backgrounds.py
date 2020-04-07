import math

### CALCULATE BACKGROUND FUNCTIONS ###

def rgb_gradient(width, height, x, y):
  base_color = (255, 255, 255)
  center_x = width/2
  center_y = height/2
  length = max(width, height)
  radius = length/4
  start_angle = 30
  subradius = length/16
  diffuse = length

  def x_length(angle):
    return math.sin(math.radians(angle))*radius

  def y_length(angle):
    return math.cos(math.radians(angle))*radius

  return (
    base_color[0] - int(
        (x - (center_x + x_length(start_angle)))**2
        + (y - (center_y + y_length(start_angle)))**2
        - subradius**2
      ) // diffuse,
    base_color[1] - int(
        (x - (center_x + x_length(start_angle + 120)))**2
        + (y-(center_y + y_length(start_angle + 120)))**2
        - subradius**2
      ) // diffuse,
    base_color[2] - int(
        (x - (center_x + x_length(start_angle + 240)))**2
        + (y-(center_y + y_length(start_angle + 240)))**2
        - subradius**2
      ) // diffuse,
  )

backgrounds = {
  'rgb_gradient': rgb_gradient
}

### DRAW BACKGROUND FUNCTIONS ###
def validate_background(background):
  if not background in backgrounds.keys():
    error_msg = '{} is not a valid background.'.format(background)
    raise ValueError(error_msg)

def draw_background(background, img):
  validate_background(background)
  width, height = img.size
  pixels = img.load()
  for x in range(width):
    for y in range(height):
      pixels[x, y] = backgrounds[background](width, height, x, y)

def draw_random_background(img):
  import random
  background = random.choice(list(backgrounds.keys()))
  draw_background(background, img)
