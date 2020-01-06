from math import radians, cos, sin, sqrt, atan2, degrees


class Vector:

    def __init__(self, x: float = 0.0, y: float = 0.0):
        self.x: float = x
        self.y: float = y

    def __add__(self, other: 'Vector') -> 'Vector':
        return Vector(self.x + other.x, self.y + other.y)

    def __truediv__(self, other: float) -> 'Vector':
        return Vector(self.x / other, self.y / other)

    def __mul__(self, other: float) -> 'Vector':
        return Vector(self.x * other, self.y * other)

    def __str__(self) -> str:
        return '[' + str(self.x) + ', ' + str(self.y) + ']'

    def get_length(self) -> float:
        return sqrt(self.x ** 2 + self.y ** 2)

    def normalize(self) -> 'Vector':
        return self / self.get_length()

    def get_degrees(self) -> float:
        return degrees(self.get_radians())

    def get_radians(self) -> float:
        return Vector.angle_reference().angle_to(self)

    def angle_to(self, other: 'Vector') -> float:
        return atan2(self.x * other.y - self.y * other.x, self.x * other.x + self.y * other.y)

    def rotate_degrees(self, angle: float) -> 'Vector':
        return self.rotate_radians(radians(angle))

    def rotate_radians(self, angle: float) -> 'Vector':
        return Vector(cos(angle) * self.x - sin(angle) * self.y, sin(angle) * self.x + cos(angle) * self.y)

    @classmethod
    def from_degrees(cls, angle: float, length: float = 1) -> 'Vector':
        return Vector.from_radians(radians(angle), length)

    @classmethod
    def from_radians(cls, angle: float, length: float = 1) -> 'Vector':
        return Vector(cos(angle) * length, sin(angle) * length)

    @classmethod
    def angle_reference(cls) -> 'Vector':
        return Vector(1.0, 0.0)
