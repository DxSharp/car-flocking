from typing import List, Tuple

from car import Car

from math import sqrt, inf
from operator import itemgetter

from goal import Goal
from wall import Wall


class World:

    def __init__(self, width: int, height: int):
        self.width: int = width
        self.height: int = height
        self.cars: List[Car] = []
        self.walls: List[Wall] = []
        self.goal: Goal = Goal(0.0, 0.0, False)
        self.rule_weights: List[float] = [0, 0, 0, 0, 0]
        self.collision_distribution: List[int] = []
        self.flocking_performance_distribution: List[float] = []
        self.total_collisions: int = 0

    def update(self, dt: float, neighbor_count: int, wall_radius: float, separation_radius: float) -> bool:
        for car in self.cars:
            neighbors = self.get_neighbors(car, neighbor_count)
            car.adjust_behavior(neighbors, self.walls, wall_radius, separation_radius, self.goal, self.rule_weights)
        for car in self.cars:
            car.update(dt, self.walls)

        all_finished = True
        for car in self.cars:
            all_finished = all_finished and car.goal_reached

        self.determine_collisions()
        self.flocking_performance_distribution.append(self.flocking_performance())
        return all_finished

    def get_neighbors(self, car: Car, neighbor_count: int):
        neighbors = [(car, inf)] * neighbor_count
        for c in self.cars:
            if c != car:
                x_dif = car.x - c.x
                y_dif = car.y - c.y
                distance = sqrt(x_dif ** 2 + y_dif ** 2)
                neighbors.append((c, distance))
                neighbors.sort(key=itemgetter(1))
                neighbors.pop()
        return neighbors

    def determine_collisions(self):
        collision_count = 0
        car_count = len(self.cars)
        car_length = self.cars[0].length
        for i in range(car_count):
            for j in range(i + 1, car_count):
                car1 = self.cars[i]
                car2 = self.cars[j]
                x_dif = car1.x - car2.x
                y_dif = car1.y - car2.y
                distance = sqrt(x_dif ** 2 + y_dif ** 2)
                if car2 in car1.overlapping_cars:
                    if distance > car_length:
                        car1.overlapping_cars.remove(car2)
                elif distance < car_length:
                    car1.overlapping_cars.append(car2)
                    collision_count += 1
        self.total_collisions += collision_count
        self.collision_distribution.append(collision_count)

    def flocking_performance(self):
        sum_x = 0
        sum_y = 0
        for car in self.cars:
            sum_x += car.x
            sum_y += car.y
        avg_x = sum_x / len(self.cars)
        avg_y = sum_y / len(self.cars)

        sum_distance = 0
        for car in self.cars:
            x_dif = car.x - avg_x
            y_dif = car.y - avg_y
            distance = x_dif ** 2 + y_dif ** 2
            sum_distance += distance
        avg_distance = sum_distance / len(self.cars)
        return avg_distance
