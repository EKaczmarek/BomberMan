from Classes.Player import Player
from Classes.Board import Board
from Classes.Client import Client
from PyQt5.QtCore import pyqtSlot
from PyQt5 import QtCore
from threading import Thread
import ast


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
        # print("In main game")
        self.client.connect_to_serwer("192.168.0.102")

        # get map from server
        self.get_map()
        # print("after main game")

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

    @pyqtSlot(bool, str, str)
    def have_map_params_response(self, value, params_json, flag):
        if value:
            if flag == "GET":
                self.handle_get_from_server(params_json)
            elif flag == "MY_POS":
                self.handle_my_pos_from_server(params_json)
                self.map_game.display_all()
            elif flag == "OTHERS_POS":
                self.handle_others_pos_from_server(params_json)
                self.map_game.display_all()
            elif flag == "BOMB":
                self.handle_info_bomb_from_server(params_json)
                self.map_game.display_all()
        else:
            pass
            # print(".... have_map_params ", value)

    def handle_info_bomb_from_server(self, params_json):
        print("Odebrano od serwera info o bomach ", params_json)
        self.map_game.set_bomb_on_map(params_json)


    def handle_get_from_server(self, params_json):
        # print(".... have_map_params ", value)
        # print("Odpowiedz serwera to : ", params_json)

        self.map_game.init_map()
        self.map_game.handle_serwer_ans_on_get(params_json)

        self.map_game.set_objects_on_map()
        self.player.set_players_pos(self.map_game.pos,
                                    self.map_game.list_of_players,
                                    self.map_game.my_id)
        # player position self.player.x, self.player.y,
        # !!!!!!!!!!!! Rect object self.player.rect
        # !!!!!!!!!!!! other players self.player.other_players_rects

        self.thread = Thread(target=self.main_loop, args=[])
        self.thread.start()

        self.map_game.display_all()

    def main_loop(self):
        while True:
            self.player.handle_moves()

    def handle_my_pos_from_server(self, params_json):
        answer = ast.literal_eval(params_json)
        print(answer[self.player.my_id])
        self.map_game.update_player_position(self.player.my_id, answer[self.player.my_id])
        self.map_game.display_all()

    def handle_others_pos_from_server(self, params_json):
        answer = ast.literal_eval(params_json)
        for k, v in answer.items():
            if k.isdigit():
                self.map_game.update_player_position(k, v)

        self.map_game.display_all()

    @pyqtSlot(bool, int, int)
    def player_has_moved_response(self, value, dx, dy):
        if value:
            self.client.send_position_update(dx/50, dy/50)

    @pyqtSlot(bool, str)
    def player_has_left_bomb_response(self, value, player_id):
        if value:
            x, y = self.map_game.get_player_position(player_id)
            print("player id ", player_id)
            print("player position x y " + str(x) + " " + str(y))
            self.client.send_info_about_bomb(y, x)




