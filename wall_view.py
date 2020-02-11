"""This module contains functions to visualize a Wall object on a Pygame Surface.

A wall is visually represented by a line with a thickness of 3 pixels and a
specifiable color. The position and length are determined by the corresponding
wall object and the pixel-to-meter ratio.

"""

from pygame.surface import Surface
from pygame.draw import line
from pygame import Color
from wall import Wall


def draw_wall(wall: Wall, color: Color, surface: Surface, pixel_meter_ratio: float):
    """Draws a given Wall object on a given Surface.

    Args:
        wall (Wall): The wall object to be visualized.
        color (Color): The color the wall should be.
        surface (Surface): The surface the wall should be drawn on.
        pixel_meter_ratio (float): The amount of pixels corresponding to one meter.

    """
    surface_height = surface.get_height()
    surface_x1 = wall.x1 * pixel_meter_ratio
    surface_y1 = surface_height - wall.y1 * pixel_meter_ratio
    surface_x2 = wall.x2 * pixel_meter_ratio
    surface_y2 = surface_height - wall.y2 * pixel_meter_ratio

    line(surface, color, (surface_x1, surface_y1), (surface_x2, surface_y2), 3)
