"""
Triangle tiles.
"""


class UnauthorizedRotationException(Exception):
    pass


class Tile():

    def __init__(self, c1, c2, c3, rotation=0):
        self.c1 = c1
        self.c2 = c2
        self.c3 = c3
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

    @property
    def left(self):
        if self.rotation == 0 or self.rotation == 60:
            return self.c1

        if self.rotation == 240 or self.rotation == 300:
            return self.c2

        if self.rotation == 120 or self.rotation == 180:
            return self.c3

    @property
    def middle(self):
        if self.rotation == 120 or self.rotation == 300:
            return self.c1

        if self.rotation == 0 or self.rotation == 180:
            return self.c2

        if self.rotation == 60 or self.rotation == 240:
            return self.c3

    @property
    def right(self):
        if self.rotation == 180 or self.rotation == 240:
            return self.c1

        if self.rotation == 60 or self.rotation == 120:
            return self.c2

        if self.rotation == 0 or self.rotation == 300:
            return self.c3

    def rotate(self, angle: int) -> 'Tile':
        if angle % 60 != 0:
            raise UnauthorizedRotationException(f"Rotation must be a multiple of 60° (passed: {angle}°)")

        self.rotation = (self.rotation + angle) % 360

        return self
