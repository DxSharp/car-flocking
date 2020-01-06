from pygame.surface import Surface
from pygame.transform import rotate, scale

from car import Car


def draw_car(car: Car, image: Surface, surface: Surface, pixel_meter_ratio: float):
    resized_image = scale(image, (round(car.length * pixel_meter_ratio), round(car.width * pixel_meter_ratio)))
    rotated_image = rotate(resized_image, car.direction.get_degrees())
    rect = rotated_image.get_rect()
    surface_x = car.x * pixel_meter_ratio - rect.width / 2.0
    surface_y = surface.get_height() - car.y * pixel_meter_ratio - rect.height / 2.0
    surface.blit(rotated_image, (surface_x, surface_y))
