from random import randrange, uniform

import pygame
from pygame.constants import KEYDOWN, K_SPACE

from config import *
from world import World
from car import Car
from world_view import draw_world

DEBUG = False

world = World(WORLD_WIDTH, WORLD_HEIGHT)


for i in range(CAR_COUNT):
    # random_x = randrange(WORLD_WIDTH)
    # random_y = randrange(WORLD_HEIGHT)
    random_x = WORLD_WIDTH / 2.0
    random_y = WORLD_HEIGHT / 2.0

    random_angle = uniform(-CAR_MAX_STEERING_ANGLE, CAR_MAX_STEERING_ANGLE)
    new_car = Car(CAR_LENGTH, CAR_WIDTH, CAR_WHEELBASE, CAR_MAX_VELOCITY, CAR_MAX_ACCELERATION,
                  CAR_MAX_STEERING_ANGLE, CAR_MAX_STEERING_CHANGE, x=random_x, y=random_y,
                  acceleration=0, steering_angle=random_angle, angle=random_angle * 5.0, velocity=10)
    world.cars.append(new_car)

pygame.init()
screen = pygame.display.set_mode((WORLD_WIDTH * PIXEL_METER_RATIO, WORLD_HEIGHT * PIXEL_METER_RATIO))

if DEBUG:
    running = True
    while running:
        event = pygame.event.wait()
        if event.type == pygame.QUIT:
            running = False
        elif event.type == KEYDOWN and event.key == K_SPACE:
            world.update(1.0 / STEPS_PER_SECOND, NEIGHBOR_COUNT, WALL_RADIUS, SEPARATION_RADIUS)
            draw_world(world, WORLD_COLOR, WALL_COLOR, VECTOR_COLOR, pygame.image.load(CAR_IMAGE_PATH),
                       screen, PIXEL_METER_RATIO)
            pygame.display.update()
else:
    running = True
    clock = pygame.time.Clock()
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
        dt = clock.get_time() / 1000.0
        if dt > 1.0 / (STEPS_PER_SECOND - 1):
            print("Not enough time to compute the amount of steps per second in real-time")
        world.update(dt, NEIGHBOR_COUNT, WALL_RADIUS, SEPARATION_RADIUS)

        draw_world(world, WORLD_COLOR, WALL_COLOR, VECTOR_COLOR, pygame.image.load(CAR_IMAGE_PATH),
                   screen, PIXEL_METER_RATIO)

        pygame.display.update()

        clock.tick_busy_loop(STEPS_PER_SECOND)
