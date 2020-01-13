from pygame.surface import Surface
from pygame.draw import line
from pygame import Color

from vector import Vector


def draw_vector(vector: Vector, color: Color, width: int, surface: Surface, pixel_meter_ratio: float):
    surface_x = vector.x * pixel_meter_ratio
    surface_y = surface.get_height() - vector.y * pixel_meter_ratio
    line(surface, color, (0.0, 0.0), (surface_x, surface_y), width)
