"""
Grid with border constraints
"""

# Project
from tile import Tile
from typing import Union

# Stdlib
from collections import namedtuple


class ColorConstraintViolationException(Exception):
    pass


class NonEmptyPositionException(Exception):
    pass


class OutOfBoundsExceptions(Exception):
    pass


class RotationConstraintViolationException(Exception):
    pass


class UnexpectedBordersException(Exception):
    pass


class Grid():

    def __init__(self, size, borders):
        # Checks
        assert(size > 0)
        self.check_borders(size, borders)

        # Allocations
        self.size = size
        self.grid = [[None] * len for len in range(2 * size - 1, 0, -2)]
        self.borders = borders
        self.missing = size * size

    def __repr__(self):
        output = ""

        for y in range(self.size - 1, -1, -1):
            output += str(self.borders[1][y])
            output += " "
            output += (" " * 4) * y
            for x in range(0, 2 * (self.size - y) - 1):
                tile = self.get_tile(x, y)
                output += str(tile) if tile is not None else " " * 3
                output += " "
            output += (" " * 4) * y
            output += str(self.borders[2][y])
            output += "\n"

        for i in range(0, self.size):
            output += " " * 3
            output += str(self.borders[0][i])
            output += " " * 4

        return output

    def get_tile(self, x: int, y: int) -> Union[None, Tile]:
        self.check_coordinates(x, y, self.size)
        return self.grid[y][x]

    def set_tile(self, tile: Union[None, Tile], x: int, y: int) -> None:
        """
        Unsafe setter.
        """
        self.check_coordinates(x, y, self.size)
        self.grid[y][x] = tile

    def add_tile(self, tile: Tile, x: int, y: int) -> None:
        """
        Safe setter.
        """
        # Check emptyness
        if self.get_tile(x, y) is not None:
            raise NonEmptyPositionException(f"A tile already exist at coordinates ({x}, {y})")

        # Check constraints
        constraints = self.get_constraints(x, y)

        if tile.rotation % 120 != constraints.rotation % 120:
            # This should never trigger
            raise RotationConstraintViolationException(f"{tile} does not respect constraint {constraints} (rotation mismatch)")

        if ((constraints.left is not None and constraints.left != tile.left) or
                (constraints.middle is not None and constraints.middle != tile.middle) or
                (constraints.right is not None and constraints.right != tile.right)):
            raise ColorConstraintViolationException(f"{tile} does not respect constraint {constraints} (color mismatch)")

        # Set tile
        self.set_tile(tile, x, y)

    def remove_tile(self, x: int, y: int) -> Tile:
        tile = self.get_tile(x, y)
        self.set_tile(None, x, y)
        return tile

    def get_constraints(self, x: int, y: int) -> Tile:
        self.check_coordinates(x, y, self.size)

        c1 = None
        c2 = None
        c3 = None
        rotation = 0 if x % 2 == 0 else 60

        if x == 0:
            c1 = self.borders[1][y]
        else:
            neighbor = self.get_tile(x - 1, y)
            if neighbor is not None:
                c1 = neighbor.right

        if y == 0 and x % 2 == 0:
            c2 = self.borders[0][x // 2]
        else:
            if x % 2 == 0:
                neighbor = self.get_tile(x + 1, y - 1)
            else:
                neighbor = self.get_tile(x - 1, y + 1)

            if neighbor is not None:
                c2 = neighbor.middle

        if x == 2 * (self.size - y - 1):
            c3 = self.borders[2][y]
        else:
            neighbor = self.get_tile(x + 1, y)
            if neighbor is not None:
                c3 = neighbor.left

        if rotation == 60:
            c2, c3 = c3, c2

        return Tile(c1, c2, c3, rotation)

    @property
    def solved(self) -> bool:
        return self.missing == 0

    @staticmethod
    def check_borders(size, borders) -> bool:
        if len(borders) != 3:
            raise UnexpectedBordersException(f"Unexpected number of borders (expected: 3, received: {len(borders)}")

        for border in borders:
            if len(border) != size:
                raise UnexpectedBordersException(f"Unexpected border length in {border} (expected: {size}, received: {len(border)}")

    @staticmethod
    def check_coordinates(x, y, size):
        if x < 0 or y < 0 or y >= size or x > 2 * (size - y - 1):
            raise OutOfBoundsExceptions(f"Out of bounds coordinates ({x}, {y})")


Position = namedtuple('Position', ['x', 'y'])