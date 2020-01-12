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

CAR_COUNT = 10

NEIGHBOR_COUNT = 7

# Distance to detect walls from
WALL_RADIUS = 20
SEPARATION_RADIUS = 20

"""
World (Model)
"""
WORLD_WIDTH = 200
WORLD_HEIGHT = 100

"""
Car (Model)
"""
CAR_LENGTH = 4.9

CAR_WIDTH = 1.8

CAR_WHEELBASE = 2.8

CAR_MAX_ACCELERATION = 5.0

CAR_MAX_VELOCITY = 20.0

CAR_MAX_STEERING_ANGLE = 37.0

CAR_MAX_STEERING_CHANGE = 30.0


"""
------------------
VIEW CONFIGURATION
------------------
"""

"""
Simulation (View)
"""
PIXEL_METER_RATIO = 7

"""
World (View)
"""
WORLD_COLOR = Color('white')

"""
World (View)
"""
WALL_COLOR = Color('black')


"""
Car (View)
"""
CAR_IMAGE_PATH = "car.png"

VECTOR_COLOR = Color('red')





