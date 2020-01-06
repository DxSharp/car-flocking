from vector import Vector


class Wall:

    def __init__(self, x1: float, y1: float, x2: float, y2: float):
        self.x1: float = x1
        self.y1: float = y1
        self.x2: float = x2
        self.y2: float = y2

    def perpendicular_vector(self, x: float, y: float) -> Vector:
        a_wall = (self.y2 - self.y1) / (self.x2 - self.x1)
        b_wall = self.y1 - a_wall * self.x1

        a_perpendicular = -1.0 / a_wall
        b_perpendicular = y - a_perpendicular * x

        x_intersection = (b_perpendicular - b_wall) / (a_wall - a_perpendicular)
        y_intersection = a_wall * x_intersection + b_wall
        return Vector(x - x_intersection, y - y_intersection)

