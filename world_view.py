from pygame.surface import Surface
from pygame import Color

from car_view import draw_car
from world import World


def draw_world(world: World, color: Color, car_image: Surface, surface: Surface, pixel_meter_ratio: float):
    surface.fill(color)
    for car in world.cars:
        draw_car(car, car_image, surface, pixel_meter_ratio)
