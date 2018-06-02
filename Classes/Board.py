import pygame
import Classes.Wall as w
import Classes.Brick as b
import Classes.Powerup as p
import Classes.Button as btn
import Classes.Client as client


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
        pygame.mixer.music.load(r"Classes/Music/music.wav")

        # Board of game
        self.powerups_array = [[0 for columns in range(15)] for rows in range(15)]
        for i in range(len(self.powerups_array)):
            for j in range(len(self.powerups_array[i])):
                self.powerups_array[i][j] = 0

        self.game = [[0 for col in range(15)] for row in range(15)]
        for i in range(len(self.game)):
            for j in range(len(self.game[i])):
                self.game[i][j] = 0
            print()

        self.cl = client.Client()
        self.cl.connectToSerwer('192.168.0.101')
        self.player_pos, self.level = self.cl.get_board_player_pos()
        print("Pos" + self.player_pos + " self.level")


        self.buttons()
        self.walls_bricks()

    def table_dimension(self, x, y):
        return int(x/50), int((y-450)/50)

    def table_to_pixels(self, x, y):
        return int(x*50), int((y*50)+450)

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
                        powerUP = p.Powerup((x, y))
                        table_x, table_y = self.table_dimension(y, x)
                        self.game[table_x][table_y] = brick.get_brick()
                        # rand = random.randint(0, 100)
                        # if (rand > 0):

                        # table_x, table_y = self.table_dimension(y, x)
                        self.powerups_array[table_x][table_y] = powerUP.get_powerup()
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
