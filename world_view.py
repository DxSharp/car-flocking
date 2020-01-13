from pygame.surface import Surface
from pygame import Color

from car_view import draw_car
from goal_view import draw_goal
from wall_view import draw_wall
from world import World


def draw_world(world: World, world_color: Color, wall_color: Color, goal_color: Color, vector_color: Color,
               car_image: Surface, surface: Surface, pixel_meter_ratio: float):
    surface.fill(world_color)
    for wall in world.walls:
        draw_wall(wall, wall_color, surface, pixel_meter_ratio)
    for car in world.cars:
        draw_car(car, car_image, vector_color, surface, pixel_meter_ratio)
    draw_goal(world.goal, goal_color, surface, pixel_meter_ratio)
