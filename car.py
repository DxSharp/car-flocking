from typing import List

from vector import Vector
from math import radians, tan


class Car:

    def __init__(self, length: float, width: float, wheelbase: float, max_velocity: float, max_acceleration: float,
                 max_steering_angle: float, max_angle_change: float, x: float = 0, y: float = 0, angle: float = 0,
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
        self.max_angle_change: float = radians(max_angle_change)

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
        if new_steering_angle > self.max_steering_angle:
            self.steering_angle = self.max_steering_angle
        elif new_steering_angle < -self.max_steering_angle:
            self.steering_angle = -self.max_steering_angle
        else:
            self.steering_angle = new_steering_angle

    def adjust_behavior(self, neighbors: List['Car']):
        separation_force = self.separation(neighbors)
        alignment_angle = self.alignment(neighbors)
        cohesion_force = self.cohesion(neighbors)

        steer = self.direction.angle_to(cohesion_force)

        if steer > 0:
            self.steering_change = self.max_angle_change
        else:
            self.steering_change = -self.max_angle_change


        # if alignment_angle > self.max_steering_angle:
        #     self.steering_change = self.max_angle_change
        # elif alignment_angle < -self.max_steering_angle:
        #     self.steering_change = -self.max_angle_change
        # else:
        #     self.steering_change = self.max_angle_change * alignment_angle / self.max_steering_angle

    def separation(self, neighbors: List['Car']) -> Vector:
        total_force = Vector()
        for neighbor in neighbors:
            separation_force = Vector(self.x - neighbor.x, self.y - neighbor.y)
            steering_force = separation_force / (separation_force.get_length() ** 2)
            total_force += steering_force
        return total_force

    def alignment(self, neighbors: List['Car']) -> float:
        direction_average = Vector()
        for neighbor in neighbors:
            direction_average += neighbor.direction
        return self.direction.angle_to(direction_average)

    def cohesion(self, neighbors: List['Car']) -> Vector:
        x_summation = 0
        y_summation = 0
        for neighbor in neighbors:
            x_summation += neighbor.x
            y_summation += neighbor.y
        neighbor_count = len(neighbors)
        x_average = x_summation / neighbor_count
        y_average = y_summation / neighbor_count
        return Vector(x_average - self.x, y_average - self.y)
