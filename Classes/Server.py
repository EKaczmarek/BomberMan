import socket
from Classes import Game_state as gs
import json
from PyQt5 import QtCore
import time

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

            self.game_state.rand_board()
            board = self.game_state.board

            self.game_state.set_board(board)

            # TO DO
            self.player_nr += 1

            # ograniczenie tutaj max 1 graczy
            self.game_state.number_players = 1;
            self.game_state.place = self.game_state.number_players
            if self.player_nr == 1:
                for key, value in self.dict_players.items():

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
                               "board": board}
                    self.s.sendto((json.dumps(payload)).encode("utf-8"), value)
                    x = self.players_to_send[key]["x"]
                    y = self.players_to_send[key]["y"]
                    self.game_state.update_player_position(key, (x, y))

    def reaction_on_pos(self, addr, data):
        id = self.get_player_id(addr)
        data = json.loads(data)

        dx, dy = int(data["ME"]["x"]), int(data["ME"]["y"])

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
        for i in info_about_players:
            payload = {i['nickname']: {'place': i['place'],
                                       'bomb_set': i['bombs'],
                                       'players_count': i['players_count']}}
            print(payload)

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










