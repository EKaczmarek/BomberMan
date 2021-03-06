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
from threading import Thread


class Player(QtCore.QObject):
    button_clicked_on_pygame = QtCore.pyqtSignal(bool, tuple)
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

    player_has_moved = QtCore.pyqtSignal(bool, int, int)
    player_has_left_bomb = QtCore.pyqtSignal(bool, str)

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

    def handle_moves(self):
        try:
            while self.is_running is True:
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
                        if e.key == pygame.K_SPACE:
                            thread = Thread(target=self.set_bomb_board, args=[])
                            thread.start()
                    # actions = clicking Exit, Menu
                    if e.type == pygame.QUIT:
                        self.is_running = False
                    if e.type == pygame.KEYDOWN and e.key == pygame.K_ESCAPE:
                        self.exit_key = True
                        self.send_message_to_server("EXIT")
                    if e.type == pygame.MOUSEBUTTONDOWN and e.button == 1:
                        mouse = pygame.mouse.get_pos()
                        print("typ mouse ", type(mouse))
                        self.button_clicked_on_pygame.emit(True, mouse)
            pygame.quit()
        except:
            pygame.quit()

    def set_bomb_board(self):
        self.send_to_server_info_bomb()
        bomb_explode = pygame.mixer.Sound('Classes/Music/TimeBomb.wav')
        time.sleep(1)
        pygame.mixer.Sound.play(bomb_explode)

    def move(self, dx, dy):

        if dx != 0:
            self.move_single_axis(dx, 0)
        if dy != 0:
            self.move_single_axis(0, dy)

    def move_single_axis(self, dx, dy):

        self.rect.x += dx
        self.rect.y += dy

        self.player_has_moved.emit(True, dx, dy)

    def send_message_to_server(self, message):
        self.board.cl.sendMessage(message)

    def send_to_server_info_bomb(self):
        self.player_has_left_bomb.emit(True, self.my_id)
