from pygame import Color

"""
-------------------
MODEL CONFIGURATION
-------------------
"""

"""
Simulation (Model)
"""
STEPS_PER_SECOND = 30

CAR_COUNT = 8

NEIGHBOR_COUNT = 7

"""
World (Model)
"""
WORLD_WIDTH = 100
WORLD_HEIGHT = 50

"""
Car (Model)
"""
CAR_LENGTH = 4.9

CAR_WIDTH = 1.8

CAR_WHEELBASE = 2.8

CAR_MAX_ACCELERATION = 5.0

CAR_MAX_VELOCITY = 20.0

CAR_MAX_STEERING_ANGLE = 5.0

CAR_MAX_STEERING_CHANGE = 30.0


"""
------------------
VIEW CONFIGURATION
------------------
"""

"""
Simulation (View)
"""
PIXEL_METER_RATIO = 15

"""
World (View)
"""
WORLD_COLOR = Color('white')


"""
Car (View)
"""
CAR_IMAGE_PATH = "car.png"









