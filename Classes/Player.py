import pygame
import time
import glob
import Classes.Board as board
import Classes.Bomb as bom
import Classes.Wall as wal
import Classes.Brick as brick
import Classes.Powerup as powerup
import re
import json
from PyQt5 import QtCore
from PyQt5.QtCore import pyqtSlot



class Player(QtCore.QObject):

    # client to connect with server

    walls = []  # List to hold walls
    bricks = []  # List to hold bricks
    side = 0

    lista = []
    images = []
    other_players_rects = []

    PLAYER_DIMENSION = 50

    # Initialize flags
    show_player = True
    exit_key = False
    bomb_key = False
    left_bombs = 0

    rect = None

    player_has_moved = QtCore.pyqtSignal(bool, int, int, int)

    def __init__(self):
        super(Player, self).__init__()
        pass


    def table_to_pixels(self, x, y):
        return int((x*50)+450), int(y*50)

    def set_players_pos(self, pos, list_of_players):

        print("w set platers")
        # set position of player from server
        self.x, self.y = pos
        print("my position: ", pos)
        print("other players' position: ", list_of_players)

        print("Moje wspolrzedne to " + str(self.x) + " " + str(self.y))
        x_pixels, y_pixels = self.table_to_pixels(self.x, self.y)
        print("Pikselowo " + str(x_pixels) + " " + str(y_pixels))
        self.rect = pygame.Rect(x_pixels, y_pixels, self.PLAYER_DIMENSION, self.PLAYER_DIMENSION)

        for item in list_of_players:
            for key, value in item.items():
                print(key, " ", value)
                self.other_players_rects.append({key: pygame.Rect(self.x, self.y, 50, 50)})

        print("self.other_players_rects ", self.other_players_rects)

    def init_game(self):
        self.main_loop()

    def main_loop(self):
        while self.exit_key != True:
            self.handle_moves()
            # self.handle_bombs()

    def handle_moves(self):

        for e in pygame.event.get():
            if e.type == pygame.KEYDOWN:
                if e.key == pygame.K_LEFT:
                    self.move(-50, 0)
                    Player.side = 1
                if e.key == pygame.K_RIGHT:
                    self.move(50, 0)
                    Player.side = 0
                if e.key == pygame.K_UP:
                    self.move(0, -50)
                if e.key == pygame.K_DOWN:
                    self.move(0, 50)
                if e.key == pygame.K_b:
                    self.leave_bomb()

            # actions = clickig Exit, Menu
            if e.type == pygame.QUIT:
                self.exit_key = True
                self.send_message_to_server("EXIT")
            if e.type == pygame.KEYDOWN and e.key == pygame.K_ESCAPE:
                self.exit_key = True
                self.send_message_to_server("EXIT")
            if e.type == pygame.MOUSEBUTTONDOWN and e.button == 1:
                mouse = pygame.mouse.get_pos()
                if self.board.exitBtn.button.collidepoint(mouse):
                    self.send_message_to_server("EXIT")
                    self.exit_key = True

    def send_message_to_server(self, message):
        self.board.cl.sendMessage(message)

    def check_is_player_dead(self):
        x, y = self.get_pos()
        message = {"type": "D", "ME": {"x": x, "y": y}}
        # print("Wiadomosc spr czy żyję ", message)
        self.send_message_to_server(message)
        answer = self.board.cl.wait4Response()
        # print("Odpowiedzialalalal " + str(answer))
        if (answer == "True"): return True
        else: return False


    def handle_bombs(self):
        # powUP = pygame.image.load(r"Classes/Pictures/wall.png").convert()

        if (self.bomb_key == True):
            seconds = (pygame.time.get_ticks() - self.bomb.start_timer) / 1000
            if (seconds >= 1.5):
                self.bomb_key = False
                ans = self.check_is_player_dead()
                print("self.list_to_destroy ", self.board.list_to_destroy)
                for i in self.board.list_to_destroy:
                    for x in range(8):
                        posx, posy = self.board.table_to_pixels(int(i[0]), int(i[1]))
                        self.board.screen.blit(self.images[x], (posy, posx))
                        pygame.display.flip()
                    self.board.game[i[0]][i[1]] = 0
                if (ans):
                    self.show_player = False



    def send_to_server_info_bomb(self):
        # self.board.list_to_destroy = []
        # print("Aktualna pozycja bomby x:" + str(self.get_pos()[0]) + " y:" + str(self.get_pos()[1]))

        payload = {"type": "BOMB", "B": {"x": self.get_pos()[0], "y": self.get_pos()[1]}}
        self.send_message_to_server(payload)
        # print("do serwera wyslano :" + str(payload))

        a = self.board.cl.wait4Response()
        print("odpowiedz serwera - lista do wybuchu: " + str(a))

        # DODANIE DO LISTY DO WYBUCHU
        self.board.list_to_destroy = a
        # print(a)

    def leave_bomb(self):
        BombExplode = pygame.mixer.Sound('Classes/Music/TimeBomb.wav')
        if (self.bomb_key == False):
            xx, yy = self.get_pos_to_bomb()
            # print("xx " + str(xx) + " yy " + str(yy))

            self.send_to_server_info_bomb()
            self.bomb = bom.Bomb(xx, yy)

            self.left_bombs += 1

            self.board.game[int(yy / 50)][int((xx - 450) / 50)] = self.bomb.get_bomb()
            self.bomb_key = True

            pygame.mixer.Sound.play(BombExplode)

            # print(self.board.list_to_destroy)

    def move(self, dx, dy):

        if dx != 0:
            self.move_single_axis(dx, 0)
        if dy != 0:
            self.move_single_axis(0, dy)

    def move_single_axis(self, dx, dy):

        self.rect.x += dx
        self.rect.y += dy

        self.player_has_moved.emit(True, 0, dx, dy)

        """for i in range(len(self.board.game)):
            for j in range(len(self.board.game[i])):

                if((type(self.board.game[i][j]) is wal.Wall)
                   or (type(self.board.game[i][j]) is brick.Brick)
                   or (type(self.board.game[i][j]) is bom.Bomb)):

                    if self.rect.colliderect(self.board.game[i][j].rect):
                        if dx > 0:  # Moving right; Hit the left side of the wall
                            self.rect.right = self.board.game[i][j].rect.left
                        if dx < 0:  # Moving left; Hit the right side of the wall
                            self.rect.left = self.board.game[i][j].rect.right
                        if dy > 0:  # Moving down; Hit the top side of the wall
                            self.rect.bottom = self.board.game[i][j].rect.top
                        if dy < 0:  # Moving up; Hit the bottom side of the wall
                            self.rect.top = self.board.game[i][j].rect.bottom

        # print("Aktualna pozycja x:" + str(self.get_pos()[0]) + " y:" + str(self.get_pos()[1]))

        payload = {"type": "POS", "ME": {"x": self.get_pos()[0], "y": self.get_pos()[1]}}

        self.send_message_to_server(payload)
        print("do serwera wyslano :" + str(payload))
        xx, yy = self.board.cl.wait4Response()
        print("odp: " + str(xx) + " " + str(yy))"""

    def get_pos(self):
        # print("Wspolrzedne 1: ", self.rect.x, ", ",self.rect.y)
        xx = int((self.rect.x - 450) / 50)
        yy = int(self.rect.y / 50)
        # print("Wspolrzedne 2: ", xx, ", ", yy)
        return xx, yy

    def get_pos_to_bomb(self):
        return self.rect.x, self.rect.y