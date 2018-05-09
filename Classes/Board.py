import random
import Classes.Wall as w
import Classes.Brick as b
import Classes.Button as btn

import pygame

class Board(object):
    level = [
        "WWWWWWWWWWWWWWW",
        "W    BB       W",
        "W W W WBW W W W",
        "W       B     W",
        "WBW W W W W W W",
        "W    BBB    BBW",
        "W W W W W W WBW",
        "W      BB BB  W",
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

    def table_dimension(self, x, y):
        return int(x/50), int((y-450)/50)

    def walls(self, walls):
        x = 450
        y = 0
        for row in self.level:
            for col in row:
                if col == "W":
                    wal = w.Wall((x, y), walls)
                    # x is a multiply of 50 f.ex 450, y also
                    # so it's easier to have element table[1][1] than table[50][50] etc
                    table_x, table_y = self.table_dimension(y, x)
                    self.game[table_x][table_y] = wal.get_wall()
                x += 50
            y += 50
            x = 450

    def bricks(self, bricks):
        print(" Z cegłami")
        x2 = 450
        y2 = 0
        # Bricks on the board
        for row2 in self.level:
            for col2 in row2:
                if col2 == "B":
                        brick = b.Brick((x2, y2), bricks)
                        table_x, table_y = self.table_dimension(y2, x2)
                        self.game[table_x][table_y] = brick.get_brick()
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

    def count(self, x_bomb, y_bomb):

        self.list_to_destroy = []
        xx = int(y_bomb / 50)
        yy = int((x_bomb - 450) / 50)

        x_brick_1, y_brick_1 = xx, yy + 1
        self.which_one(x_brick_1, y_brick_1)

        x_brick_2, y_brick_2 = xx, yy - 1
        self.which_one(x_brick_2, y_brick_2)

        x_brick_3, y_brick_3 = xx - 1, yy
        self.which_one(x_brick_3, y_brick_3)

        x_brick_4, y_brick_4 = xx + 1, yy
        self.which_one(x_brick_4, y_brick_4)

        self.list_to_destroy.append((xx, yy))

        return self.list_to_destroy

    def which_one(self, x_brick, y_brick):
        if (self.game[x_brick][y_brick] != 0):
            if (self.game[x_brick][y_brick].desc == "brick"):
                print("Powinno nie byc obiektu o wpolrzednych: ", x_brick, " ", y_brick)
                self.list_to_destroy.append((x_brick, y_brick))



