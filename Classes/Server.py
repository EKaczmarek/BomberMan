import socket
from Classes import Game_state as gs
import json
from PyQt5 import QtCore
import time
import requests
from threading import Thread

class Server(QtCore.QObject):

    dict_players = {}
    players_to_send = {}
    player_nr = 0
    info_about_players = []

    pl_number_name = {}
    players_number_to_name = []

    set_bomb = QtCore.pyqtSignal(bool, tuple, str)

    def __init__(self, parent=None):
        super(Server, self).__init__()

        self.host = None
        self.port = None
        self.size = None

    def connectWithClient(self):
        self.host = ''
        self.port = 50001
        self.size = 2048
        try:
            self.s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            self.s.bind((self.host, self.port))
            self.game_state = gs.Game_state()

            self.game_state.rand_board()
            board = self.game_state.board
            self.game_state.set_board(board)

        except ConnectionRefusedError as err:
            self.s.close()

    # nasłuchiwanie przez serwer
    def listening(self):
        while True:
            try:
                data, addr = self.s.recvfrom(self.size*2)
                # print("Otrzymano: ", data)
                if data:
                     self.sending_to_client(data.decode("utf-8"), addr)
                else:
                    continue
            except ConnectionRefusedError as err:
                break

    # obliczenie id gracza na podstawie adresu IP - porownanie z wartosciami w slowniku self.dict_players
    def get_player_id(self, addr):
        for key, value in self.dict_players.items():
            if(value == addr):
                # # print("id tego gracza to: ", key)
                return key

    def find_nickname(self, id):
        nickname = ''
        for i in self.players_number_to_name:
            print(i)
            for key, value in i.items():
                if key == id:
                    nickname = value
        return nickname

    def send_info_to_client_game_over(self, info_about_players, player_id):
        print("send info about game over client ", info_about_players)
        addr = ('', '')
        for k, v in self.dict_players.items():
            if k == player_id:
                addr = v[0], v[1]

        print(addr)
        res_info_about_player = ''
        for i in info_about_players:
            for k, v in i.items():
                if k == 'id':
                    res_info_about_player = i
                    break

        print(res_info_about_player)
        data = {"type": "END_GAME", 'SCORES': res_info_about_player}
        print("wyslano ", res_info_about_player)
        print("addr ", addr)
        self.s.sendto(json.dumps(data).encode("utf-8"), addr)

    def reaction_on_get(self, addr, lista_graczy, players_login):
            self.dict_players[self.player_nr] = addr

            self.pl_number_name[self.player_nr] = players_login

            if self.player_nr == 0:
                self.player_pos = {"x": 1, "y": 1}
            elif self.player_nr == 1:
                self.player_pos = {"x": 13, "y": 1}
            elif self.player_nr == 2:
                self.player_pos = {"x": 1, "y": 13}
            elif self.player_nr == 3:
                self.player_pos = {"x": 13, "y": 13}

            self.players_to_send[self.player_nr] = self.player_pos
            lista_graczy.append(self.dict_players)

            # slownik numer gracza - nazxwa gracza
            # lista self.players_number_to_name
            self.players_number_to_name.append(self.pl_number_name)
            print("Odwzorowowanie number gracza - login ", self.players_number_to_name)
            self.to_send = {}

            # TO DO
            self.player_nr += 1

            time.sleep(10)
            # TO DO oczekiwanie na graczy
            self.game_state.number_players = self.player_nr + 1
            print(self.game_state.number_players)

            if self.game_state.number_players > 1: # >
                self.game_state.place = self.game_state.number_players

                for key, value in self.dict_players.items():
                    self.send_info_players_game(key, value)
            else:
                print("No one to play :(")
                # TO DO
                # send info to client that no one to play

            for k, v in self.to_send.items():
                self.s.sendto((json.dumps(self.to_send[k])).encode("utf-8"), k)

    def send_info_players_game(self, key, value):
        nickname = self.find_nickname(key)

        data_player = {'id': key,
                       'nickname': nickname,
                       'bombs': 0,
                       'players_count': self.game_state.number_players,
                       'place': 0}

        print(data_player)
        self.info_about_players.append(data_player)

        payload = {"type": "GET",
                   "status": 200, key: self.players_to_send[key],
                   "players": self.players_to_send,
                   "board": self.game_state.board}

        # self.s.sendto((json.dumps(payload)).encode("utf-8"), value)

        self.to_send[value] = payload

        x = self.players_to_send[key]["x"]
        y = self.players_to_send[key]["y"]
        self.game_state.update_player_position(key, (x, y))

    def reaction_on_pos(self, addr, data):
        id = self.get_player_id(addr)
        data = json.loads(data)

        dx, dy = int(data["ME"]["x"]), int(data["ME"]["y"])

        speed = self.game_state.get_players_speed(id)

        for i in range(0, speed):
            time.sleep(.2)
            last_pos = self.game_state.get_player_pos(id)
            new_pos, opis = self.game_state.find_new_player_position(last_pos, dx, dy)


            # poniżej wymiar tablicy np x=1 y=2
            self.game_state.update_player_position(id, (new_pos[0], new_pos[1]))

            if opis != "last" and opis != "empty":
                self.game_state.set_player_powerup(id, opis)

            data = {"type": "POS", id: {"x": new_pos[0], "y": new_pos[1]}}
            self.s.sendto(json.dumps(data).encode("utf-8"), addr)

            data = {"type": "UPDATE_POS", id: {"x": new_pos[0], "y": new_pos[1]}}

            self.game_state.show_board()
            for i, k in self.dict_players.items():
                if i != id:
                    self.s.sendto(json.dumps(data).encode("utf-8"), self.dict_players[i])

    def add_bomb_to_player(self, player_id):
        for i in self.info_about_players:
            if i["id"] == player_id:
                i["bombs"] += 1

    def set_place_to_player(self, player_id, place):
        for i in self.info_about_players:
            if i["id"] == player_id:
                i["place"] = place

    def send_info_to_db(self, info_about_players):
        new_statistics = {}

        for i in info_about_players:
            name = i.pop('nickname')
            id = i.pop('id')
            new_statistics[name] = i
        print("new statistics ", new_statistics)

        try:
            URL = 'http://192.168.43.102:8080/api/privileged/ranking/'
            AUTH = requests.auth.HTTPBasicAuth('game_server', 'game_server123')
            response = requests.post(URL, auth=AUTH, json=new_statistics)
            if response.ok:
                print('statistics added for players: {}'.format(', '.join(new_statistics.keys())))
                print()
        except requests.exceptions.RequestException or requests.exceptions.Timeout \
                or requests.exceptions.HTTPError or requests.exceptions.TooManyRedirects:
            text = "Can't connect to management server"
            self.error_connection_server_logging.emit(True, text)
            print(text)


    def reaction_on_bomb(self, addr, data):
        # sprawdzenie ile bomb zostawił gracz i ile może zostawić
        self.set_bomb.emit(True, addr, data)

    # wysylanie informacji do klienta na podstawie otrzymanej wiadomosci
    def sending_to_client(self, data, addr):
        lista_graaczy = []
        try:
            c = json.loads(data)['type']

            # wyslanie informacji o planszy, jaka pozycje ma zajac gracz, o pozycjach inn
            if c == "GET":
                self.reaction_on_get(addr, lista_graaczy, json.loads(data)['login'])

            # wysłanie informacji o pozycji:
            #   do gracza od ktorego przyszla zwrotnej informacji ze jest ok
            #   do pozostałych informacji o tym że inny gracz wykonał ruch
            elif c == "POS":
                self.reaction_on_pos(addr, data)

            # wysłanie informacji o bombie
            elif c == "BOMB":
                self.reaction_on_bomb(addr, data)

            # opuszczenie gry przez gracza
            elif c == "EXIT":
                pass

            elif c == "BOMB_BLOW_OK":
                self.game_state.show_board()

        except UnicodeDecodeError:
            pass
            # # print("Bład dekodowania")


    def stopConnection(self):
        self.stream.stop_stream()
        self.stream.close()
        self.s.close()










