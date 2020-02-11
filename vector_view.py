"""This module contains functions to visualize a Vector object on a Pygame Surface.

A vector is visually represented as a line with a thickness of 1 pixel and a
specifiable color. The tail position is always the origin (0, 0). The head position
is determined by the corresponding vector object.

"""

from pygame.surface import Surface
from pygame.draw import line
from pygame import Color
from vector import Vector


def draw_vector(vector: Vector, color: Color, surface: Surface, pixel_meter_ratio: float):
    """Draws a given Vector object on a given Surface.

    Args:
        vector (Vector): The vector object to be visualized.
        color (Color): The color the vector should be.
        surface (Surface): The surface the vector should be drawn on.
        pixel_meter_ratio (float): The amount of pixels corresponding to one meter.

    """
    surface_x = vector.x * pixel_meter_ratio
    surface_y = surface.get_height() - vector.y * pixel_meter_ratio
    line(surface, color, (0.0, surface.get_height()), (surface_x, surface_y), 1)
