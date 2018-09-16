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

    @pyqtSlot(bool, int, int)
    def game_over_response(self, value, player_id, place):
        if value:
            self.server.set_place_to_player(player_id, place)

            print("GAME OVER ")
            print(self.server.info_about_players)
            self.server.send_info_to_client_game_over(self.server.info_about_players, player_id)

            self.server.send_info_to_db(self.server.info_about_players)

            answer = self.server.game_state.how_many_players_left()
            print("players left ", answer)

            if answer == 1:
                id_winner = self.server.game_state.get_winner_id()
                self.server.send_info_to_client_winner(self.server.info_about_players, id_winner)



    def set_bomb_thread(self, addr, data):
        # print("begin set bomb response")
        player_id = self.server.get_player_id(addr)
        answer = self.server.game_state.player_can_leave_bomb(player_id)

        if answer is True:
            self.server.add_bomb_to_player(player_id)

            i, j = self.server.game_state.set_bomb(addr, data, player_id)
            payload = {"type": "BOMB", "BOMB_POS": {"x": i, "y": j}, "whose_bomb": player_id}
            for key, value in self.server.dict_players.items():
                self.server.s.sendto(json.dumps(payload).encode("utf-8"), value)

            time.sleep(2)
            # wybuch bomby, od czasu otrzymania tego komunikatu od serwera klient efekty wybuchu
            range_of_bomb = self.server.game_state.get_range_of_bomb(player_id)
            self.server.game_state.count_where_blow(i, j, range_of_bomb)

            # po wybuchu wyslanie info kto zginal
            list_dead_players = self.server.game_state.handle_bombs(j, i, self.server.game_state.list_to_destroy)

            if list_dead_players == []:
                x_player, y_player = self.server.game_state.get_player_pos(player_id)
                for i in self.server.game_state.list_to_destroy:
                    if i[0] == x_player and i[1] == y_player:
                        list_dead_players.append(player_id)

            payload = {"type": "BOMB_BLOW", "BOMB_POS": {"x": i, "y": j},
                       "ELEMENTS_BLOW": self.server.game_state.list_to_destroy}

            for key, value in self.server.dict_players.items():
                self.server.s.sendto(json.dumps(payload).encode("utf-8"), value)

            # odswiezenie swojego stanu gry
            for k in self.server.game_state.list_to_destroy:
                if self.server.game_state.game[k[1]][k[0]] != 0:
                    if self.server.game_state.game[k[1]][k[0]].desc == "bomb" or self.server.game_state.game[k[1]][
                        k[0]].desc == "brick":
                        self.server.game_state.game[k[1]][k[0]] = 0
                    elif self.server.game_state.game[k[1]][k[0]].desc == "powerup":
                        if self.server.game_state.game[k[1]][k[0]].view == "brick":
                            self.server.game_state.game[k[1]][k[0]].change_view("powerup")
                        else:
                            self.server.game_state.game[k[1]][k[0]] = 0

            if list_dead_players != []:
                self.server.game_state.game_over.emit(True, player_id, self.server.game_state.place)
                self.server.game_state.place -= 1

                dictionary_dead_players = {}
                for k in list_dead_players:
                    dictionary_dead_players[k] = self.server.game_state.get_player_pos(k)


                payload = {"type": "PLAYER_DEAD", "PLAYERS_POS": dictionary_dead_players}
                for key, value in self.server.dict_players.items():
                    self.server.s.sendto(json.dumps(payload).encode("utf-8"), value)

                print("dictionary_dead_players ", dictionary_dead_players)

                self.server.game_state.remove_player_from_map(dictionary_dead_players)
                print("Usunieto gracza z planszy ")

                answer = self.server.game_state.how_many_players_left()
                print(answer)

                if answer == 1:
                    id_winner = self.server.game_state.get_winner_id()
                    self.server.send_info_to_client_winner(self.server.info_about_players, id_winner)

        # print("end set bomb response")

    @pyqtSlot(bool, tuple, str)
    def set_bomb_response(self, value, addr, data):
        if value:
            thread = Thread(target=self.set_bomb_thread, args=[addr, data,])
            thread.start()

    def setup(self):
        self.setup_server()
        self.server.connectWithClient()
        thread = Thread(target=self.server.listening, args=[])
        thread.start()

    def setup_server(self):
        server = Server.Server()
        self.server = server




