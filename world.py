from typing import List, Tuple

from car import Car

from math import sqrt, inf
from operator import itemgetter

from wall import Wall


class World:

    def __init__(self, width: int, height: int):
        self.width: int = width
        self.height: int = height
        self.cars: List[Car] = []
        self.walls: List[Wall] = []

    def update(self, dt: float, neighbor_count: int, wall_radius: float, separation_radius: float):
        for car in self.cars:
            car.adjust_behavior(self.get_neighbors(car, neighbor_count), self.walls, wall_radius, separation_radius)
        for car in self.cars:
            car.update(dt, self.walls)

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
