"""This module contains functions to visualize a Car object on a Pygame Surface.

A car is visually represented by an image. This image is scaled and positioned
according to the corresponding car object. Furthermore, the flocking vector of
the car is drawn on top of the image. The position of the vector is relative
to the car and in accordance with the corresponding vector object. The color of
the vector can be specified and its thickness is fixed at 1 pixel.

"""

from pygame.surface import Surface
from pygame.transform import rotate, scale
from pygame.draw import line
from pygame import Color
from car import Car


def draw_car(car: Car, image: Surface, vector_color: Color, surface: Surface, pixel_meter_ratio: float):
    """Draws a given Car object on a given Surface.

    Args:
        car (Car): The car object to be visualized.
        image (Surface): A surface containing an image visualizing a car
        vector_color (Color): The color the flocking vector should be
        surface (Surface): The surface the car should be drawn on.
        pixel_meter_ratio (float): The amount of pixels corresponding to one meter.

    """
    resized_image = scale(image, (round(car.length * pixel_meter_ratio), round(car.width * pixel_meter_ratio)))
    rotated_image = rotate(resized_image, car.direction.get_degrees())
    rect = rotated_image.get_rect()
    surface_x = car.x * pixel_meter_ratio - rect.width / 2.0
    surface_y = surface.get_height() - car.y * pixel_meter_ratio - rect.height / 2.0
    surface.blit(rotated_image, (surface_x, surface_y))

    car_x = car.x * pixel_meter_ratio
    car_y = surface.get_height() - car.y * pixel_meter_ratio
    vector_x = (car.x + car.vector.x) * pixel_meter_ratio
    vector_y = surface.get_height() - (car.y + car.vector.y) * pixel_meter_ratio
    line(surface, vector_color, (car_x, car_y), (vector_x, vector_y), 1)
