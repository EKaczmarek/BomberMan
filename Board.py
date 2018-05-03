from main import Brick
from main import Wall
import random

class Board(object):
    level = [
        "WWWWWWWWWWWWWWW",
        "W             W",
        "W W W W W W W W",
        "W             W",
        "W W W W W W W W",
        "W             W",
        "W W W W W W W W",
        "W             W",
        "W W W W W W W W",
        "W             W",
        "W W W W W W W W",
        "W             W",
        "W W W W W W W W",
        "W             W",
        "WWWWWWWWWWWWWWW",
    ]

    def __init__(self):
        x = 450
        y = 0
        for row in self.level:
            for col in row:
                if col == "W":
                    Wall((x, y))
                x += 50
            y += 50
            x = 450
        x2 = 450
        y2 = 0

        for row2 in self.level:
            for col2 in row2:
                if col2 != "W":
                    if (row2 != 500 and col2 != 50):
                        rand = random.randint(1, 100)
                        if rand > 65:
                            Brick((x2, y2))
                x2 += 50
            y2 += 50
            x2 = 450