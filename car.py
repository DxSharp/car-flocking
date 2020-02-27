"""This module contains functionality to represent a car in the simulation.

A car is represented by its dimensions and limitations with respect to velocity and turning radius. The distance between
the front axle and the front of the car is considered equal to the distance between the back axle and the back of the
car. In other words, the midpoint of the wheelbase is equal to the midpoint of the length of the car. The movement of
the car is based on a Simple Car kinematics model (see: http://planning.cs.uiuc.edu/node658.html).

This module contains functions to calculate the flocking forces experienced by a car. These flocking forces are then
translated into adjustment of the control parameters of a car: acceleration and steering.

"""

from typing import List, Tuple
from goal import Goal
from vector import Vector
from math import radians, tan, inf
from wall import Wall


class Car:

    def __init__(self, length: float, width: float, wheelbase: float, max_velocity: float, max_acceleration: float,
                 max_steering_angle: float, max_steering_change: float, x: float = 0, y: float = 0, angle: float = 0,
                 velocity: float = 0, steering_angle: float = 0, acceleration: float = 0, steering_change: float = 0):
        """Initializes a new car object.

        Args:
            length (float): The length of the car in meters.
            width (float): The width of the car in meters.
            wheelbase (float): The distance between the front and back axle of the car in meters.
            max_velocity (float): The maximum velocity the car can achieve in meters per second.
            max_acceleration (float): The maximum acceleration the car can achieve in meters per second squared.
            max_steering_angle (float): The maximum possible angle the wheels of the car can rotate in degrees.
            max_steering_change (float): The maximum speed with which the wheel angle of the car can change in degrees
                per second.
            x (float): The x-value of the initial position of the car in meters.
            y (float): The y-value of the initial position of the car in meters.
            angle (float): The initial angle of the car relative to the positive x-axis.
            velocity (float): The initial velocity of the car in meters per second.
            steering_angle (float): The initial angle of the wheels of the car in degrees.
            acceleration (float): The initial acceleration of the car in meters per second squared.
            steering_change (float): The initial change of wheel angle in degrees per seconds.

        """
        self.length: float = length
        self.width: float = width
        self.wheelbase: float = wheelbase

        self.x: float = x
        self.y: float = y
        self.direction: Vector = Vector.from_degrees(angle)
        self.steering_angle: float = radians(steering_angle)

        self.velocity: float = velocity
        self.steering_change: float = radians(steering_change)

        self.acceleration: float = acceleration

        self.max_velocity: float = max_velocity
        self.max_acceleration: float = max_acceleration
        self.max_steering_angle: float = radians(max_steering_angle)
        self.max_steering_change: float = radians(max_steering_change)

        self.overlapping_cars: List[Car] = []
        self.goal_reached: bool = False
        self.flocking_vector: Vector = Vector()

    def update(self, dt: float):
        """Updates position, direction, velocity and steering angle given a time step in seconds.

        Args:
            dt (float): The amount of time in seconds to progress the simulation.

        """
        x_change = self.velocity * self.direction.x
        y_change = self.velocity * self.direction.y
        angle_change = tan(self.steering_angle) * self.velocity / self.wheelbase

        self.x = self.x + x_change * dt
        self.y = self.y + y_change * dt
        self.direction = self.direction.rotate_radians(angle_change * dt)

        new_velocity = self.velocity + self.acceleration * dt
        new_steering_angle = self.steering_angle + self.steering_change * dt

        self.velocity = min(self.max_velocity, new_velocity)
        self.steering_angle = max(-self.max_steering_angle, min(new_steering_angle, self.max_steering_angle))

    def adjust_behavior(self, neighbors: List[Tuple['Car', float]], goal: Goal, rule_weights: List[float]):
        """Changes the control parameters of this car given its neighbors, its goal and the flocking rule weights.

        First, it is determined if the car has reached its goal yet. Next, the flocking forces experienced are
        calculated, of which the weighted average is taken to obtain the final flocking vector. This final vector is
        used to determine the steering change.

        Args:
            neighbors (List[Tuple[Car, float]]): A list of neighboring cars and the distance between this car and each
                respective neighboring car.
            goal (Goal): The goal that this car should steer towards.
            rule_weights (List[float]): A list with the weights of each flocking force. The respective flocking forces
                are [Separation, Alignment, Cohesion, Goal].

        """
        if goal.active:
            goal_force = self.goal_force(goal)
            if goal_force.get_length() < self.length:
                self.goal_reached = True
        else:
            goal_force = Vector(0.0, 0.0)

        if not self.goal_reached:
            for neighbor in neighbors:
                self.goal_reached = self.goal_reached or neighbor[0].goal_reached

        separation_force = self.separation(neighbors)
        alignment_force = self.alignment(neighbors)
        cohesion_force = self.cohesion(neighbors)

        self.flocking_vector = separation_force * rule_weights[0] + alignment_force * rule_weights[1] + \
            cohesion_force * rule_weights[2] + goal_force * rule_weights[3]

        steering_direction = self.direction.rotate_radians(self.steering_angle)

        if self.flocking_vector == Vector(0, 0):
            angle_dif = 0
        else:
            angle_dif = steering_direction.angle_to(self.flocking_vector)

        if angle_dif > 0:
            self.steering_change = self.max_steering_change
        elif angle_dif < 0:
            self.steering_change = -self.max_steering_change
        elif self.steering_angle > 0:
            self.steering_change = -self.max_steering_change
        else:
            self.steering_change = self.max_steering_change

    def goal_force(self, goal: Goal) -> 'Vector':
        """Determines the force this car experiences to towards the specified goal.

        Args:
            goal (Goal): The goal that this car should steer towards.

        Returns:
            Vector: A vector representing the force experienced by this car towards the goal.

        """
        return Vector(goal.x - self.x, goal.y - self.y)

    def wall_avoidance(self, walls: List[Wall], wall_radius) -> 'Vector':
        """Determines the force this car experiences to avoid given walls within the specified radius.

        TODO: Revise and incorporate into simulation.

        Args:
            walls (List[Wall]): A list of walls that the car can collide with.
            wall_radius (float): The radius around this car a wall must be in to be taken into account.

        Returns:
            Vector: A vector representing the wall avoidance force experienced by this car.

        """
        resulting_force = Vector()
        heading = self.direction.rotate_radians(self.steering_angle)
        for wall in walls:
            steering_vector = wall.perpendicular_vector(self.x, self.y)
            vector_length = steering_vector.get_length()
            if vector_length < wall_radius:
                rotation = steering_vector.angle_to(heading)
                if rotation > 0.0:
                    steering_vector = steering_vector.rotate_degrees(90)
                else:
                    steering_vector = steering_vector.rotate_degrees(-90)

                if abs(rotation) < radians(90):
                    steering_force = steering_vector.change_length(0)
                else:
                    steering_force = steering_vector.change_length(wall_radius - vector_length)

                resulting_force += steering_force

        return resulting_force

    def separation(self, neighbors: List[Tuple['Car', float]]) -> Vector:
        """Determines the separation force this car experiences given its neighbors.

        Args:
            neighbors (List[Tuple[Car, float]]): A list of neighboring cars and the distance between this car and each
                respective neighboring car.

        Returns:
            Vector: A vector representing the separation force experienced by this car.

        """
        resulting_force = Vector()
        for neighbor in neighbors:
            distance = neighbor[1]
            n = neighbor[0]
            separation_vector = Vector(self.x - n.x, self.y - n.y)
            if distance == 0:
                separation_length = inf
            else:
                separation_length = 1 / distance
            separation_force = separation_vector.change_length(separation_length)
            resulting_force += separation_force
        return resulting_force

    @staticmethod
    def alignment(neighbors: List[Tuple['Car', float]]) -> 'Vector':
        """Determines the alignment force this car experiences given its neighbors.

        Args:
            neighbors (List[Tuple[Car, float]]): A list of neighboring cars and the distance between this car and each
                respective neighboring car.

        Returns:
            Vector: A vector representing the alignment force experienced by this car.

        """
        resulting_force = Vector()
        for neighbor in neighbors:
            resulting_force += neighbor[0].direction
        return resulting_force

    def cohesion(self, neighbors: List[Tuple['Car', float]]) -> Vector:
        """Determines the cohesion force this car experiences given its neighbors.

        Args:
            neighbors (List[Tuple[Car, float]]): A list of neighboring cars and the distance between this car and each
                respective neighboring car.

        Returns:
            Vector: A vector representing the cohesion force experienced by this car.

        """
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

    def wall_collision(self, walls: List[Wall], new_x: float, new_y: float) -> bool:
        """Determines if this car will collide with a wall if moving to the specified new position.

        TODO: Revise and incorporate into simulation.

        Args:
            walls (List[Wall]): A list of walls that the car can collide with.
            new_x (float): The x-value of the new position.
            new_y (float): The y-value of the new position.

        Returns:
            bool: True if the specified movement will result in a collision, false otherwise.

        """
        for wall in walls:
            v1 = wall.perpendicular_vector(self.x, self.y)
            v2 = wall.perpendicular_vector(new_x, new_y)
            angle = v1.angle_to(v2)
            if angle != 0.0:
                return True
        return False
