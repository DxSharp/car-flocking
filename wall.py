from vector import Vector


class Wall:

    def __init__(self, x1: float, y1: float, x2: float, y2: float):
        self.x1: float = x1
        self.y1: float = y1
        self.x2: float = x2
        self.y2: float = y2

    def perpendicular_vector(self, x: float, y: float) -> Vector:
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

