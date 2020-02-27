"""This module contains functionality to configure all elements for a simulation into one object.

The core of a scenario is the world generator function passed upon initialization. The world returned by this function
should already contain all objects such as cars, therefore configuring the parameters of these elements. These
parameters can be made variable by passing keyword arguments to this generator function.

"""

from typing import Callable, List
import pygame
from pygame import Color
from world import World
from world_view import draw_world


class Scenario:

    def __init__(self, world_generator: Callable[..., World], steps_per_second: int, neighbor_count: int,
                 rule_weights: List[float], simulation_time: int):
        """Initializes a new scenario object.

        Args:
            world_generator (Callable[..., World]): A function that generates the world to use in this scenario, given
                any number of keyword arguments corresponding to simulation variables.
            steps_per_second (int): The amount of steps to calculate within each second.
            neighbor_count (int): The amount of neighbors that cars should take into account for flocking.
            rule_weights (List[float]): A list with the weights of each flocking force. The respective flocking forces
                are [Separation, Alignment, Cohesion, Goal].
            simulation_time (int): The amount of time in seconds to simulate the scenario, after the goal is reached.

        """
        self.world_generator = world_generator
        self.steps_per_second = steps_per_second
        self.neighbor_count = neighbor_count
        self.rule_weights = rule_weights
        self.simulation_time = simulation_time

    def simulate(self, **simulation_variables: ...):
        """Simulates this scenario given its simulation variables.

        The simulation variables are passed to the world generator function which was specified upon initialization
        of this scenario. These variables can be used to easily vary simulation parameters over multiple runs.

        Args:
            simulation_variables (...): The variables to be passed to the world generator.

        Returns:
            List[int]: Time series of the collisions measured during the simulation.
            List[float]: Time series of the flocking density measured during the simulation.
            int: The amount of steps after which the goal was reached. Always 0 if there is no active goal.

        """
        world = self.world_generator(simulation_variables)
        goal_reached = not world.goal.active
        dt = 1.0 / self.steps_per_second

        step_counter = 0
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
                        car_image_path: str, **simulation_variables: ...):
        """Simulates this scenario visually in real-time given its simulation variables.

        The simulation variables are passed to the world generator function which was specified upon initialization
        of this scenario. These variables can be used to easily vary simulation parameters over multiple runs. The other
        arguments customize the visual representation of the simulation.

        With a visual simulation, the steps will be processed in real-time. However, if the simulation is too
        computationally complex, the time required to calculate the next time can exceed the duration of the time step.
        If this is the case, notice is given via a print statement. Note that the resulting performance measure
        distributions will be inaccurate as a result.

        Args:
            simulation_variables (...): The variables to be passed to the world generator.
            pixel_meter_ratio (int): The amount of pixels corresponding to one meter.
            world_color (Color): The color the world should be, i.e., the background color.
            goal_color (Color): The color goals should be.
            vector_color (Color): The color of flocking vectors originating from cars.
            car_image_path (str): The filepath to the image visualizing a car.

        Returns:
            List[int]: Time series of the collisions measured during the simulation.
            List[float]: Time series of the flocking density measured during the simulation.
            int: The amount of steps after which the goal was reached. Always 0 if there is no active goal.

        """
        world = self.world_generator(simulation_variables)
        goal_reached = not world.goal.active

        pygame.init()
        screen = pygame.display.set_mode((world.width * pixel_meter_ratio, world.height * pixel_meter_ratio))

        step_counter = 0
        running = True
        clock = pygame.time.Clock()
        while not goal_reached and running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False

            dt = clock.get_time() / 1000.0
            if dt > 1.0 / (self.steps_per_second - 1):
                print("Could not compute steps per second in real-time")

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
                print("Could not compute steps per second in real-time")

            world.update(dt, self.neighbor_count, self.rule_weights)
            step_counter += 1

            draw_world(world, world_color, goal_color, vector_color, pygame.image.load(car_image_path),
                       screen, pixel_meter_ratio)
            pygame.display.update()
            clock.tick_busy_loop(self.steps_per_second)

        return world.collision_distribution, world.flocking_performance_distribution, steps_to_goal
