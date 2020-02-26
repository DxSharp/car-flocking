"""This module contains functions to visualize a World object on a Pygame Surface.

A world is visually represented as the background of the surface, with a
specifiable color. The objects present in this world (cars, walls, cars) are
drawn on top of this background.

"""

from pygame.surface import Surface
from pygame import Color
from car_view import draw_car
from goal_view import draw_goal
from world import World


def draw_world(world: World, world_color: Color, goal_color: Color, vector_color: Color,
               car_image: Surface, surface: Surface, pixel_meter_ratio: float):
    """Draws a given World object on a given Surface.

    Args:
        world (World): The world object to be visualized.
        world_color (Color): The color the world should be, i.e., the background color.
        goal_color (Color): The color goals should be.
        vector_color (Color): The color of flocking vectors originating from cars.
        car_image (Surface): A surface containing the image visualizing a car.
        surface (Surface): The surface the world should be drawn on.
        pixel_meter_ratio (float): The amount of pixels corresponding to one meter.

    """
    surface.fill(world_color)
    for car in world.cars:
        draw_car(car, car_image, vector_color, surface, pixel_meter_ratio)
    draw_goal(world.goal, goal_color, surface, pixel_meter_ratio)
