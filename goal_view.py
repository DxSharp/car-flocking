"""This module contains functions to visualize a Goal object on a Pygame Surface.

A goal is visually represented as a filled circle with a radius of 5 pixels and
a specifiable color. The position is the determined by the corresponding goal
object.

"""

from pygame.surface import Surface
from pygame import Color
from pygame.draw import circle
from goal import Goal


def draw_goal(goal: Goal, color: Color, surface: Surface, pixel_meter_ratio: float):
    """Draws a given Goal object on a given Surface.

    Args:
        goal (Goal): The goal object to be visualized.
        color (Color): The color the goal should be.
        surface (Surface): The surface the goal should be drawn on.
        pixel_meter_ratio (float): The amount of pixels corresponding to one meter.

    """
    surface_x = goal.x * pixel_meter_ratio
    surface_y = surface.get_height() - goal.y * pixel_meter_ratio
    circle(surface, color, (int(surface_x), int(surface_y)), 5)
