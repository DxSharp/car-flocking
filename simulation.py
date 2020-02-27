"""This module contains example code to configure and run simulations.

"""

from random import randrange
from typing import Dict
from pygame import Color
from car import Car
from goal import Goal
from scenario import Scenario
from world import World

"""
-------------------
MODEL CONFIGURATION
-------------------
"""

"""
Simulation (Model)
"""
STEPS_PER_SECOND = 50

CAR_COUNT = 25

NEIGHBOR_COUNT = 6

SIMULATION_TIME = 30

OPTIMIZED_WEIGHTS = [243, 27, 9, 0.4]

"""
World (Model)
"""
WORLD_WIDTH = 300

WORLD_HEIGHT = 100

"""
Car (Model)
"""
CAR_LENGTH = 4.9

CAR_WIDTH = 1.8

CAR_WHEELBASE = 2.8

CAR_MAX_ACCELERATION = 5.0

CAR_MAX_VELOCITY = 5

CAR_MAX_STEERING_ANGLE = 37.0

CAR_MAX_STEERING_CHANGE = CAR_MAX_STEERING_ANGLE

"""
------------------
VIEW CONFIGURATION
------------------
"""

"""
Simulation (View)
"""
PIXEL_METER_RATIO = 8

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

"""
Vector (View)
"""
VECTOR_COLOR = Color('red')


def open_scenario(simulation_variables: Dict) -> World:
    world = World(WORLD_WIDTH, WORLD_HEIGHT)

    for i in range(simulation_variables['car_count']):
        car_x = randrange(1, WORLD_WIDTH)
        car_y = randrange(1, WORLD_HEIGHT)
        car_angle = randrange(0, 360)
        new_car = Car(CAR_LENGTH, CAR_WIDTH, CAR_WHEELBASE, CAR_MAX_VELOCITY, CAR_MAX_ACCELERATION,
                      CAR_MAX_STEERING_ANGLE, CAR_MAX_STEERING_CHANGE, x=car_x, y=car_y,
                      acceleration=2, steering_angle=0, angle=car_angle)
        world.cars.append(new_car)

    return world


def goal_scenario(simulation_variables: Dict) -> World:
    world = World(WORLD_WIDTH, WORLD_HEIGHT)

    for i in range(CAR_COUNT):
        car_x = randrange(1, WORLD_WIDTH / 3)
        car_y = randrange(1, WORLD_HEIGHT)
        car_angle = randrange(0, 360)
        new_car = Car(CAR_LENGTH, CAR_WIDTH, CAR_WHEELBASE, CAR_MAX_VELOCITY, CAR_MAX_ACCELERATION,
                      CAR_MAX_STEERING_ANGLE, CAR_MAX_STEERING_CHANGE, x=car_x, y=car_y,
                      acceleration=2, steering_angle=0, angle=car_angle)
        world.cars.append(new_car)

    world.goal = Goal(WORLD_WIDTH * 5 / 6, WORLD_HEIGHT / 2, True)

    return world


s = Scenario(goal_scenario, STEPS_PER_SECOND, NEIGHBOR_COUNT, OPTIMIZED_WEIGHTS, 10)

s.simulate_visual(PIXEL_METER_RATIO, WORLD_COLOR, GOAL_COLOR, VECTOR_COLOR, CAR_IMAGE_PATH)
