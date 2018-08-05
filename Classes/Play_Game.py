from Classes.Player import Player
from Classes.Board import Board
from Classes.Client import Client
from PyQt5.QtCore import pyqtSlot
from PyQt5.QtWidgets import QDialog
from PyQt5 import QtCore
from threading import Thread
import ast
import pygame

class PlayGame(QtCore.QObject):

    def __init__(self, parent = None):
        super(PlayGame, self).__init__()

        self.player = None
        self.map_game = None
        self.client = None

        self.is_running = False

    def setup_all(self):
        player = Player()
        self.setup_player(player)

        map_game = Board()
        self.map_game = map_game

        client = Client()
        self.client = client

    def run_game(self):
        print("In main game")
        self.client.connect_to_serwer("192.168.1.12")

        # get map from server
        self.get_map()
        print("after main game")

        thread = Thread(target=self.client.listening, args=[])
        thread.start()

    def setup_player(self, player):
        self.player = player

    def setup_map(self, map_game):
        self.map_game = map_game

    def setup_client(self, client):
        self.client = client

    def get_map(self):
        self.is_running = True
        self.client.sendMessage({"type": "GET"})
        print("Wylano wiadomosc z get_mapp!!!!!! lololo")

    @pyqtSlot(bool, str)
    def have_map_params(self, value, params_json):
        if value:
            print(".... have_map_params ", value)
            print("Odpowiedz serwera to : ", params_json)
            self.map_game.init_map()
            self.map_game.set_objects_on_map()

            self.map_game.handle_serwer_ans_on_get(params_json)

            self.player.set_players_pos(self.map_game.pos, self.map_game.list_of_players)
            # player position self.player.x, self.player.y,
            # !!!!!!!!!!!! Rect object self.player.rect
            # !!!!!!!!!!!! other players self.player.other_players_rects

            self.map_game.display_all()

            """self.game = self.map_game.game

            self.map_game.load()

            self.player.init_game()

            self.map_game.display_all(self.pygame, self.game)

            self.map_game.show_map()"""
        else:
            print(".... have_map_params ", value)



