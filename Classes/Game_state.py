import Classes.Wall as w
import Classes.Brick as b
import Classes.Bomb as bomb
import Classes.Player_object_board as Player_ob
import json
from PyQt5 import QtCore
import random
from Classes.Powerup import Powerup
import time
from threading import Thread

class Game_state(QtCore.QObject):

    bomb_must_blow = QtCore.pyqtSignal(bool, int, int)
    game_over = QtCore.pyqtSignal(bool, int, int)

    level = []
    last_pos = ''
    number_players = 0


    def __init__(self):
        super(Game_state, self).__init__()
        self.game = [[0 for col in range(15)] for row in range(15)]
        for i in range(len(self.game)):
            for j in range(len(self.game[i])):
                self.game[i][j] = 0

    def set_board(self, board):
        self.level = map(''.join, zip(*[iter(board)]*15))
        self.walls_bricks()

    def get_winner_id(self):
        id = ''
        for i in range(len(self.game)):
            for j in range(len(self.game[i])):
                if self.game[i][j] != 0:
                    if self.game[i][j].desc[0:6] == "player":
                        name, id = self.game[i][j].desc.split(" ")
                        print("wygral ", id)
        return id



    def how_many_players_left(self):
        player_ammount = 0
        for i in range(len(self.game)):
            for j in range(len(self.game[i])):
                if self.game[i][j] != 0:
                    if self.game[i][j].desc[0:6] == "player":
                        player_ammount += 1
        return player_ammount

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

        if self.last_pos == '':
            print("\n tworzenie obiektu \n")
            self.game[1][1] = Player_ob.Player_object_board((1, 1), "player 1", 1, 1, 1)
            self.last_pos = (1, 1)

    # from pixels to table dimenstion
    def table_dimension(self, x, y):
        return int(x/50), int((y-450)/50)

    def show_board(self):
        pass
        """print("~~~~~~~~~~~~~~~~~~~~~~~~~~Ćala plansza~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~")
        for i in range(len(self.game)):
            for j in range(len(self.game[i])):
                if self.game[i][j] != 0:
                    print(self.game[i][j].desc, end="\t")
                else:
                    print("empty", end="\t")
            print(end='\n')"""

    def remove_player_from_map(self, json_dead):
        print("json dead ", json_dead)
        if json_dead != {}:
            for k, v in json_dead.items():
                print("id gracza ", k)
                x, y = v[0], v[1]
                self.game[y][x] = 0
                print("X ", x)
                print("y ", y)

        print("Po usunieciu gracza na serwerze")


    def player_can_leave_bomb(self, player_id):

        number_bombs_on_board = self.get_number_player_number_bombs_on_board(player_id)
        print("\nnumber_bombs_on_board ", number_bombs_on_board)

        time.sleep(.5)
        k, w = self.get_player_pos(player_id)

        if self.game[w][k].desc[0:6] == "player":
            player = self.game[w][k].get_player()
            number_player_can_leave = player.bombs

            print("number_player_can_leave ", number_player_can_leave)

        if number_player_can_leave > number_bombs_on_board:
            return True

    def get_players_speed(self, player_id):
        speed = 1

        k, w = self.get_player_pos(player_id)

        if self.game[w][k].desc[0:6] == "player":
            player = self.game[w][k].get_player()
            speed = player.speed

            print("players_speed ", speed)
        return speed

    def get_range_of_bomb(self, player_id):
        player_range_of_bombs = 1
        k, w = self.get_player_pos(player_id)

        if self.game[w][k].desc[0:6] == "player":
            player = self.game[w][k].get_player()
            player_range_of_bombs = player.range_bomb

            print("player range of bombs ", player_range_of_bombs)

        return player_range_of_bombs




    def find_last_position(self, player_id):

        for i in range(len(self.game)):
            for j in range(len(self.game[i])):
                if self.game[i][j] != 0:
                    player_desc = "player " + str(player_id)
                    if self.game[i][j].desc == player_desc:
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

        last_pos = self.find_last_position(player_id)

        bombs = 1
        range = 1
        speed = 1

        # attributes to powerups
        if self.game[last_pos[1]][last_pos[0]] != 0:
            if not isinstance(self.game[last_pos[1]][last_pos[0]].desc, int):
                if self.game[last_pos[1]][last_pos[0]].desc[0:6] == "player":
                    bombs = self.game[last_pos[1]][last_pos[0]].bombs
                    range = self.game[last_pos[1]][last_pos[0]].range_bomb
                    speed = self.game[last_pos[1]][last_pos[0]].speed

        self.game[last_pos[1]][last_pos[0]] = 0

        # set current position of player
        player_desc = "player " + str(player_id)
        self.game[y][x] = Player_ob.Player_object_board(self.table_to_pixels(x, y), player_desc, bombs, range, speed)
        self.last_pos = (y, x)


    def set_player_powerup(self, id, opis):
        x, y = self.get_player_pos(id)
        if opis == "S":
            self.game[y][x].set_speed()
            thread = Thread(target=self.game[y][x].start_timer_speed, args=[])
            thread.start()
            print(self.game[y][x].speed)
        elif opis == "N":
            self.game[y][x].set_range_bomb()
            thread = Thread(target=self.game[y][x].start_timer_bombs_range, args=[])
            thread.start()
            print("set_bombs ", self.game[y][x].range_bomb)
        elif opis == "R":
            self.game[y][x].set_bombs_number()
            thread = Thread(target=self.game[y][x].start_timer_bombs_no, args=[])
            thread.start()
            print("number_bombs ", self.game[y][x].bombs)


    def table_to_pixels(self, x, y):
        return int(x * 50), int((y * 50) + 450)

    # bomb position 'B x1y2'
    def set_bomb(self, addr, position, player_id):
        position = json.loads(position)

        x = position["ME"]["x"]
        y = position["ME"]["y"]

        i, j = self.table_to_pixels(x, y)

        # print("table dimension " + str(x) + " " + str(y))
        description_bomb = "player " + str(player_id)
        self.game[y][x] = bomb.Bomb(i, j, description_bomb)

        return x, y


    
    def board_ranges(self):
        self.list_to_rand = []
        for i in range(18, 26):
            self.list_to_rand.append(i)
        for i in range(33, 41, 2):
            self.list_to_rand.append(i)

        for j in range(0, 3):
            for i in range(76, 88):
                self.list_to_rand.append(i + (30 * j))

        for j in range(0, 2):
            for i in range(61, 73, 2):
                self.list_to_rand.append(i + (30 * j))

        for i in range(166, 178):
            self.list_to_rand.append(i)
        for i in range(183, 185, 2):
            self.list_to_rand.append(i)
        for i in range(198, 206):
            self.list_to_rand.append(i)
        print(self.list_to_rand)

    def rand_board(self):
        board = "WWWWWWWWWWWWWWWW             WW W W W W W W WW             WW W W W W W W WW             WW W W W W W W WW             WW W W W W W W WW             WW W W W W W W WW             WW W W W W W W WW             WWWWWWWWWWWWWWWW"

        self.board_ranges()

        print(len(self.list_to_rand))
        list_new = []
        # losowanie Brick
        for i in range(0, 50):
            a = random.choice(self.list_to_rand)
            self.list_to_rand.remove(a)
            list_new.append(a)

        #dodanie do planszy
        for i in list_new:
            new = list(board)
            new[i] = 'B'
            board = ''.join(new)
        

        list_powerup = []
        for i in range(0, 30):
        # losowanie Powerup'ow
            a = random.choice(list_new)
            list_new.remove(a)
            list_powerup.append(a)

        for i in list_powerup:
            new = list(board)
            new[i] = random.choice(['S', 'R', 'N'])
            board = ''.join(new)

        print("board", board)
        self.board = board
        #self.board = "WWWWWWWWWWWWWWWW    R   SB   WW WSWNWBW W W WW             WWRWRW W W WSW WWBB N RBN  BR WWBW W WBW WNW WWRNS BNS BBN  WW W W W W W W WW B RR BB S B WW W W W W W W WWNB  SS BB SB WW W W W W W W WW  NS NBSS    WWWWWWWWWWWWWWWW"

    def handle_bombs(self, x_bomb, y_bomb, list_to_destroy):

        list_of_dead = []

        for i in list_to_destroy:
            if self.game[i[1]][i[0]] != 0:
                if self.game[i[1]][i[0]].desc[0:6] == "player":
                    number = self.game[i[1]][i[0]].desc.split(" ")[1]
                    list_of_dead.append(number)

        return list_of_dead

    # count where is it about to blow and send list client
    def count_where_blow(self, xx, yy, range_of_bomb):
        self.list_to_destroy = []

        self.list_to_destroy.append((xx, yy))

        x_brick_1, y_brick_1 = xx, yy + 1
        self.which_one(x_brick_1, y_brick_1)

        x_brick_2, y_brick_2 = xx, yy - 1
        self.which_one(x_brick_2, y_brick_2)

        x_brick_3, y_brick_3 = xx - 1, yy
        self.which_one(x_brick_3, y_brick_3)

        x_brick_4, y_brick_4 = xx + 1, yy
        self.which_one(x_brick_4, y_brick_4)

        if range_of_bomb != 1:
            for j in range(1, range_of_bomb):
                if (x_brick_1, y_brick_1) in self.list_to_destroy:
                    x_brick_1, y_brick_1 = xx, yy + 1 + j
                    self.which_one(x_brick_1, y_brick_1)

                if (x_brick_2, y_brick_2) in self.list_to_destroy:
                    x_brick_2, y_brick_2 = xx, yy - 1 - j
                    self.which_one(x_brick_2, y_brick_2)

                if (x_brick_3, y_brick_3) in self.list_to_destroy:
                    x_brick_3, y_brick_3 = xx - 1 - j, yy
                    self.which_one(x_brick_3, y_brick_3)

                if (x_brick_4, y_brick_4) in self.list_to_destroy:
                    x_brick_4, y_brick_4 = xx + 1 + j, yy
                    self.which_one(x_brick_4, y_brick_4)

        print(self.list_to_destroy)

    def which_one(self, x_brick, y_brick):
        if self.game[x_brick][y_brick] != 0:
            if self.game[x_brick][y_brick].desc == "brick" or self.game[x_brick][y_brick].desc[0:6] == "player" or self.game[x_brick][y_brick].desc == "powerup":
                self.list_to_destroy.append((x_brick, y_brick))
        else:
            self.list_to_destroy.append((x_brick, y_brick))

    def get_number_player_number_bombs_on_board(self, player_id):
        number_left_bomb = 0
        for i in range(len(self.game)):
            for j in range(len(self.game[i])):
                if self.game[i][j] != 0:
                    if self.game[i][j].desc == "bomb":
                        if self.game[i][j].whose_bomb == "player " + str(player_id):
                            number_left_bomb += 1
        return number_left_bomb

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

    def find_new_player_position(self, last_pos, dx, dy):
        x, y = int(last_pos[0] + dx), int(last_pos[1] + dy)
        if self.game[y][x] == 0:
            return (x, y), "empty"
        else:
            if self.game[y][x].desc == "powerup" and self.game[y][x].view == "powerup":
                return (x, y), self.game[y][x].kind
            else:
                return last_pos, "last"














