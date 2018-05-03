import random
import Classes.Wall as w
import Classes.Brick as b
import Classes.Button as btn

import pygame

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

    def __init__(self, walls, bricks):

        # Set up the display
        self.screen = pygame.display.set_mode((1200, 750))

        # Board of game
        self.game = [[0 for col in range(15)] for row in range(15)]
        for i in range(len(self.game)):
            for j in range(len(self.game[i])):
                self.game[i][j] = 0
            print()
        self.buttons()
        self.walls(walls)
        self.bricks(bricks)

    def walls(self, walls):
        x = 450
        y = 0
        for row in self.level:
            for col in row:
                if col == "W":
                    wal = w.Wall((x, y), walls)
                    self.game[int(y/50)][int((x-450)/50)] = wal.get_wall()
                x += 50
            y += 50
            x = 450

    def bricks(self, bricks):
        print(" Z cegłami")
        x2 = 450
        y2 = 0
        # skrzynki na planszy
        for row2 in self.level:
            for col2 in row2:
                if col2 != "W":
                    if (row2 != 500 and col2 != 50):
                        rand = random.randint(1, 100)
                        if rand > 65:
                            if ((x2 == 500 and y2 == 50) or (x2 == 500 and y2 == 100) or (x2 == 550 and y2 == 50)):
                                continue
                            else:
                                brick = b.Brick((x2, y2), bricks)
                                self.game[int(y2 / 50)][int((x2 - 450) / 50)] = brick.get_brick()
                x2 += 50
            y2 += 50
            x2 = 450

    def buttons(self):
        # Create buttons
        self.exitBtn = btn.Button("Pictures\exit.png", (200, 600))
        self.menuBtn = btn.Button("Pictures\menu.png", (400, 600))

    def show_board(self):
        for i in range(len(self.game)):
            for j in range(len(self.game[i])):
                if(self.game[i][j] != 0):
                    print(self.game[i][j].x, " ", self.game[i][j].y, " ", self.game[i][j].desc, end='\n')
            print()