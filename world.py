from typing import List, Tuple

from car import Car

from math import sqrt, inf
from operator import itemgetter

from wall import Wall


class World:

    def __init__(self, width: int, height: int, cars: List[Car] = None):
        self.width: int = width
        self.height: int = height
        if cars is None:
            self.cars: List[Car] = []
        else:
            self.cars: List[Car] = cars
        self.walls: List[Wall] = [
            Wall(0.0, 0.0, width, 0.0),
            Wall(0.0, 0.0, 0.0, height),
            Wall(width, 0.0, width, height),
            Wall(0.0, height, width, height)
        ]

    def update(self, dt: float, neighbor_count: int):
        for car in self.cars:
            car.adjust_behavior(self.get_neighbors(car, neighbor_count))
        for car in self.cars:
            car.update(dt)
        self.wrap_world()

    def wrap_world(self):
        for car in self.cars:
            if car.x > self.width:
                car.x -= self.width
            elif car.x < 0:
                car.x += self.width

            if car.y > self.height:
                car.y -= self.height
            elif car.y < 0:
                car.y += self.height

    def get_neighbors(self, car: Car, neighbor_count: int):
        neighbors = [(None, inf)] * neighbor_count
        for c in self.cars:
            if c != car:
                x_dif = car.x - c.x
                if x_dif > self.width / 2.0:
                    x_dif = car.x - (c.x + self.width)
                elif x_dif < -(self.width / 2.0):
                    x_dif = car.x - (c.x - self.width)

                y_dif = car.y - c.y
                if y_dif > self.height / 2.0:
                    y_dif = car.y - (c.y + self.height)
                elif y_dif < -(self.height / 2.0):
                    y_dif = car.y - (c.y - self.height)

                distance = sqrt(x_dif ** 2 + y_dif ** 2)

                neighbors.append((c, distance))
                neighbors.sort(key=itemgetter(1))
                neighbors.pop()
        return [n for (n, _) in neighbors]
