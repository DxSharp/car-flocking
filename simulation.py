from random import randrange, uniform

import pygame
from pygame.constants import KEYDOWN, K_SPACE

from config import *
from goal import Goal
from world import World
from world_view import draw_world

DEBUG = False

world = World(WORLD_WIDTH, WORLD_HEIGHT)

road_scenario1(world, 50, 20)

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
            draw_world(world, WORLD_COLOR, WALL_COLOR, GOAL_COLOR, VECTOR_COLOR, pygame.image.load(CAR_IMAGE_PATH),
                       screen, PIXEL_METER_RATIO)
            pygame.display.update()
else:
    running = True
    clock = pygame.time.Clock()
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = pygame.mouse.get_pos()
                goal_x = mouse_pos[0] / PIXEL_METER_RATIO
                goal_y = WORLD_HEIGHT - mouse_pos[1] / PIXEL_METER_RATIO

                world.goal = Goal(goal_x, goal_y)
        dt = clock.get_time() / 1000.0
        if dt > 1.0 / (STEPS_PER_SECOND - 1):
            print("Not enough time to compute the amount of steps per second in real-time")
        world.update(dt, NEIGHBOR_COUNT, WALL_RADIUS, SEPARATION_RADIUS)

        draw_world(world, WORLD_COLOR, WALL_COLOR, GOAL_COLOR, VECTOR_COLOR, pygame.image.load(CAR_IMAGE_PATH),
                   screen, PIXEL_METER_RATIO)

        pygame.display.update()

        clock.tick_busy_loop(STEPS_PER_SECOND)
