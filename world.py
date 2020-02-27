"""This module contains functionality to represent the world which contains all relevant elements of the simulation.

The world is represented as a plane with specified width and height. However, these dimensions are not enforced.
Therefore, cars can travel beyond these dimensions. The dimensions are used for the visual representation of the world.

"""

from typing import List, Tuple
from car import Car
from math import sqrt, inf
from operator import itemgetter
from goal import Goal


class World:

    def __init__(self, width: int, height: int):
        """Initializes a new world object.

        Args:
            width (float): The width of the world in meters.
            height (float): The height of the world in meters.

        """
        self.width: int = width
        self.height: int = height
        self.cars: List[Car] = []
        self.goal: Goal = Goal(0.0, 0.0, False)
        self.collision_distribution: List[int] = []
        self.flocking_performance_distribution: List[float] = []

    def update(self, dt: float, neighbor_count: int, rule_weights: List[float]) -> bool:
        """Updates the world and all elements in it according to the provided time step in seconds.

        Determines if all cars have reached the goal, returning True if so. Also determines and stores performance
        measures after updating.

        Args:
            dt (float): The amount of time in seconds to progress the simulation.
            neighbor_count (int): The amount of cars to incorporate into the neighborhood of each cars.
            rule_weights (List[float]): A list with the weights of each flocking force. The respective flocking forces
                are [Separation, Alignment, Cohesion, Goal].

        Returns:
            bool: True if all cars have reached the goal as a result of this update, False otherwise.

        """
        for car in self.cars:
            neighbors = self.get_neighbors(car, neighbor_count)
            car.adjust_behavior(neighbors, self.goal, rule_weights)
        for car in self.cars:
            car.update(dt)

        all_finished = True
        for car in self.cars:
            all_finished = all_finished and car.goal_reached

        self.collision_distribution.append(self.determine_collisions())
        self.flocking_performance_distribution.append(self.flocking_performance())
        return all_finished

    def get_neighbors(self, car: Car, neighbor_count: int) -> List[Tuple['Car', float]]:
        """Determines neighboring cars given some car and the amount of cars to include in the neighborhood.

        Args:
            car (Car): The car for which the neighborhood is to be determined.
            neighbor_count (int): The amount of cars to incorporate into the neighborhood.

        Returns:
            (List[Tuple[Car, float]]): A list of neighboring cars and the distance between the given car and each
                respective neighboring car.

        """
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

    def determine_collisions(self) -> int:
        """Determines the amount of collisions that occurred.

        Cars are considered to overlap when the distance between their midpoints is less than one car length. Cars are
        only considered collided if they were not overlapping in the previous time step, but are overlapping in the
        current time step. As a result, collisions are only counted once.

        Returns:
            int: The amount of collisions that have occurred as a result of the last time step.

        """
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
        return collision_count

    def flocking_performance(self) -> float:
        """Determines the mean squared error between the position of individual cars and the center of all cars.

        Can be used as a performance measure on the density of the flock.

        Returns:
            float: The mean squared error of distance between cars and the center of all cars.

        """
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
