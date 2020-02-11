"""This module contains functionality to represent a wall that cars should steer away from.

A wall is represented as a line in the world. It is represented by two pairs of x and y
positions, one for each line end. A vector perpendicular to the wall towards a specified
point can be determined. This vector can be used to determine the steering force from the
wall.

"""

from vector import Vector


class Wall:

    def __init__(self, x1: float, y1: float, x2: float, y2: float):
        """Initializes a new wall object

        Args:
            x1 (float): The x position of the first line end point.
            y1 (float): The y position of the first line end point.
            x2 (float): The x position of the second line end point.
            y2 (float): The y position of the second line end point.

        """
        self.x1: float = x1
        self.y1: float = y1
        self.x2: float = x2
        self.y2: float = y2

    def perpendicular_vector(self, x: float, y: float) -> Vector:
        """Determines a vector perpendicular to the wall towards the point specified by the arguments.

        Args:
            x (float): The x position of the vector head.
            y (float): The y position of the vector head.

        Returns:
            Vector: The perpendicular vector as described, or a zero vector if this vector does not exist.

        """
        x_dif = self.x2 - self.x1
        y_dif = self.y2 - self.y1
        if x_dif == 0:
            x_intersection = self.x1
            y_intersection = y
        elif y_dif == 0:
            x_intersection = x
            y_intersection = self.y1
        else:
            a_wall = y_dif / x_dif
            b_wall = self.y1 - a_wall * self.x1

            a_perpendicular = -1.0 / a_wall
            b_perpendicular = y - a_perpendicular * x

            x_intersection = (b_perpendicular - b_wall) / (a_wall - a_perpendicular)
            y_intersection = a_wall * x_intersection + b_wall

        if self.x2 > self.x1 and (x_intersection > self.x2 or x_intersection < self.x1):
            return Vector(0.0, 0.0)
        elif self.x1 > self.x2 and (x_intersection > self.x1 or x_intersection < self.x2):
            return Vector(0.0, 0.0)
        if self.y2 > self.y1 and (y_intersection > self.y2 or y_intersection < self.y1):
            return Vector(0.0, 0.0)
        elif self.y1 > self.y2 and (y_intersection > self.y1 or y_intersection < self.y2):
            return Vector(0.0, 0.0)
        else:
            return Vector(x - x_intersection, y - y_intersection)

