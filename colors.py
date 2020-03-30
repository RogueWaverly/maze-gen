colors = {
  'black': (0, 0, 0),
  'taiwan-blue': (0, 0, 151),
  'periwinkle': (153, 153, 255),
  'lime': (153, 255, 153),
  'cyan': (153, 255, 255),
  'taiwan-red': (254, 0, 0),
  'red': (255, 153, 153),
  'magenta': (255, 153, 255),
  'canary': (255, 255, 153),
  'white': (255, 255, 255),
}

def random_color():
  import random
  return random.choice(list(colors.values()))
