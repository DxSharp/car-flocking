from typing import List, Tuple

from vector import Vector
from math import radians, tan, sqrt, degrees

from wall import Wall


class Car:

    def __init__(self, length: float, width: float, wheelbase: float, max_velocity: float, max_acceleration: float,
                 max_steering_angle: float, max_steering_change: float, x: float = 0, y: float = 0, angle: float = 0,
                 velocity: float = 0, steering_angle: float = 0, acceleration: float = 0, steering_change: float = 0):
        self.length: float = length
        self.width: float = width
        self.wheelbase: float = wheelbase

        self.x: float = x
        self.y: float = y
        self.direction = Vector.from_degrees(angle)
        self.steering_angle: float = radians(steering_angle)

        self.velocity: float = velocity
        self.steering_change: float = radians(steering_change)

        self.acceleration: float = acceleration

        self.max_velocity: float = max_velocity
        self.max_acceleration: float = max_acceleration
        self.max_steering_angle: float = radians(max_steering_angle)
        self.max_steering_change: float = radians(max_steering_change)

        # TODO: Remove code below this
        self.vector = Vector()


    def update(self, dt: float):
        x_change = self.velocity * self.direction.x
        y_change = self.velocity * self.direction.y
        angle_change = tan(self.steering_angle) * self.velocity / self.wheelbase

        self.x += x_change * dt
        self.y += y_change * dt
        self.direction = self.direction.rotate_radians(angle_change * dt)

        new_velocity = self.velocity + self.acceleration * dt
        new_steering_angle = self.steering_angle + self.steering_change * dt

        self.velocity = min(self.max_velocity, new_velocity)
        self.steering_angle = max(-self.max_steering_angle, min(new_steering_angle, self.max_steering_angle))

    def adjust_behavior(self, neighbors: List[Tuple['Car', float]], walls: List[Wall], wall_radius: float):
        wall_vector = self.wall_avoidance(walls, wall_radius)
        self.vector = wall_vector
        # for wall in walls:
        #     steering_vector = wall.perpendicular_vector(self.x, self.y)
        #     steering_force = steering_vector.change_length(1.0 / steering_vector.get_length())
        #     wall_force += steering_force
        #     print(steering_force)
        # print('---')
        # print(wall_force)
        # print(wall_force.angle_to(self.direction))
        # print(self.steering_angle)
        # print()
        steering_direction = self.direction.rotate_radians(self.steering_angle)



        angle_dif = steering_direction.angle_to(wall_vector)

        print(self.steering_angle)

        print(angle_dif)
        print()
        if angle_dif > 0:
            self.steering_change = self.max_steering_change
        elif angle_dif < 0:
            self.steering_change = -self.max_steering_change
        elif self.steering_angle > 0:
            self.steering_change = -self.max_steering_change
        else:
            self.steering_change = self.max_steering_change



    def wall_avoidance(self, walls: List[Wall], wall_radius) -> 'Vector':
        wall_force = Vector()
        for wall in walls:
            steering_vector = wall.perpendicular_vector(self.x, self.y)
            vector_length = steering_vector.get_length()
            if vector_length < wall_radius:
                steering_force = steering_vector.change_length(wall_radius - vector_length)
                wall_force += steering_force
        return wall_force

    def separation(self, neighbors: List[Tuple['Car', float]]) -> Vector:
        radius = 0.0
        for neighbor in neighbors:
            distance = neighbor[1]
            if distance > radius:
                radius = distance

        total_length = 0.0
        for neighbor in neighbors:
            distance = neighbor[1]
            total_length += radius - distance

        total_force = Vector()
        for neighbor in neighbors:
            n = neighbor[0]
            distance = neighbor[1]
            separation_vector = Vector(self.x - n.x, self.y - n.y)
            separation_force = ((radius - distance) ** 2) / total_length
            total_force += separation_vector.change_length(separation_force)
        return total_force

    def alignment(self, neighbors: List[Tuple['Car', float]]) -> float:
        direction_average = Vector()
        for neighbor in neighbors:
            direction_average += neighbor.direction
        return self.direction.angle_to(direction_average)

    def cohesion(self, neighbors: List[Tuple['Car', float]]) -> Vector:
        x_summation = 0
        y_summation = 0
        for neighbor in neighbors:
            x_summation += neighbor.x
            y_summation += neighbor.y
        neighbor_count = len(neighbors)
        x_average = x_summation / neighbor_count
        y_average = y_summation / neighbor_count
        return Vector(x_average - self.x, y_average - self.y)
