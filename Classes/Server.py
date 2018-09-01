import socket
from Classes import Game_state as gs
from threading import Thread
import json
from time import sleep
import pygame


class Server:

    dict_players = {}
    players_to_send = {}
    player_nr = 0

    def __init__(self):
        # print("Inicjalizacja klasy serwer")
        self.host = ''
        self.port = 50001
        self.size = 2048

    # połączenie z klientem
    def connectWithClient(self):
        # print("Nawiazanie polaczenia")
        try:
            self.s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            self.s.bind((self.host, self.port))
            self.s.settimeout(1)
            self.game_state = gs.Game_state()
        except ConnectionRefusedError as err:
            # print(err)
            self.s.close()

    # nasłuchiwanie przez serwer
    def listening(self):
        while True:
            try:
                # print("Czekam na kolejna wiadomosc")

                data, addr = self.s.recvfrom(self.size*2)
                # print("Otrzymalem: ", data, " od ", addr)
                if data:
                     self.sending_to_client(data.decode("utf-8"), addr)
                else:
                    continue
            except ConnectionRefusedError as err:
                # print(err)
                # print("Bład połączenia")
                break
            except socket.error:
                sleep(2)
                continue

    # obliczenie id gracza na podstawie adresu IP - porownanie z wartosciami w slowniku self.dict_players
    def get_player_id(self, addr):
        for key, value in self.dict_players.items():
            if(value == addr):
                # print("id tego gracza to: ", key)
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
        # print("Gracze: " + str(lista_graczy))
        board = "WWWWWWWWWWWWWWWW    BB       WW W W WBW W W WW       B     WWBW W W W W W WW    BBB    BBWW W W W W W WBWW      BB BB  WW W W W W W W WW             WW W W W W W W WW             WW W W W W W W WW             WWWWWWWWWWWWWWWW"
        self.game_state.set_board(board)

        # TO DO
        self.player_nr += 1
        # print("player_nr ", self.player_nr)


        # ograniczenie tutaj max 1 graczy
        self.game_state.number_players = 1;
        if self.player_nr == 1:
            for key, value in self.dict_players.items():
                payload = {"type": "GET",
                           "status": 200, key: self.players_to_send[key],
                           "players": self.players_to_send,
                           "board": board}
                # print("Do wyslania: ", self.players_to_send)
                self.s.sendto((json.dumps(payload)).encode("utf-8"), value)
                # print("Wyslano")
                x = self.players_to_send[key]["x"]
                y = self.players_to_send[key]["y"]
                self.game_state.update_player_position(key, (x, y))

    def reaction_on_pos(self, addr, data):
        id = self.get_player_id(addr)
        print("ID GRACZA: ", id)
        # # print(self.dict_players[self.player_nr] + " " + addr)
        print("Otrzymano pozycje od gracza " + str(addr[0]) + " w postaci: " + data)
        data = json.loads(data)
        dx, dy = int(data["ME"]["x"]), int(data["ME"]["y"])

        last_pos = self.game_state.get_player_pos(id)
        print("last pos " + str(last_pos))

        new_pos = self.game_state.find_new_player_position(last_pos, dx, dy)
        print("new pos " + str(new_pos))

        # poniżej wymiar tablicy np x=1 y=2
        self.game_state.update_player_position(id, (new_pos[0], new_pos[1]))

        data = {"type": "POS", id: {"x": new_pos[0], "y": new_pos[1]}}
        self.s.sendto(json.dumps(data).encode("utf-8"), addr)
        print("Wyslano ", str(data) + " do " + str(addr))

        data = {"type": "UPDATE_POS", id: {"x": new_pos[0], "y": new_pos[1]}}

        self.game_state.show_board()
        for i, k in self.dict_players.items():
            if i != id:
                self.s.sendto(json.dumps(data).encode("utf-8"), self.dict_players[i])
                print("Wysylam: " + str(data) + " do " + str(self.dict_players[i]))

    def reaction_on_bomb(self, addr, data):

        print("Otrzymano info o pozostawionej bombie od " + addr[0] + " w postaci: ", data)
        player_id = self.get_player_id(addr)

        i, j = self.game_state.set_bomb(addr, data, player_id)

        payload = {"type": "BOMB", "BOMB_POS": {"x": i, "y": j}, "whose_bomb": player_id}
        for key, value in self.dict_players.items():
            self.s.sendto(json.dumps(payload).encode("utf-8"), value)
            print("Wyslano ", payload)


        # print("Lista do wybuchu: " + str(self.game_state.list_to_destroy))
        self.game_state.show_board()



    # wysylanie informacji do klienta na podstawie otrzymanej wiadomosci
    def sending_to_client(self, data, addr):
        try:
            received = json.loads(data)
            # print(received)
            # print(type(received))
            c = (received['type'])
            lista_graczy = []

            # wyslanie informacji o planszy, jaka pozycje ma zajac gracz, o pozycjach inn
            if c == "GET":
                self.reaction_on_get(addr, lista_graczy)

            # wysłanie informacji o pozycji:
            #   do gracza od ktorego przyszla zwrotnej informacji ze jest ok
            #   do pozostałych informacji o tym że inny gracz wykonał ruch
            elif c == "POS":
                self.reaction_on_pos(addr, data)

            # wysłanie informacji o bombie
            if c == "BOMB":
               self.reaction_on_bomb(addr, data)

            # aktywacja użytkownika
            if c == "MONGO":
                pass
                # print("Otrzymano komunikat dotyczacy bazy mongo of "+ addr[0])

            # opuszczenie gry przez gracza
            if c == "EXIT":
                # print("Otrzymano info o wyjsciu z gry gracza " + addr[0])
                self.game_state.kill_player(addr[0])

        except UnicodeDecodeError:
            pass
            # print("Bład dekodowania")

    def stopConnection(self):
        self.stream.stop_stream()
        self.stream.close()
        self.s.close()


serwer = Server()
serwer.connectWithClient()
thread = Thread(target=serwer.listening, args=[])
thread.start()

