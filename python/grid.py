"""
Grid with border constraints
"""

# Project
from dot import Dot
from tile import Tile
from typing import List, Optional

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

    def __init__(self, size: int, borders: List[List[Dot]]) -> None:
        # Checks
        assert(size > 0)
        self.check_borders(size, borders)

        # Allocations
        self.size = size
        self.grid: List[List[Optional[Tile]]] = [[None] * len for len in range(2 * size - 1, 0, -2)]
        self.borders = borders

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

    @property
    def missing(self) -> int:
        return sum(line.count(None) for line in self.grid)

    @property
    def solved(self) -> bool:
        return self.missing == 0

    def get_tile(self, x: int, y: int) -> Optional[Tile]:
        self.check_coordinates(x, y, self.size)
        return self.grid[y][x]

    def set_tile(self, tile: Optional[Tile], x: int, y: int) -> None:
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

    def remove_tile(self, x: int, y: int) -> Optional[Tile]:
        tile = self.get_tile(x, y)
        self.set_tile(None, x, y)
        return tile

    def get_constraints(self, x: int, y: int) -> Tile:
        self.check_coordinates(x, y, self.size)

        left = None
        middle = None
        right = None
        rotation = 0 if x % 2 == 0 else 180

        if x == 0:
            left = self.borders[1][y]
        else:
            neighbor = self.get_tile(x - 1, y)
            if neighbor is not None:
                left = neighbor.right

        if y == 0 and x % 2 == 0:
            middle = self.borders[0][x // 2]
        else:
            if x % 2 == 0:
                neighbor = self.get_tile(x + 1, y - 1)
            else:
                neighbor = self.get_tile(x - 1, y + 1)

            if neighbor is not None:
                middle = neighbor.middle

        if x == 2 * (self.size - y - 1):
            right = self.borders[2][y]
        else:
            neighbor = self.get_tile(x + 1, y)
            if neighbor is not None:
                right = neighbor.left

        return Tile(left, middle, right, rotation)

    @staticmethod
    def check_borders(size, borders: List[List[Dot]]):
        if len(borders) != 3:
            raise UnexpectedBordersException(f"Unexpected number of borders (expected: 3, received: {len(borders)}")

        for border in borders:
            if len(border) != size:
                raise UnexpectedBordersException(f"Unexpected border length in {border} (expected: {size}, received: {len(border)}")

    @staticmethod
    def check_coordinates(x: int, y: int, size: int):
        if x < 0 or y < 0 or y >= size or x > 2 * (size - y - 1):
            raise OutOfBoundsExceptions(f"Out of bounds coordinates ({x}, {y})")


Position = namedtuple('Position', ['x', 'y'])
