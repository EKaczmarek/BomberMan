import re
import Classes.Wall as w
import Classes.Brick as b
import Classes.Powerup as p
import Classes.Bomb as bomb
import Classes.Button as btn
import Classes.Player_object_board as Player_ob
import json
from PyQt5 import QtCore
import time
import pygame
class Game_state(QtCore.QObject):

    bomb_must_blow = QtCore.pyqtSignal(bool, int, int)

    level = []
    last_pos = ''
    number_players = 0

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
            self.last_pos = (1, 1)

    # from pixels to table dimenstion
    def table_dimension(self, x, y):
        return int(x/50), int((y-450)/50)

    def show_board(self):
        print("~~~~~~~~~~~~~~~~~~~~~~~~~~Ćala plansza~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~")
        for i in range(len(self.game)):
            for j in range(len(self.game[i])):
                if(self.game[i][j] != 0):
                    print(self.game[i][j].desc, end="\t")
                else:
                    print("empty", end="\t")
            print(end='\n')

    def find_last_position(self, player_id):

        for i in range(len(self.game)):
            for j in range(len(self.game[i])):
                if(self.game[i][j] != 0):
                    player_desc = "player " + str(player_id)
                    if(self.game[i][j].desc == player_desc):
                        print(self.game[i][j].desc == player_desc)
                        return j, i

        if player_id == 0:
            return 1, 1
        elif player_id == 1:
            return 13, 1
        elif player_id == 2:
            return 1, 13
        elif player_id == 3:
            return 13, 13

    # position nowa pozycja garcza w tablicy
    def update_player_position(self, player_id, position):

        x = position[0]
        y = position[1]
        print("position ", position)

        # removing player from last position
        # self.game[self.last_pos[0]][self.last_pos[1]] = 0
        self.last_pos = self.find_last_position(player_id)

        self.game[self.last_pos[1]][self.last_pos[0]] = 0

        # set current position of player
        player_desc = "player " + str(player_id)
        print(str(player_desc) + " pozycja " + str(x) + " " + str(y))
        self.game[y][x] = Player_ob.Player_object_board(self.table_to_pixels(x, y), player_desc)
        self.last_pos = (y, x)

        #self.show_board()

    def table_to_pixels(self, x, y):
        return int(x * 50), int((y * 50) + 450)

    # bomb position 'B x1y2'
    def set_bomb(self, addr, position, player_id):
        print(" w set_bomb")
        print("position", position)
        print("typ: ", type(position))
        position = json.loads(position)

        x = position["ME"]["x"]
        y = position["ME"]["y"]

        i, j = self.table_to_pixels(x, y)

        print("table dimension " + str(x) + " " + str(y))
        description_bomb = "player " + str(player_id)
        self.game[y][x] = bomb.Bomb(i, j, description_bomb)

        self.handle_bombs(y, x)
        return x, y


    def check_is_any_player_dead(self):
        list_of_dead = []
        for i in self.list_to_destroy:
            for j in range(0, self.number_players):
                x, y = self.get_player_pos(j)
                if i[0] == y and i[1] == x:
                    list_of_dead.append(j)
        return list_of_dead

    def handle_bombs(self, x, y):
        time.sleep(1.5)
        self.count_where_blow(x, y)
        self.
        print("self.list_to_destroy ", self.list_to_destroy)
        ans = self.check_is_any_player_dead()

        if ans != []:
            print("Zginal graczz o numerze: ", ans)
        else:
            print("Nikt nie zginal")

        """seconds = (self.now - bomba.start_timer) / 1000
        print(" czasss ", pygame.time.get_ticks() / 1000)
        print(" lol czas ", bomba.start_timer / 1000)

        if seconds >= 1.5:
            print(" JESST!! ", seconds)
            #ans = self.check_is_any_player_dead()
            self.count_where_blow(x, y)
            print("self.list_to_destroy ", self.list_to_destroy)
            for i in self.board.list_to_destroy:
                for x in range(8):
                    posx, posy = self.board.table_to_pixels(int(i[0]), int(i[1]))
                    self.board.screen.blit(self.images[x], (posy, posx))
                    pygame.display.flip()
                self.board.game[i[0]][i[1]] = 0
            if (ans):
                print("Gracz zginął")
            else:
                print("Nikt nie zginal")
            return True
        return False"""

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

    def get_player_pos(self, player_id):
        a, b = '', ''
        for i in range(len(self.game)):
            for j in range(len(self.game[i])):
                if self.game[i][j] != 0:
                    if self.game[i][j].desc == ("player " + str(player_id)):
                        return j, i
                    elif self.game[i][j].desc == "bomb":
                        if self.game[i][j].whose_bomb == ("player " + str(player_id)):
                            a, b = j, i
        return a, b

    def find_new_player_position(self, last_pos, dx, dy):
        x, y = last_pos[0] + dx, last_pos[1] + dy

        if self.game[y][x] == 0:
            return x, y
        else:
            return last_pos

    def get_bomb_pos(self):
        for i in range(len(self.game)):
            for j in range(len(self.game[i])):
                if(self.game[i][j] != 0):
                    if(self.game[i][j].desc == "BOMB"):
                        return i, j
                    # below to change
                    else:
                        return 1,1











