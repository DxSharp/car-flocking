from pygame.surface import Surface
from pygame.draw import line
from pygame import Color

from wall import Wall


def draw_wall(wall: Wall, color: Color, surface: Surface, pixel_meter_ratio: float):
    surface_height = surface.get_height()
    surface_x1 = wall.x1 * pixel_meter_ratio
    surface_y1 = surface_height - wall.y1 * pixel_meter_ratio
    surface_x2 = wall.x2 * pixel_meter_ratio
    surface_y2 = surface_height - wall.y2 * pixel_meter_ratio

    line(surface, color, (surface_x1, surface_y1), (surface_x2, surface_y2), 3)
