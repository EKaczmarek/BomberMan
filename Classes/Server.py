import socket
from Classes import Game_state as gs
import json
from PyQt5 import QtCore
import time

class Server(QtCore.QObject):

    dict_players = {}
    players_to_send = {}
    player_nr = 0

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
                print("Otrzymano: ", data)
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

    def reaction_on_get(self, addr, lista_graczy):
            self.dict_players[self.player_nr] = addr
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

            self.game_state.rand_board()
            board = self.game_state.board

            self.game_state.set_board(board)

            # TO DO
            self.player_nr += 1
            # # print("player_nr ", self.player_nr)


            # ograniczenie tutaj max 1 graczy
            self.game_state.number_players = 1;
            if self.player_nr == 1:
                for key, value in self.dict_players.items():
                    payload = {"type": "GET",
                               "status": 200, key: self.players_to_send[key],
                               "players": self.players_to_send,
                               "board": board}
                    # # print("Do wyslania: ", self.players_to_send)
                    self.s.sendto((json.dumps(payload)).encode("utf-8"), value)
                    # # print("Wyslano")
                    x = self.players_to_send[key]["x"]
                    y = self.players_to_send[key]["y"]
                    self.game_state.update_player_position(key, (x, y))

    def reaction_on_pos(self, addr, data):
        id = self.get_player_id(addr)
        data = json.loads(data)
        dx, dy = int(data["ME"]["x"]), int(data["ME"]["y"])

        last_pos = self.game_state.get_player_pos(id)
        new_pos = self.game_state.find_new_player_position(last_pos, dx, dy)

        # poniżej wymiar tablicy np x=1 y=2
        self.game_state.update_player_position(id, (new_pos[0], new_pos[1]))

        data = {"type": "POS", id: {"x": new_pos[0], "y": new_pos[1]}}
        self.s.sendto(json.dumps(data).encode("utf-8"), addr)

        data = {"type": "UPDATE_POS", id: {"x": new_pos[0], "y": new_pos[1]}}

        self.game_state.show_board()
        for i, k in self.dict_players.items():
            if i != id:
                self.s.sendto(json.dumps(data).encode("utf-8"), self.dict_players[i])

    # wysylanie informacji do klienta na podstawie otrzymanej wiadomosci
    def sending_to_client(self, data, addr):
        lista_graaczy = []
        try:
            c = json.loads(data)['type']

            # wyslanie informacji o planszy, jaka pozycje ma zajac gracz, o pozycjach inn
            if c == "GET":
                self.reaction_on_get(addr, lista_graaczy)

            # wysłanie informacji o pozycji:
            #   do gracza od ktorego przyszla zwrotnej informacji ze jest ok
            #   do pozostałych informacji o tym że inny gracz wykonał ruch
            elif c == "POS":
                self.reaction_on_pos(addr, data)

            # wysłanie informacji o bombie
            elif c == "BOMB":
                player_id = self.get_player_id(addr)
                if self.game_state.check_if_player_left_bomb(player_id):
                    self.set_bomb.emit(False, addr, data)
                else:
                    self.set_bomb.emit(True, addr, data)

            # opuszczenie gry przez gracza
            elif c == "EXIT":
                pass

            elif c =="BOMB_BLOW_OK":
                self.game_state.show_board()

        except UnicodeDecodeError:
            pass
            # # print("Bład dekodowania")


    def stopConnection(self):
        self.stream.stop_stream()
        self.stream.close()
        self.s.close()










