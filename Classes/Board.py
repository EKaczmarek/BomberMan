import Classes.Wall as w
import Classes.Brick as b
import Classes.Button as btn
import Classes.Client as client
import pygame


class Board(object):
    level = [
            "WWWWWWWWWWWWWWW",
            "W    BBBBBBB  W",
            "WBW W W W W W W",
            "WB  B   BBB   W",
            "WBW WBW W W W W",
            "W   BBBBBBBB  W",
            "W W W W W W W W",
            "W  BB         W",
            "W W W W W W W W",
            "W BBBBBBBBBB  W",
            "W W W WBWBW W W",
            "WB  BBBBBB    W",
            "WBW W WBW W W W",
            "WBB B  B      W",
            "WWWWWWWWWWWWWWW",
        ]

    def __init__(self,):

        # Set up the display
        self.screen = pygame.display.set_mode((1200, 750), pygame.RESIZABLE)

        # Board of game
        self.game = [[0 for col in range(15)] for row in range(15)]
        for i in range(len(self.game)):
            for j in range(len(self.game[i])):
                self.game[i][j] = 0
            print()

            """cl = client.Client()
                cl.connectToSerwer('192.168.0.103')
                cl.sendMessage("GET")
                lev = cl.wait4Response()
            
                print("Dlugosc odp: ", len(lev))
                print("Poziom: ", lev)
            
                self.level = map(''.join, zip(*[iter(lev)]*15))"""

        self.buttons()
        self.walls_bricks()

    def table_dimension(self, x, y):
        return int(x/50), int((y-450)/50)

    def walls_bricks(self):
        x = 450
        y = 0
        for row in self.level:
            for col in row:
                if col == "W":
                    wal = w.Wall((x, y))
                    # x is a multiply of 50 f.ex 450, y also
                    # so it's easier to have element table[1][1] than table[50][50] etc
                    table_x, table_y = self.table_dimension(y, x)
                    self.game[table_x][table_y] = wal.get_wall()
                elif col == "B":
                        brick = b.Brick((x, y))
                        table_x, table_y = self.table_dimension(y, x)
                        self.game[table_x][table_y] = brick.get_brick()
                x += 50
            y += 50
            x = 450

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
        # self.list_to_blow = []
        xx, yy = self.table_dimension(y_bomb, x_bomb)
        print("Bomba: ", xx, " ", yy)

        x_brick_1, y_brick_1 = xx, yy + 1
        self.which_one(x_brick_1, y_brick_1)
        print("Cegla 1: ", x_brick_1, " ", y_brick_1)

        x_brick_2, y_brick_2 = xx, yy - 1
        self.which_one(x_brick_2, y_brick_2)
        print("Cegla 2: ", x_brick_2, " ", y_brick_2)

        x_brick_3, y_brick_3 = xx - 1, yy
        self.which_one(x_brick_3, y_brick_3)
        print("Cegla 3: ", x_brick_3, " ", y_brick_3)

        x_brick_4, y_brick_4 = xx + 1, yy
        self.which_one(x_brick_4, y_brick_4)
        print("Cegla 4: ", x_brick_4, " ", y_brick_4)

        self.list_to_destroy.append((xx, yy))
        print("To destroy: ", self.list_to_destroy)

        return self.list_to_destroy

    def which_one(self, x_brick, y_brick):
        # self.list_to_blow.append((x_brick, y_brick))
        if (self.game[x_brick][y_brick] != 0):
            if (self.game[x_brick][y_brick].desc == "brick"):
                print("Powinno nie byc obiektu o wpolrzednych: ", x_brick, " ", y_brick)
                self.list_to_destroy.append((x_brick, y_brick))
