from pygame.surface import Surface
from pygame.transform import rotate, scale
from pygame.draw import line
from pygame import Color

from car import Car


def draw_car(car: Car, image: Surface, vector_color: Color, surface: Surface, pixel_meter_ratio: float):
    resized_image = scale(image, (round(car.length * pixel_meter_ratio), round(car.width * pixel_meter_ratio)))
    rotated_image = rotate(resized_image, car.direction.get_degrees())
    rect = rotated_image.get_rect()
    surface_x = car.x * pixel_meter_ratio - rect.width / 2.0
    surface_y = surface.get_height() - car.y * pixel_meter_ratio - rect.height / 2.0
    surface.blit(rotated_image, (surface_x, surface_y))
    # TODO: Remove code below this
    car_x = car.x * pixel_meter_ratio
    car_y = surface.get_height() - car.y * pixel_meter_ratio
    vector_x = (car.x + car.vector.x) * pixel_meter_ratio
    vector_y = surface.get_height() - (car.y + car.vector.y) * pixel_meter_ratio
    line(surface, vector_color, (car_x, car_y), (vector_x, vector_y), 3)
