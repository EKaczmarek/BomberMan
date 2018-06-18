import re
import Classes.Wall as w
import Classes.Brick as b
import Classes.Powerup as p
import Classes.Bomb as bomb
import Classes.Button as btn
import Classes.Player_object_board as Player_ob

class Game_state:
    level = []
    last_pos = ''

    def __init__(self):
        print("Inicjalizacja stanu gry")
        self.game = [[0 for col in range(15)] for row in range(15)]
        for i in range(len(self.game)):
            for j in range(len(self.game[i])):
                self.game[i][j] = 0

    # board = "WWWWWWWWWWWWWWWW    BB       WW W W WBW W W WW       B     WWBW W W W W W WW    BBB    BBWW W W W W W WBWW      BB BB  WW W W W W W W WW             WW W W W W W W WW             WW W W W W W W WW             WWWWWWWWWWWWWWWW"
    def set_board(self, board):
        self.level = map(''.join, zip(*[iter(board)]*15))
        self.walls_bricks()

    def walls_bricks(self):
        x = 450
        y = 0
        for row in self.level:
            for col in row:
                if col == "W":
                    wal = w.Wall((x, y))
                    # x is a multiply of 50 f.ex 450, y also
                    # so it's easier to have element table[1][1] than table[50][50] etc
                    # table_x, table_y - [0-15][0-15]
                    # x,y - [450-1150][0-700]
                    table_x, table_y = self.table_dimension(y, x)
                    self.game[table_x][table_y] = wal.get_wall()
                elif col == "B":
                    brick = b.Brick((x, y))
                    table_x, table_y = self.table_dimension(y, x)
                    self.game[table_x][table_y] = brick.get_brick()
                    powerUP = p.Powerup((x, y))
                x += 50
            y += 50
            x = 450

        if(self.last_pos == ''):
            self.game[1][1] = Player_ob.Player_object_board((1,1), 1)
            self.last_pos = (1,1)

        self.show_board()

    # from pixels to table dimenstion
    def table_dimension(self, x, y):
        return int(x/50), int((y-450)/50)

    def show_board(self):
        print("w show_board")
        for i in range(len(self.game)):
            for j in range(len(self.game[i])):
                if(self.game[i][j] != 0):
                    print(self.game[i][j].desc, end="\t")
                else:
                    print("empty", end="\t")
            print(end='\n')

    # position like 'P x1y2'
    def update_player_position(self, player_ip, position):

        x = int(re.search('P x(.*)y', position).group(1))
        y = int(re.search('y(.*)', position).group(1))

        # removing player from last position
        self.game[self.last_pos[0]][self.last_pos[1]] = 0

        # set current position of player
        self.game[y][x] = Player_ob.Player_object_board((x, y), "player 1")
        self.last_pos = y, x
        self.show_board()

    # bomb position 'B x1y2'
    def set_bomb(self, player_ip, position):
        print(" w set_bomb")
        x = int(re.search('B x(.*)y', position).group(1))
        y = int(re.search('y(.*)', position).group(1))

        self.game[y][x] = bomb.Bomb(x, y)
        self.show_board()
        self.count_where_blow(y,x)

    #count where is it about to blow and send list client
    def count_where_blow(self, xx, yy):
        self.list_to_destroy = []
        print(self.list_to_destroy)
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
        print(self.list_to_destroy)

    def which_one(self, x_brick, y_brick):
        if (self.game[x_brick][y_brick] != 0):
            if (self.game[x_brick][y_brick].desc == "brick"):
                self.list_to_destroy.append((x_brick, y_brick))
        else:
            self.list_to_destroy.append((x_brick, y_brick))

    def check_is_player_dead(self, address):
        ans = self.get_player_pos()
        xx, yy = self.get_bomb_pos()
        if (ans == 0):
            x,y = xx, yy
        else:
            x,y = ans[0], ans[1]

        if ((x == xx and y == yy)
            or (x == xx + 1 and y == yy)
            or (x == xx - 1 and y == yy)
            or (x == xx and y == yy + 1)
            or (x == xx and y == yy - 1)):
            print("Player", x, " ", y)
            print("Bomba 1: ", xx, " ", yy)
            self.kill_player(address)
            return True
        else:
            return False

    def kill_player(self, address):
        i, j = self.get_player_pos()
        self.game[i][j] = 0

    def get_player_pos(self):
        for i in range(len(self.game)):
            for j in range(len(self.game[i])):
                if(self.game[i][j] != 0):
                    if(self.game[i][j].desc == "player 1"):
                        return i,j
        return (self.get_bomb_pos())

    def get_bomb_pos(self):
        for i in range(len(self.game)):
            for j in range(len(self.game[i])):
                if(self.game[i][j] != 0):
                    if(self.game[i][j].desc == "BOMB"):
                        return i, j
                    # below to change
                    else:
                        return 1,1











