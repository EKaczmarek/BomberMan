from Classes.Player import Player
from Classes.Board import Board
from Classes.Client import Client
from PyQt5.QtCore import pyqtSlot
from PyQt5.QtWidgets import QDialog
from PyQt5 import QtCore
from threading import Thread
import ast

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

        thread = Thread(target=self.client.listening, args=[])
        thread.start()

    def setup_player(self, player):
        self.player = player

    def setup_map(self, map_game):
        self.map_game = map_game

    def setup_client(self, client):
        self.client = client

    def get_map(self):
        self.client.sendMessage({"type": "GET"})
        print("Wsylano wiadomosc")


    def handle_serwer_ans_on_get(self, answer_on_get):
        self.my_id = 0

        # I know it's dangerous but on windows json.loads doesnt work here :(
        answer = ast.literal_eval(answer_on_get)

        for key, value in answer.items():
            print(type(key))
            if(key.isdigit()):
                print(key)
                self.my_id = key

        level = answer["board"]
        pos = (answer[self.my_id]["x"], answer[self.my_id]["y"])

        list_of_players = []

        for key, value in answer.items():
            if (key=="players"):
                for k, v in value.items():
                    if(str(k) != str(self.my_id)):
                        list_of_players.append({k: v})


        print("plansza: ", level)
        print("moja pozycja: ", pos)
        print("inni gracze: " + str(list_of_players))

        self.level, self.pos, self.list_of_player =  map(''.join, zip(*[iter(level)]*15)), pos, list_of_players


    @pyqtSlot(bool, str)
    def have_map_params(self, value, params_json):
        if value:
            print(".... have_map_params ", value)
            print("Odpowiedz serwera to : ", params_json)
            self.handle_serwer_ans_on_get(params_json)
        else:
            print(".... have_map_params ", value)



