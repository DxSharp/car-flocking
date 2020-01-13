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

    def update(self, dt: float, walls: List[Wall]):
        x_change = self.velocity * self.direction.x
        y_change = self.velocity * self.direction.y
        angle_change = tan(self.steering_angle) * self.velocity / self.wheelbase

        new_x = self.x + x_change * dt
        new_y = self.y + y_change * dt

        will_collide = self.wall_collisions(walls, new_x, new_y)
        if not will_collide:
            self.x = new_x
            self.y = new_y


        self.direction = self.direction.rotate_radians(angle_change * dt)

        new_velocity = self.velocity + self.acceleration * dt
        new_steering_angle = self.steering_angle + self.steering_change * dt

        self.velocity = min(self.max_velocity, new_velocity)
        self.steering_angle = max(-self.max_steering_angle, min(new_steering_angle, self.max_steering_angle))

    def adjust_behavior(self, neighbors: List[Tuple['Car', float]], walls: List[Wall],
                        wall_radius: float, separation_radius: float):
        wall_force = self.wall_avoidance(walls, wall_radius)
        separation_force = self.separation(neighbors, separation_radius)
        alignment_force = self.alignment(neighbors)
        cohesion_force = self.cohesion(neighbors)
        self.vector = cohesion_force * 0.5 + alignment_force * 4 + separation_force * 1 + wall_force * 1

        steering_direction = self.direction.rotate_radians(self.steering_angle)

        angle_dif = steering_direction.angle_to(self.vector)

        if angle_dif > 0:
            self.steering_change = self.max_steering_change
        elif angle_dif < 0:
            self.steering_change = -self.max_steering_change
        elif self.steering_angle > 0:
            self.steering_change = -self.max_steering_change
        else:
            self.steering_change = self.max_steering_change

    def wall_avoidance(self, walls: List[Wall], wall_radius) -> 'Vector':
        resulting_force = Vector()
        for wall in walls:
            steering_vector = wall.perpendicular_vector(self.x, self.y)
            vector_length = steering_vector.get_length()
            if vector_length < wall_radius:
                steering_force = steering_vector.change_length(wall_radius - vector_length)
                resulting_force += steering_force
        return resulting_force

    def separation(self, neighbors: List[Tuple['Car', float]], separation_radius: float) -> Vector:
        resulting_force = Vector()
        for neighbor in neighbors:
            distance = neighbor[1]
            if distance < separation_radius:
                n = neighbor[0]
                separation_vector = Vector(self.x - n.x, self.y - n.y)
                separation_force = separation_vector.change_length(separation_radius - distance)
                resulting_force += separation_force
        return resulting_force

    @staticmethod
    def alignment(neighbors: List[Tuple['Car', float]]) -> 'Vector':
        resulting_force = Vector()
        for neighbor in neighbors:
            resulting_force += neighbor[0].direction
        return resulting_force

    def cohesion(self, neighbors: List[Tuple['Car', float]]) -> Vector:
        x_summation = 0
        y_summation = 0
        for neighbor in neighbors:
            n = neighbor[0]
            x_summation += n.x
            y_summation += n.y
        neighbor_count = len(neighbors)
        x_average = x_summation / neighbor_count
        y_average = y_summation / neighbor_count
        return Vector(x_average - self.x, y_average - self.y)

    def wall_collisions(self, walls: List[Wall], new_x: float, new_y: float) -> bool:
        for wall in walls:
            v1 = wall.perpendicular_vector(self.x, self.y)
            v2 = wall.perpendicular_vector(new_x, new_y)
            angle = v1.angle_to(v2)
            if angle != 0.0:
                return True
        return False
