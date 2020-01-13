from pygame.surface import Surface
from pygame import Color
from pygame.draw import circle

from goal import Goal


def draw_goal(goal: Goal, color: Color, surface: Surface, pixel_meter_ratio: float):
    surface_x = goal.x * pixel_meter_ratio
    surface_y = surface.get_height() - goal.y * pixel_meter_ratio
    circle(surface, color, (int(surface_x), int(surface_y)), 5)
