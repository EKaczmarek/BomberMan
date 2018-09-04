
from PyQt5.QtWidgets import QApplication
from PyQt5.QtCore import pyqtSlot
from threading import Thread
from Classes import Server
import json
import time

class Application_server(QApplication):

    def __init__(self, *agrs, **kwargs):
        super(Application_server, self).__init__(*agrs, **kwargs)
        self.server = None


    @pyqtSlot(bool, tuple, str)
    def set_bomb_response(self, value, addr, data):
        if value:
            player_id = self.server.get_player_id(addr)

            i, j = self.server.game_state.set_bomb(addr, data, player_id)
            payload = {"type": "BOMB", "BOMB_POS": {"x": i, "y": j}, "whose_bomb": player_id}
            for key, value in self.server.dict_players.items():
                self.server.s.sendto(json.dumps(payload).encode("utf-8"), value)

            time.sleep(1.5)
            # wybuch bomby, od czasu otrzymania tego komunikatu od serwera klient efekty wybuchu
            self.server.game_state.count_where_blow(i, j)
            print("self.list_to_destroy ", self.server.game_state.list_to_destroy)
            payload = {"type": "BOMB_BLOW", "BOMB_POS": {"x": i, "y": j},
                        "ELEMENTS_BLOW": self.server.game_state.list_to_destroy}

            for key, value in self.server.dict_players.items():
                self.server.s.sendto(json.dumps(payload).encode("utf-8"), value)

            # odswiezenie swojego stanu gry
            for k in self.server.game_state.list_to_destroy:
                self.server.game_state.game[k[1]][k[0]] = 0

            # po wybuchu wyslanie info kto zginal
            list_dead_players = self.server.game_state.handle_bombs(j, i)
            dictionary_dead_players = {}
            for k in list_dead_players:
                print(type(k))
                dictionary_dead_players[k] = self.server.game_state.get_player_pos(k)

            payload = {"type": "PLAYER_DEAD", "PLAYERS_POS": dictionary_dead_players}
            for key, value in self.server.dict_players.items():
                self.server.s.sendto(json.dumps(payload).encode("utf-8"), value)


        else:
            print("Gracz juz postawil bombe ", data)


    def setup(self):
        self.setup_server()
        self.server.connectWithClient()
        thread = Thread(target=self.server.listening, args=[])
        thread.start()

    def setup_server(self):
        server = Server.Server()
        self.server = server




