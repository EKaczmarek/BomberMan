from Classes.Player import Player
from Classes.Board import Board
from Classes.Client import Client
from PyQt5.QtCore import pyqtSlot
from PyQt5.QtWidgets import QDialog
from PyQt5 import QtCore


class PlayGame(QtCore.QObject):

    def __init__(self, parent = None):
        super(PlayGame, self).__init__()

        self.player = None
        self.map_game = None
        self.client = None

    def setup_all(self):
        player = Player()
        self.setup_player(player)

        map_game = Board()
        self.map_game = map_game

        client = Client()
        self.client = client

        print("All setud up")

    def run_game(self):
        print("In main game")
        self.client.connect_to_serwer("192.168.0.102")

        # get map from server
        self.get_map()
        print("after main game")

    def setup_player(self, player):
        self.player = player

    def setup_map(self, map_game):
        self.map_game = map_game

    def setup_client(self, client):
        self.client = client

    def get_map(self):
        self.client.sendMessage({"type": "GET"})

    @pyqtSlot(bool, str)
    def have_map_params(self, value, params_json):
        if value:
            print(".... have_map_params ", value)
            print("Odpowiedz serwera to : ", params_json)
        else:
            print(".... have_map_params ", value)
