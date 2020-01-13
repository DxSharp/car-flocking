from typing import List

from pygame import Color

from wall import Wall
from world import World

"""
-------------------
MODEL CONFIGURATION
-------------------
"""

"""
Simulation (Model)
"""
STEPS_PER_SECOND = 30

CAR_COUNT = 1

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


def box_configuration(world: World):
    world.walls = [
        Wall(0.0, 0.0, world.width, 0.0),
        Wall(0.0, 0.0, 0.0, world.height),
        Wall(world.width, 0.0, world.width, world.height),
        Wall(0.0, world.height, world.width, world.height)
    ]



def road_configuration(world: World, length: float, width: float):
    x1 = world.width / 2 - length / 2
    x2 = world.width / 2 + length / 2

    y1 = world.height / 2 - width / 2
    y2 = world.height / 2 + width / 2

    world.walls = [
        Wall(0.0, 0.0, x1, 0.0),
        Wall(x1, 0.0, x1, y1),
        Wall(x1, y1, x2, y1),
        Wall(x2, y1, x2, 0.0),
        Wall(x2, 0.0, world.width, 0.0),
        Wall(world.width, 0.0, world.width, world.height),

        Wall(0.0, 0.0, 0.0, world.height),
        Wall(0.0, world.height, x1, world.height),
        Wall(x1, world.height, x1, y2),
        Wall(x1, y2, x2, y2),
        Wall(x2, y2, x2, world.height),
        Wall(x2, world.height, world.width, world.height)
    ]



