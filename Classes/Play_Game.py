from Classes.Player import Player
from Classes.Board import Board
from Classes.Client import Client
from PyQt5.QtCore import pyqtSlot
from PyQt5 import QtCore
from threading import Thread
import ast
import pygame

class PlayGame(QtCore.QObject):

    game_over_for_player = QtCore.pyqtSignal(bool, str)

    error_connection_server_logging = QtCore.pyqtSignal(bool, str)

    def __init__(self, parent = None):
        super(PlayGame, self).__init__()

        self.player = None
        self.map_game = None
        self.client = None

        self.is_running = False

    def set_url(self, url):
        self.url = url

    def setup_all(self):
        player = Player()
        self.setup_player(player)

        map_game = Board()
        self.map_game = map_game

        client = Client()
        self.client = client

    def run_game(self, login):
        # # print("In main game")
        self.client.connect_to_serwer("192.168.0.103")

        self.client.login = login
        # get map from server
        self.get_map(login)
        # # print("after main game")

        thread = Thread(target=self.client.listening, args=[])
        thread.start()


    def setup_player(self, player):
        self.player = player

    def setup_map(self, map_game):
        self.map_game = map_game

    def setup_client(self, client):
        self.client = client

    def get_map(self, login):
        self.is_running = True
        self.client.sendMessage({"type": "GET", "login": login})

    @pyqtSlot(bool, tuple)
    def button_clicked_on_pygame_response(self, value, mouse_pos):
        if value:
            print("in signaln button_clicked_on_pygame_response")

            if self.map_game.exitBtn.button.collidepoint(mouse_pos):
                print("Kliknieto na exit")
                self.client.sendMessage({"type": "EXIT"})
                pygame.quit()

            elif self.map_game.menuBtn.button.collidepoint(mouse_pos):
                print("Kliknieto na back ")
                self.client.sendMessage({"type": "EXIT"})
                print("login ", self.client.login)

                pygame.quit()

                # TO DO
                """try:
                    URL = str(self.url) + '/api/ranking/'

                    response = requests.get(URL, params={'nickname': self.client.login, 'scores': 'true'})
                    if response.ok:
                        statistics = json.loads(response.content.decode())
                        print(json.dumps(statistics, indent=4))
                        print()
    
                    # TO DO statistics for specific player
                    self.game_over_for_player.emit(True)
                except requests.exceptions.RequestException or requests.exceptions.Timeout \
                           or requests.exceptions.HTTPError or requests.exceptions.TooManyRedirects:
                    text = "Can't connect to management server"
                    self.error_connection_server_logging.emit(True, text)
                    print(text)"""
            else:
                pass


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
            elif flag == "PLAYER_DEAD":
                self.handle_info_dead_players_from_server(params_json)
                self.map_game.display_all()
            elif flag == "BOMB_BLOW":
                self.handle_blowing_bomb(params_json)
                self.client.sendMessage({"type": "BOMB_BLOW_OK"})
                self.map_game.display_all()
            elif flag == "END_GAME":
                self.game_over_for_player.emit(True, params_json)
            elif flag == "WINNER":
                print("wygralesm ", self.client.login)

        else:
            pass
            # # print(".... have_map_params ", value)

    def handle_info_bomb_from_server(self, params_json):
        # print("Odebrano od serwera info o bomach ", params_json)
        self.map_game.set_bomb_on_map(params_json)

    def handle_info_dead_players_from_server(self, params_json):
        json_dead = ast.literal_eval(params_json)
        # self.map_game.remove_player_from_map(json_dead)
        print("w handle info dead players from server")

        """for k, v in json_dead.items():
            if k == 'PLAYERS_POS':
                for key, value in v.items():
                    if key == self.map_game.my_id:
                        self.game_over_for_player.emit(True)"""

    def handle_blowing_bomb(self, params_json):
        self.map_game.show_efects_blow(params_json)



    def handle_get_from_server(self, params_json):
        # # print(".... have_map_params ", value)
        # # print("Odpowiedz serwera to : ", params_json)
        self.is_running = True

        self.map_game.init_map(self.client.login)
        self.map_game.handle_serwer_ans_on_get(params_json, self.client.login)

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
        self.player.is_running = True
        self.player.handle_moves()

    def handle_my_pos_from_server(self, params_json):
        answer = ast.literal_eval(params_json)
        # print(answer[self.player.my_id])
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
            print("w player left bomb response")
            x, y = self.map_game.get_player_position(player_id)
            # print("player id ", player_id)
            # print("player position x y " + str(x) + " " + str(y))
            self.client.send_info_about_bomb(y, x)




