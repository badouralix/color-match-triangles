"""
Triangle tiles.
"""

# Project
from dot import Dot

# Stdlib
from typing import Optional


class UnauthorizedRotationException(Exception):
    pass


class Tile():

    def __init__(self, left: Optional[Dot], middle: Optional[Dot], right: Optional[Dot], rotation: int = 0) -> None:
        self.left = left
        self.middle = middle
        self.right = right
        self.rotation = rotation

    def __repr__(self):
        return f"Tile({self.left} {self.middle} {self.right})"

    def __str__(self):
        output = ""

        for c in [self.left, self.middle, self.right]:
            if c is None:
                output += " "
            else:
                output += str(c)

        return output

    def rotate(self, angle: int) -> 'Tile':
        # Sanitize input
        angle = angle % 360

        if angle % 60 != 0:
            raise UnauthorizedRotationException(f"Rotation must be a multiple of 60° (passed: {angle}°)")

        # Save current dots
        left = self.left
        middle = self.middle
        right = self.right

        # Perform dot permutation
        if angle == 120 or angle == 180:
            self.left = right
        elif angle == 240 or angle == 300:
            self.left = middle

        if angle == 60 or angle == 240:
            self.middle = right
        elif angle == 120 or angle == 300:
            self.middle = left

        if angle == 60 or angle == 120:
            self.right = middle
        elif angle == 180 or angle == 240:
            self.right = left

        # Save new tile rotation
        self.rotation = (self.rotation + angle) % 360

        # Return tile
        return self
