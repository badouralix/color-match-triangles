#!/usr/bin/env python3

# Project
from grid import ColorConstraintViolationException, Grid, Position
from tile import Tile

import dot

# Stdlib
from collections import defaultdict
from random import shuffle, randint
from typing import Dict, Set

# Constants
GRID_SIZE = 4


class NoNextPositionException(Exception):
    pass


class NonSolvablePathException(Exception):
    pass


def next_position(pos: Position, size: int = GRID_SIZE) -> Position:
    if pos.y == size - 1:
        raise NoNextPositionException(f"No valid position after ({pos.x}, {pos.y})")

    if pos.y % 2 == 0:
        if pos.x == 2 * (size - pos.y - 1):
            return Position(x=2 * (size - pos.y - 2), y=pos.y + 1)
        else:
            return Position(x=pos.x + 1, y=pos.y)
    else:
        if pos.x == 0:
            return Position(x=0, y=pos.y + 1)
        else:
            return Position(x=pos.x - 1, y=pos.y)


def next_tile(remaining_tiles: Set[Tile], tile_lookup: Dict[int, Set[Tile]], constraints: Tile) -> Tile:
    """
    Generator of potentially valid tiles.
    """
    potential_tiles = remaining_tiles

    for c in [constraints.left, constraints.middle, constraints.right]:
        if c is not None:
            potential_tiles = potential_tiles & tile_lookup[c]

    # Try to randomize a bit in order to find new solutions
    potential_tiles = list(potential_tiles)
    shuffle(potential_tiles)

    for tile in potential_tiles:
        yield tile.rotate(angle=randint(0, 5) * 60)


def rec_solve(pos: Position, grid: Grid, remaining_tiles: Set[Tile], tile_lookup: Dict[int, Set[Tile]]) -> bool:
    """
    Deterministic backtracking.
    """
    for tile in next_tile(remaining_tiles, tile_lookup, grid.get_constraints(x=pos.x, y=pos.y)):
        remaining_tiles.remove(tile)

        if (pos.x % 2 == 0 and tile.rotation % 120 != 0) or (pos.x % 2 == 1 and tile.rotation % 120 != 60):
            tile.rotate(angle=60)

        for _ in range(0, 3):
            try:
                grid.add_tile(tile, x=pos.x, y=pos.y)
                return rec_solve(next_position(pos), grid, remaining_tiles, tile_lookup)
            except ColorConstraintViolationException:
                tile.rotate(angle=120)
                continue
            except NoNextPositionException:
                # Happens after the new tile was successfully added to the grid at the current position
                return grid.solved
            except NonSolvablePathException:
                grid.remove_tile(x=pos.x, y=pos.y)
                tile.rotate(angle=120)
                continue

        grid.remove_tile(x=pos.x, y=pos.y)
        remaining_tiles.add(tile)

    # At this point, we tried all potential tiles, and none of them fitted
    tile = grid.remove_tile(x=pos.x, y=pos.y)
    if tile is not None:
        remaining_tiles.add(tile)

    raise NonSolvablePathException(f"No solution found at ({pos.x}, {pos.y}) in the current branch")


def main():
    # Init tiles
    tiles = set()
    tiles.add(Tile(dot.GREEN, dot.BLACK, dot.BLACK))
    tiles.add(Tile(dot.WHITE, dot.BLACK, dot.BLUE))
    tiles.add(Tile(dot.WHITE, dot.BLACK, dot.BLUE))
    tiles.add(Tile(dot.WHITE, dot.BLUE, dot.BLUE))
    tiles.add(Tile(dot.BLUE, dot.BLACK, dot.ORANGE))
    tiles.add(Tile(dot.BLACK, dot.RED, dot.GREEN))
    tiles.add(Tile(dot.RED, dot.ORANGE, dot.GREEN))
    tiles.add(Tile(dot.BLUE, dot.WHITE, dot.WHITE))
    tiles.add(Tile(dot.RED, dot.BLACK, dot.GREEN))
    tiles.add(Tile(dot.RED, dot.GREEN, dot.BLACK))
    tiles.add(Tile(dot.GREEN, dot.RED, dot.WHITE))
    tiles.add(Tile(dot.WHITE, dot.ORANGE, dot.GREEN))
    tiles.add(Tile(dot.ORANGE, dot.WHITE, dot.RED))
    tiles.add(Tile(dot.GREEN, dot.WHITE, dot.ORANGE))
    tiles.add(Tile(dot.BLACK, dot.GREEN, dot.ORANGE))
    tiles.add(Tile(dot.BLUE, dot.GREEN, dot.ORANGE))
    assert(len(tiles) == GRID_SIZE * GRID_SIZE)

    # Init grid
    grid = Grid(size=GRID_SIZE, borders=[
        [dot.WHITE, dot.RED, dot.WHITE, dot.ORANGE],
        [dot.BLUE, dot.RED, dot.GREEN, dot.BLACK],
        [dot.GREEN, dot.GREEN, dot.WHITE, dot.GREEN],
    ])

    # Build a fast lookup table
    tile_lookup = defaultdict(set)
    for tile in tiles:
        for c in [tile.left, tile.middle, tile.right]:
            tile_lookup[c].add(tile)

    # Start resolution
    rec_solve(Position(x=0, y=0), grid, tiles, tile_lookup)

    # Print solution
    print(grid)


if __name__ == "__main__":
    main()
