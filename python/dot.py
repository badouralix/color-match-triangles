"""
Colorful dots.
"""


class Dot():

    def __init__(self, s: str) -> None:
        self.s = s

    def __str__(self):
        return self.s


BLACK = Dot("○")
BLUE = Dot("\x1b[34m●\x1b[0m")
GREEN = Dot("\x1b[32m●\x1b[0m")
ORANGE = Dot("\x1b[33m●\x1b[0m")
RED = Dot("\x1b[31m●\x1b[0m")
WHITE = Dot("●")
