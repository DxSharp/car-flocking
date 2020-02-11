import time
from typing import Tuple

import pygame

from config import *
from goal import Goal
from world_view import draw_world

NEW_STUFF = False

if not NEW_STUFF:

    world = load_scenario(open_scenario, [243, 27, 9, 0.4, 0], CAR_COUNT, CAR_MAX_VELOCITY)

    pygame.init()
    screen = pygame.display.set_mode((WORLD_WIDTH * PIXEL_METER_RATIO, WORLD_HEIGHT * PIXEL_METER_RATIO))

    running = True
    step_goal = SIMULATION_TIME * STEPS_PER_SECOND
    step_counter = 0
    clock = pygame.time.Clock()
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = pygame.mouse.get_pos()
                goal_x = mouse_pos[0] / PIXEL_METER_RATIO
                goal_y = WORLD_HEIGHT - mouse_pos[1] / PIXEL_METER_RATIO

                world.goal = Goal(goal_x, goal_y, True)
        dt = clock.get_time() / 1000.0
        if dt > 1.0 / (STEPS_PER_SECOND - 1):
            print("Not enough time to compute the amount of steps per second in real-time")

        if step_counter > STEPS_PER_SECOND * 2:
            world.count_collisions = True
        running = running and not world.update(dt, NEIGHBOR_COUNT, WALL_RADIUS, SEPARATION_RADIUS)

        draw_world(world, WORLD_COLOR, WALL_COLOR, GOAL_COLOR, VECTOR_COLOR, pygame.image.load(CAR_IMAGE_PATH),
                   screen, PIXEL_METER_RATIO)

        pygame.display.update()
        step_counter += 1
        clock.tick_busy_loop(STEPS_PER_SECOND)
    print(world.flocking_performance_distribution)

else:

    def run_simulation(scenario: Callable[[], World], weights: List[float], simulation_amount: int, car_count: int,
                       car_velocity: float) -> Tuple[List[List[int]], List[List[float]]]:
        collision_distributions = []
        flocking_distributions = []
        for i in range(simulation_amount):
            start_time = time.time()
            world = load_scenario(scenario, weights, car_count, car_velocity)
            step_goal = SIMULATION_TIME * STEPS_PER_SECOND
            step_counter = 0
            while step_counter < step_goal:
                dt = 1.0 / STEPS_PER_SECOND
                world.update(dt, NEIGHBOR_COUNT, WALL_RADIUS, SEPARATION_RADIUS)
                step_counter += 1
            collision_distributions.append(world.collision_distribution)
            flocking_distributions.append(world.flocking_performance_distribution)
            stop_time = time.time()
            print("Car Velocity", car_velocity, "| Simulation Number", i + 1, "| Time Taken", stop_time - start_time)
        return collision_distributions, flocking_distributions


    def conditional_simulation(scenario: Callable[[], World], weights: List[float], simulation_amount: int,
                               car_count: int, car_velocity: float) -> Tuple[
        List[List[int]], List[List[float]], float, float, List[float]]:
        collision_distributions = []
        flocking_distributions = []
        collision_sum = 0
        steps_sum = 0
        goal_step_distribution = []
        for i in range(simulation_amount):
            start_time = time.time()
            world = load_scenario(scenario, weights, car_count, car_velocity)
            goal_reached = False
            step_counter = 0
            while not goal_reached:
                dt = 1.0 / STEPS_PER_SECOND
                goal_reached = world.update(dt, NEIGHBOR_COUNT, WALL_RADIUS, SEPARATION_RADIUS)
                step_counter += 1

            steps_sum += step_counter
            goal_step_distribution.append(step_counter)

            step_goal = SIMULATION_TIME * STEPS_PER_SECOND
            step_counter = 0
            while step_counter < step_goal:
                dt = 1.0 / STEPS_PER_SECOND
                world.update(dt, NEIGHBOR_COUNT, WALL_RADIUS, SEPARATION_RADIUS)
                step_counter += 1

            collision_distributions.append(world.collision_distribution)
            flocking_distributions.append(world.flocking_performance_distribution)

            collision_sum += world.total_collisions

            stop_time = time.time()
            print("Car Velocity", car_velocity, "| Simulation Number", i + 1, "| Time Taken", stop_time - start_time)
        return collision_distributions, flocking_distributions, collision_sum / simulation_amount, \
               steps_sum / simulation_amount, goal_step_distribution


    # file1 = open("collisions_velocity_goal.txt", "w+")
    # file2 = open("flocking_velocity_goal.txt", "w+")
    # file3 = open("steps_velocity_goal.txt", "w+")

    # for cv in range(3, 33, 3):
    #     c, f, x, y, g = conditional_simulation(goal_scenario, [OPTIMIZED_WEIGHTS[0], OPTIMIZED_WEIGHTS[1],
    #                                                            OPTIMIZED_WEIGHTS[2], OPTIMIZED_WEIGHTS[3], 0],
    #                                            50, CAR_COUNT, cv)
    #
    #     for i in c:
    #         for j in i:
    #             file1.write(str(j))
    #             file1.write('\t')
    #         file1.write('\n')
    #
    #     for i in f:
    #         for j in i:
    #             file2.write(str(j))
    #             file2.write('\t')
    #         file2.write('\n')
    #
    #     for i in g:
    #         file3.write(str(i))
    #         file3.write('\t')
    #
    #     file1.write('\n')
    #     file2.write('\n')
    #     file3.write('\n')
    #     file3.write('\n')
    #
    # file1.close()
    # file2.close()
    # file3.close()

    # file1 = open("collisions_car_count_goal.txt", "w+")
    # file2 = open("flocking_car_count_goal.txt", "w+")
    # file3 = open("steps_car_count_goal.txt", "w+")
    #
    # for cc in range(10, 110, 10):
    #     c, f, x, y, g = conditional_simulation(goal_scenario, [OPTIMIZED_WEIGHTS[0], OPTIMIZED_WEIGHTS[1],
    #                                                            OPTIMIZED_WEIGHTS[2], OPTIMIZED_WEIGHTS[3], 0],
    #                                            20, cc, CAR_MAX_VELOCITY)
    #
    #     for i in c:
    #         for j in i:
    #             file1.write(str(j))
    #             file1.write('\t')
    #         file1.write('\n')
    #
    #     for i in f:
    #         for j in i:
    #             file2.write(str(j))
    #             file2.write('\t')
    #         file2.write('\n')
    #
    #     for i in g:
    #         file3.write(str(i))
    #         file3.write('\t')
    #
    #     file1.write('\n')
    #     file2.write('\n')
    #     file3.write('\n')
    #     file3.write('\n')
    #
    # file1.close()
    # file2.close()
    # file3.close()

    # file1 = open("collisions_time_goal.txt", "w+")
    # file2 = open("flocking_time_goal.txt", "w+")
    # file3 = open("steps_taken_goal.txt", "w+")

    # c, f, x, y, g = conditional_simulation(goal_scenario, [OPTIMIZED_WEIGHTS[0], OPTIMIZED_WEIGHTS[1],
    #                                                        OPTIMIZED_WEIGHTS[2], OPTIMIZED_WEIGHTS[3], 0],
    #                                        100, CAR_COUNT, CAR_MAX_VELOCITY)
    #
    # for i in c:
    #     for j in i:
    #         file1.write(str(j))
    #         file1.write('\t')
    #     file1.write('\n')
    #
    # for i in f:
    #     for j in i:
    #         file2.write(str(j))
    #         file2.write('\t')
    #     file2.write('\n')
    #
    # for i in g:
    #     file3.write(str(i))
    #     file3.write('\t')
    #
    # file1.write('\n')
    # file2.write('\n')
    # file3.write('\n')
    #
    # file1.close()
    # file2.close()
    # file3.close()

    # possible_weights = [0.1, 0.2, 0.4, 0.8, 1, 2, 4, 8]
    #
    # collision_results = []
    # steps_results = []
    # for w in possible_weights:
    #     x, y, c, s = conditional_simulation(goal_scenario,
    #                                         [OPTIMIZED_WEIGHTS[0], OPTIMIZED_WEIGHTS[1], OPTIMIZED_WEIGHTS[2],
    #                                          w, 0], 50, CAR_COUNT, CAR_MAX_VELOCITY)
    #     collision_results.append(c)
    #     steps_results.append(s)
    #
    # print(collision_results)
    # print(steps_results)

    # file1 = open("collisions_velocity.txt", "w+")
    # file2 = open("flocking_velocity.txt", "w+")
    #
    # for cv in range(3, 33, 3):
    #     c, f = run_simulation(open_scenario, [OPTIMIZED_WEIGHTS[0], OPTIMIZED_WEIGHTS[1], OPTIMIZED_WEIGHTS[2], 0, 0],
    #                           50, CAR_COUNT, cv)
    #
    #     for i in c:
    #         for j in i:
    #             file1.write(str(j))
    #             file1.write('\t')
    #         file1.write('\n')
    #
    #     for i in f:
    #         for j in i:
    #             file2.write(str(j))
    #             file2.write('\t')
    #         file2.write('\n')
    #
    #     file1.write('\n')
    #     file2.write('\n')
    #
    # file1.close()
    # file2.close()

    # file1 = open("collisions_car_count.txt", "w+")
    # file2 = open("flocking_car_count.txt", "w+")
    #
    # for cc in range(10, 110, 10):
    #     c, f = run_simulation(open_scenario, [OPTIMIZED_WEIGHTS[0], OPTIMIZED_WEIGHTS[1], OPTIMIZED_WEIGHTS[2], 0, 0],
    #                           50, cc)
    #
    #     for i in c:
    #         for j in i:
    #             file1.write(str(j))
    #             file1.write('\t')
    #         file1.write('\n')
    #
    #     for i in f:
    #         for j in i:
    #             file2.write(str(j))
    #             file2.write('\t')
    #         file2.write('\n')
    #
    #     file1.write('\n')
    #     file2.write('\n')
    #
    # file1.close()
    # file2.close()

    # start = time.time()
    # c, f = run_simulation(open_scenario, [OPTIMIZED_WEIGHTS[0], OPTIMIZED_WEIGHTS[1], OPTIMIZED_WEIGHTS[2], 0, 0], 100)
    # stop = time.time()
    # print(stop - start)
    #
    # file1 = open("collisions_time.txt", "w+")
    #
    # for i in c:
    #     for j in i:
    #         file1.write(str(j))
    #         file1.write('\t')
    #     file1.write('\n')
    #
    # file2 = open("flocking_time.txt", "w+")
    #
    # for i in f:
    #     for j in i:
    #         file2.write(str(j))
    #         file2.write('\t')
    #     file2.write('\n')
