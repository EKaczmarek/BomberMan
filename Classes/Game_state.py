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
import random
from Classes.Powerup import Powerup

class Game_state(QtCore.QObject):

    bomb_must_blow = QtCore.pyqtSignal(bool, int, int)

    level = []
    last_pos = ''
    number_players = 0

    def __init__(self):
        # print("Inicjalizacja stanu gry")
        self.game = [[0 for col in range(15)] for row in range(15)]
        for i in range(len(self.game)):
            for j in range(len(self.game[i])):
                self.game[i][j] = 0

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

                elif col == "S" or col == "N" or col == "R":
                    powerup = Powerup((x, y), col)
                    table_x, table_y = self.table_dimension(y, x)
                    self.game[table_x][table_y] = powerup.get_powerup()

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
                if self.game[i][j] != 0:
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
                        # print(self.game[i][j].desc == player_desc)
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
        # print("position ", position)

        # removing player from last position
        # self.game[self.last_pos[0]][self.last_pos[1]] = 0
        self.last_pos = self.find_last_position(player_id)

        self.game[self.last_pos[1]][self.last_pos[0]] = 0

        # set current position of player
        player_desc = "player " + str(player_id)
        # print(str(player_desc) + " pozycja " + str(x) + " " + str(y))
        self.game[y][x] = Player_ob.Player_object_board(self.table_to_pixels(x, y), player_desc)
        self.last_pos = (y, x)

        #self.show_board()

    def table_to_pixels(self, x, y):
        return int(x * 50), int((y * 50) + 450)

    # bomb position 'B x1y2'
    def set_bomb(self, addr, position, player_id):
        # print(" w set_bomb")
        # print("position", position)
        # print("typ: ", type(position))
        position = json.loads(position)

        x = position["ME"]["x"]
        y = position["ME"]["y"]

        i, j = self.table_to_pixels(x, y)

        # print("table dimension " + str(x) + " " + str(y))
        description_bomb = "player " + str(player_id)
        self.game[y][x] = bomb.Bomb(i, j, description_bomb)

        return x, y


    def check_is_any_player_dead(self):
        list_of_dead = []
        print("check is any player dead ", self.list_to_destroy)
        print("self.number_players ", self.number_players)
        for i in self.list_to_destroy:
            for j in range(0, self.number_players):
                x, y = self.get_player_pos(j)
                if i[0] == y and i[1] == x:
                    list_of_dead.append(j)
        print("list of dead ", list_of_dead)
        return list_of_dead

    def rand_board(self):
        board = "WWWWWWWWWWWWWWWW             WWSW W W W W W WW             WW W W W W W W WW             WW W W W W W W WW             WW W W W W W W WW             WW W W W W W W WW             WW W W W W W W WW             WWWWWWWWWWWWWWWW"

        list_to_rand = []
        for i in range(18, 26):
            list_to_rand.append(i)
        for i in range(33, 41, 2):
            list_to_rand.append(i)

        for j in range(0, 3):
            for i in range(76, 88):
                list_to_rand.append(i + (30 * j))

        for j in range(0, 2):
            for i in range(61, 73, 2):
                list_to_rand.append(i + (30 * j))

        for i in range(166, 178):
            list_to_rand.append(i)
        for i in range(183, 185, 2):
            list_to_rand.append(i)
        for i in range(198, 206):
            list_to_rand.append(i)
        print(list_to_rand)

        print(len(list_to_rand))
        list_new = []
        for i in range (0, 50):
            a = random.choice(list_to_rand)
            list_to_rand.remove(a)
            list_new.append(a)

        print("list new  ")
        for i in list_new:
            new = list(board)
            new[i] = 'B'
            board = ''.join(new)

        print("ilosc wystapien ", board.count('B'))
        print(list_new)
        print(board)
        self.board = board

    def handle_bombs(self, x, y):
        time.sleep(1.5)
        self.count_where_blow(x, y)

        # print("self.list_to_destroy ", self.list_to_destroy)
        ans = self.check_is_any_player_dead()

        if ans != []:
            print("Zginal graczz o numerze: ", ans)
        else:
            print("Nikt nie zginal")
        return ans

    # count where is it about to blow and send list client
    def count_where_blow(self, xx, yy):
        self.list_to_destroy = []

        x_brick_1, y_brick_1 = xx, yy + 1
        self.which_one(x_brick_1, y_brick_1)

        x_brick_2, y_brick_2 = xx, yy - 1
        self.which_one(x_brick_2, y_brick_2)

        x_brick_3, y_brick_3 = xx - 1, yy
        self.which_one(x_brick_3, y_brick_3)

        x_brick_4, y_brick_4 = xx + 1, yy
        self.which_one(x_brick_4, y_brick_4)

        self.list_to_destroy.append((xx, yy))

    def which_one(self, x_brick, y_brick):
        if self.game[x_brick][y_brick] != 0:
            if self.game[x_brick][y_brick].desc == "brick" or self.game[x_brick][y_brick].desc[0:6] == "player":
                self.list_to_destroy.append((x_brick, y_brick))
        else:
            self.list_to_destroy.append((x_brick, y_brick))

    def get_player_pos(self, player_id):
        a, b = '', ''
        while a == '':
            for i in range(len(self.game)):
                for j in range(len(self.game[i])):
                    if self.game[i][j] != 0:
                        if self.game[i][j].desc == ("player " + str(player_id)):
                            return j, i
                        elif self.game[i][j].desc == "bomb":
                            if self.game[i][j].whose_bomb == ("player " + str(player_id)):
                                a, b = j, i
        return a, b

    def check_if_player_left_bomb(self, player_id):
        left_bomb = False
        for i in range(len(self.game)):
            for j in range(len(self.game[i])):
                if self.game[i][j] != 0:
                    if self.game[i][j].desc == "bomb":
                        if self.game[i][j].whose_bomb == "player " + str(player_id):
                            left_bomb = True
        return left_bomb

    def find_new_player_position(self, last_pos, dx, dy):
        print("last_pos ", last_pos)
        x, y = int(last_pos[0] + dx), int(last_pos[1] + dy)

        if self.game[y][x] == 0:
            return x, y
        else:
            return last_pos














