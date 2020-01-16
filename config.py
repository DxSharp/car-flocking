from random import randrange
from typing import Callable

from pygame import Color

from car import Car
from goal import Goal
from vector import Vector
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

CAR_COUNT = 40

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

CAR_MAX_VELOCITY = 10

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
Wall (View)
"""
WALL_COLOR = Color('black')

"""
Goal (View)
"""
GOAL_COLOR = Color('blue')

"""
Car (View)
"""
CAR_IMAGE_PATH = "car.png"

VECTOR_COLOR = Color('red')


def load_scenario(scenario: Callable[[], World]) -> World:
    return scenario()


def open_scenario() -> World:
    world = World(WORLD_WIDTH, WORLD_HEIGHT)

    for i in range(CAR_COUNT):
        car_x = randrange(1, WORLD_WIDTH)
        car_y = randrange(1, WORLD_HEIGHT)
        car_direction = Vector(WORLD_WIDTH / 2 - car_x, WORLD_HEIGHT / 2 - car_y)
        car_angle = car_direction.get_degrees()
        new_car = Car(CAR_LENGTH, CAR_WIDTH, CAR_WHEELBASE, CAR_MAX_VELOCITY, CAR_MAX_ACCELERATION,
                      CAR_MAX_STEERING_ANGLE, CAR_MAX_STEERING_CHANGE, x=car_x, y=car_y,
                      acceleration=2, steering_angle=0, angle=car_angle)
        world.cars.append(new_car)

    world.rule_weights = [1, 4, 1, 0, 0]

    return world


def box_scenario() -> World:
    world = World(WORLD_WIDTH, WORLD_HEIGHT)

    world.walls = [
        Wall(0.0, 0.0, world.width, 0.0),
        Wall(0.0, 0.0, 0.0, world.height),
        Wall(world.width, 0.0, world.width, world.height),
        Wall(0.0, world.height, world.width, world.height)
    ]

    for i in range(CAR_COUNT):
        car_x = randrange(1, WORLD_WIDTH)
        car_y = randrange(1, WORLD_HEIGHT)
        car_direction = Vector(WORLD_WIDTH / 2 - car_x, WORLD_HEIGHT / 2 - car_y)
        car_angle = car_direction.get_degrees()
        new_car = Car(CAR_LENGTH, CAR_WIDTH, CAR_WHEELBASE, CAR_MAX_VELOCITY, CAR_MAX_ACCELERATION,
                      CAR_MAX_STEERING_ANGLE, CAR_MAX_STEERING_CHANGE, x=car_x, y=car_y,
                      acceleration=2, steering_angle=0, angle=car_angle)
        world.cars.append(new_car)

    world.rule_weights = [1, 5, 1, 0, 1]

    return world


def road_scenario1() -> World:
    world = World(WORLD_WIDTH, WORLD_HEIGHT)

    road_length = 50
    road_width = 50

    x1 = world.width / 2 - road_length / 2
    x2 = world.width / 2 + road_length / 2

    y1 = world.height / 2 - road_width / 2
    y2 = world.height / 2 + road_width / 2

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

    for i in range(CAR_COUNT):
        car_x = randrange(1, x1)
        car_y = randrange(1, WORLD_HEIGHT)
        car_direction = Vector(x1 / 2 - car_x, WORLD_HEIGHT / 2 - car_y)
        car_angle = car_direction.get_degrees()
        new_car = Car(CAR_LENGTH, CAR_WIDTH, CAR_WHEELBASE, CAR_MAX_VELOCITY, CAR_MAX_ACCELERATION,
                      CAR_MAX_STEERING_ANGLE, CAR_MAX_STEERING_CHANGE, x=car_x, y=car_y,
                      acceleration=2, steering_angle=0, angle=car_angle)
        world.cars.append(new_car)

    world.rule_weights = [1, 1, 1, 0, 0]

    world.goal = Goal(WORLD_WIDTH * 0.8, WORLD_HEIGHT * 0.2)
    return world
