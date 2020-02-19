"""This module contains functionality for vector calculus.

A vector object initialized with this module is always considered to originate from the origin (0, 0),
which is the tail of the vector. The initialisation arguments correspond to the position of the head
of the vector. For the default vector, the position of the head is also the origin, which corresponds
to the zero vector.

"""

from math import radians, cos, sin, sqrt, atan2, degrees


class Vector:

    def __init__(self, x: float = 0.0, y: float = 0.0):
        """Initializes a new vector object.

        Args:
            x (float): The x position of the head of the vector.
            y (float): The y position of the head of the vector.

        """
        self.x: float = x
        self.y: float = y

    def __add__(self, other: 'Vector') -> 'Vector':
        """Adds another vector to this vector.

        Args:
            other (Vector): The vector to add to this vector.

        Returns:
            Vector: A new vector with the head in the position of the summed vectors.

        """
        return Vector(self.x + other.x, self.y + other.y)

    def __truediv__(self, other: float) -> 'Vector':
        """Reduces the length of this vector through division by the specified float.

        Args:
            other (float): The denominator to divide the length by.

        Returns:
            Vector: A new vector with reduced length.

        """
        return Vector(self.x / other, self.y / other)

    def __mul__(self, other: float) -> 'Vector':
        """Increases the length of this vector through multiplication by the specified float.

        Args:
            other (float): The multiplier to multiply the length with.

        Returns:
            Vector: A new vector with increased length.

        """
        return Vector(self.x * other, self.y * other)

    def __eq__(self, other: 'Vector') -> bool:
        """Compares this vector to another vector by comparing the x and y positions.

        Args:
            other (Vector): The vector to compare with.

        Returns:
            bool: True if the vectors are equal, false otherwise.

        """
        return self.x == other.x and self.y == other.y

    def __str__(self) -> str:
        """Creates a string representation of this vector.

        Returns:
            str: A string representation of this vector.

        """
        return '[' + str(self.x) + ', ' + str(self.y) + ']'

    def get_length(self) -> float:
        """Calculates the length of this vector.

        Returns:
            float: The length of this vector.

        """
        return sqrt(self.x ** 2 + self.y ** 2)

    def normalize(self) -> 'Vector':
        """Normalizes this vector, setting its length to 1.

        Returns:
            Vector: A new vector with length 1 in the same direction as this vector.

        """
        return self / self.get_length()

    def get_degrees(self) -> float:
        """Calculates the shortest angle in degrees between the positive x-axis and this vector.

        Note that the shortest angle can be either clockwise or counterclockwise relative to the positive x-axis. If the
        shortest angle is obtained by counterclockwise rotation from the positive x-axis to this vector, the resulting
        angle is positive. In case of clockwise rotation, the angle is negative.

        Returns:
            float: The shortest angle in degrees between the positive x-axis and this vector.

        """
        return degrees(self.get_radians())

    def get_radians(self) -> float:
        """Calculates the shortest angle in radians between the positive x-axis and this vector.

        Note that the shortest angle can be either clockwise or counterclockwise relative to the positive x-axis. If the
        shortest angle is obtained by counterclockwise rotation from the positive x-axis to this vector, the resulting
        angle is positive. In case of clockwise rotation, the angle is negative.

        Returns:
            float: The shortest angle in radians between the positive x-axis and this vector.

        """
        return Vector.angle_reference().angle_to(self)

    def change_length(self, new_length: float) -> 'Vector':
        """Creates a new vector with the same direction as this vector, with the specified length.

        Args:
            new_length (float): The length of the new vector.

        Returns:
            Vector: A vector with length as specified in the same direction as this vector.

        """
        length = self.get_length()
        if length == 0.0:
            return Vector(self.x, self.y)
        else:
            return self * new_length / self.get_length()

    def angle_to(self, other: 'Vector') -> float:
        """Calculates the shortest angle in radians between this vector and the other vector given.

        Note that the shortest angle can be either clockwise or counterclockwise relative to this vector. If the
        shortest angle is obtained by counterclockwise rotation from this vector to the other vector, the resulting
        angle is positive. In case of clockwise rotation, the angle is negative.

        Args:
            other (Vector): The vector the calculate the angle to.

        Returns:
            float: The shortest angle in radians between this vector and the other vector given.

        """
        return atan2(self.x * other.y - self.y * other.x, self.x * other.x + self.y * other.y)

    def rotate_degrees(self, angle: float) -> 'Vector':
        """Creates a new vector with the same length as this vector, rotated by the given angle in degrees.

        If the specified angle is positive, rotation will be counterclockwise. In case of a negative angle, rotation
        will be clockwise.

        Args:
            angle (float): The angle in degrees to rotate this vector.

        Returns:
            Vector: A vector with the same length as this vector, rotated by the given angle in degrees.

        """
        return self.rotate_radians(radians(angle))

    def rotate_radians(self, angle: float) -> 'Vector':
        """Creates a new vector with the same length as this vector, rotated by the given angle in radians.

        If the specified angle is positive, rotation will be counterclockwise. In case of a negative angle, rotation
        will be clockwise.

        Args:
            angle (float): The angle in radians to rotate this vector.

        Returns:
            Vector: A vector with the same length as this vector, rotated by the given angle in radians.

        """
        return Vector(cos(angle) * self.x - sin(angle) * self.y, sin(angle) * self.x + cos(angle) * self.y)

    @classmethod
    def from_degrees(cls, angle: float, length: float = 1) -> 'Vector':
        """Creates a new vector with the given length and angle in degrees relative to the positive x-axis.

        A positive angle corresponds to counterclockwise rotation relative to the positive x-axis. In case of a negative
        angle, the relative rotation is clockwise.

        Args:
            angle (float): The angle in degrees relative to the positive x-axis of the new vector.
            length (float):  The length of the new vector.

        Returns:
            Vector: A vector with angle in degrees and length as specified.

        """
        return Vector.from_radians(radians(angle), length)

    @classmethod
    def from_radians(cls, angle: float, length: float = 1) -> 'Vector':
        """Creates a new vector with the given length and angle in radians relative to the positive x-axis.

        A positive angle corresponds to counterclockwise rotation relative to the positive x-axis. In case of a negative
        angle, the relative rotation is clockwise.

        Args:
            angle (float): The angle in radians relative to the positive x-axis of the new vector.
            length (float):  The length of the new vector.

        Returns:
            Vector: A vector with angle in radians and length as specified.

        """
        return Vector(cos(angle) * length, sin(angle) * length)

    @classmethod
    def angle_reference(cls) -> 'Vector':
        """Creates a new vector corresponding to the positive x-axis, used as reference for angles.

        Returns:
            Vector: A vector corresponding to the positive x-axis.

        """
        return Vector(1.0, 0.0)
