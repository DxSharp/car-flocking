from typing import Callable, List, Tuple, Any

import pygame
from pygame import Color

from world import World
from world_view import draw_world

from config import *


class Scenario:

    def __init__(self, world_generator: Callable[[Any], World], steps_per_second: int, neighbor_count: int,
                 rule_weights: List[float], simulation_time: int, goal_flocking: bool = False):
        self.world_generator = world_generator
        self.goal_flocking = goal_flocking
        self.steps_per_second = steps_per_second
        self.neighbor_count = neighbor_count
        self.rule_weights = rule_weights
        self.simulation_time = simulation_time

    def simulate(self, *generator_args: Any):
        world = self.world_generator(generator_args)
        goal_reached = not self.goal_flocking
        step_counter = 0
        dt = 1.0 / self.steps_per_second
        while not goal_reached:
            goal_reached = world.update(dt, self.neighbor_count, self.rule_weights)
            step_counter += 1

        steps_to_goal = step_counter

        step_goal = self.simulation_time * self.steps_per_second
        step_counter = 0
        while step_counter < step_goal:
            world.update(dt, self.neighbor_count, self.rule_weights)
            step_counter += 1

        return world.collision_distribution, world.flocking_performance_distribution, steps_to_goal

    def simulate_visual(self, pixel_meter_ratio: int, world_color: Color, goal_color: Color, vector_color: Color,
                        car_image_path: str, *generator_args: Any):
        print(type(generator_args))
        world = self.world_generator(generator_args)
        goal_reached = not self.goal_flocking
        step_counter = 0

        pygame.init()
        screen = pygame.display.set_mode((world.width * pixel_meter_ratio, world.height * pixel_meter_ratio))
        running = True
        clock = pygame.time.Clock()

        while not goal_reached and running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
            dt = clock.get_time() / 1000.0
            if dt > 1.0 / (self.steps_per_second - 1):
                print("Not enough time to compute the amount of steps per second in real-time")
            goal_reached = world.update(dt, self.neighbor_count, self.rule_weights)
            step_counter += 1

            draw_world(world, world_color, goal_color, vector_color, pygame.image.load(car_image_path),
                       screen, pixel_meter_ratio)

            pygame.display.update()
            clock.tick_busy_loop(self.steps_per_second)

        steps_to_goal = step_counter

        step_goal = self.simulation_time * self.steps_per_second
        step_counter = 0
        while step_counter < step_goal and running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
            dt = clock.get_time() / 1000.0
            if dt > 1.0 / (self.steps_per_second - 1):
                print("Not enough time to compute the amount of steps per second in real-time")
            world.update(dt, self.neighbor_count, self.rule_weights)
            step_counter += 1

            draw_world(world, world_color, goal_color, vector_color, pygame.image.load(car_image_path),
                       screen, pixel_meter_ratio)

            pygame.display.update()
            clock.tick_busy_loop(self.steps_per_second)

        return world.collision_distribution, world.flocking_performance_distribution, steps_to_goal


def open_scenario(generator_args: Any) -> World:
    world = World(WORLD_WIDTH, WORLD_HEIGHT)

    for i in range(generator_args[0]):
        car_x = randrange(1, WORLD_WIDTH)
        car_y = randrange(1, WORLD_HEIGHT)
        car_angle = randrange(0, 360)
        new_car = Car(CAR_LENGTH, CAR_WIDTH, CAR_WHEELBASE, CAR_MAX_VELOCITY, CAR_MAX_ACCELERATION,
                      CAR_MAX_STEERING_ANGLE, CAR_MAX_STEERING_CHANGE, x=car_x, y=car_y,
                      acceleration=2, steering_angle=0, angle=car_angle)
        world.cars.append(new_car)

    return world


s = Scenario(open_scenario, STEPS_PER_SECOND, NEIGHBOR_COUNT, OPTIMIZED_WEIGHTS, 10)

s.simulate_visual(PIXEL_METER_RATIO, WORLD_COLOR, GOAL_COLOR, VECTOR_COLOR, CAR_IMAGE_PATH, 50)
