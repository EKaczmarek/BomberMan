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

    player_has_moved = QtCore.pyqtSignal(bool, str, int, int)

    def __init__(self):
        super(Player, self).__init__()
        pass

    def table_to_pixels(self, x, y):
        return int((x*50)+450), int(y*50)

    def set_players_pos(self, pos, list_of_players, my_id):
        self.x, self.y = pos
        self.my_id = my_id

        x_pixels, y_pixels = self.table_to_pixels(self.x, self.y)
        self.rect = pygame.Rect(y_pixels, x_pixels, self.PLAYER_DIMENSION, self.PLAYER_DIMENSION)

        for item in list_of_players:
            for key, value in item.items():
                x_pixels_others, y_pixels_others = self.table_to_pixels(value["x"], value["y"])
                self.other_players_rects.append({key: pygame.Rect(y_pixels_others, x_pixels_others, 50, 50)})

        # self.handle_bombs()

    def handle_moves(self):
        for e in pygame.event.get():
            if e.type == pygame.KEYDOWN:
                if e.key == pygame.K_LEFT:
                    self.move(-50, 0)
                if e.key == pygame.K_RIGHT:
                    self.move(50, 0)
                if e.key == pygame.K_UP:
                    self.move(0, -50)
                if e.key == pygame.K_DOWN:
                    self.move(0, 50)
                if e.key == pygame.K_b:
                    self.leave_bomb()

            # actions = clicking Exit, Menu
            if e.type == pygame.QUIT:
                self.exit_key = True
                self.send_message_to_server("EXIT")
            if e.type == pygame.KEYDOWN and e.key == pygame.K_ESCAPE:
                self.exit_key = True
                self.send_message_to_server("EXIT")
            if e.type == pygame.MOUSEBUTTONDOWN and e.button == 1:
                mouse = pygame.mouse.get_pos()
                """if self.board.exitBtn.button.collidepoint(mouse):
                    self.send_message_to_server("EXIT")
                    self.exit_key = True"""

    def move(self, dx, dy):

        if dx != 0:
            self.move_single_axis(dx, 0)
        if dy != 0:
            self.move_single_axis(0, dy)

    def move_single_axis(self, dx, dy):

        i = self.my_id

        self.rect.x += dx
        self.rect.y += dy

        self.player_has_moved.emit(True, i, dx, dy)

    def send_message_to_server(self, message):
        self.board.cl.sendMessage(message)

    def handle_bombs(self):
        # powUP = pygame.image.load(r"Classes/Pictures/wall.png").convert()

        if (self.bomb_key == True):
            seconds = (pygame.time.get_ticks() - self.bomb.start_timer) / 1000
            if (seconds >= 1.5):
                self.bomb_key = False
                ans = self.check_is_player_dead()
                # print("self.list_to_destroy ", self.board.list_to_destroy)
                for i in self.board.list_to_destroy:
                    for x in range(8):
                        posx, posy = self.board.table_to_pixels(int(i[0]), int(i[1]))
                        self.board.screen.blit(self.images[x], (posy, posx))
                        pygame.display.flip()
                    self.board.game[i[0]][i[1]] = 0
                if (ans):
                    self.show_player = False

    def send_to_server_info_bomb(self):
        bomb_pos = self.get_pos_to_bomb()
        payload = {"type": "BOMB", "B": {"x": bomb_pos[0], "y": bomb_pos[1]}}
        print("Wiadomosc o bombie do serwera: ", payload)
        self.send_message_to_server(payload)
        # # print("do serwera wyslano :" + str(payload))

        # a = self.board.cl.wait4Response()
        # print("odpowiedz serwera - lista do wybuchu: " + str(a))

        # DODANIE DO LISTY DO WYBUCHU
        # self.board.list_to_destroy = a
        # # print(a)

    def leave_bomb(self):
        BombExplode = pygame.mixer.Sound('Classes/Music/TimeBomb.wav')
        if (self.bomb_key == False):
            xx, yy = self.get_pos_to_bomb()
            # # print("xx " + str(xx) + " yy " + str(yy))

            self.send_to_server_info_bomb()
            self.bomb = bom.Bomb(xx, yy)

            self.left_bombs += 1

            self.board.game[int(yy / 50)][int((xx - 450) / 50)] = self.bomb.get_bomb()
            self.bomb_key = True

            pygame.mixer.Sound.play(BombExplode)

            # # print(self.board.list_to_destroy)

    def get_pos_to_bomb(self):
        return self.rect.x, self.rect.y