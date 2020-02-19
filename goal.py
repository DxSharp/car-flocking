"""This module contains functionality to represent a goal location for cars to flock to.

A goal is represented as a point in the world, with an x and y position. A goal can be
activated or deactivated. Cars will only flock towards a goal if it is active.

"""


class Goal:

    def __init__(self, x: float, y: float, active: bool):
        """Initializes a new goal object.

        Args:
            x (float): The x position of the goal.
            y (float): The y position of the goal.
            active (bool): Specifies if cars should flock to the goal or not.

        """
        self.x: float = x
        self.y: float = y
        self.active: bool = active
