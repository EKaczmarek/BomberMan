import socket
from Classes import Game_state as gs
from threading import Thread
import time
import json
from time import sleep

class Server:

    dict_players = {}
    players_to_send = {}
    player_nr = 0

    def __init__(self):
        print("Inicjalizacja klasy serwer")
        self.host = ''
        self.port = 50001
        self.size = 2048

    # połączenie z klientem
    def connectWithClient(self):
        print("Nawiazanie polaczenia")
        try:
            self.s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            self.s.bind((self.host, self.port))
            self.s.settimeout(1)
            self.game_state = gs.Game_state()
        except ConnectionRefusedError as err:
            print(err)
            self.s.close()

    # nasłuchiwanie przez serwer
    def listening(self):
        while True:
            try:
                print("Czekam na kolejna wiadomosc")
                data, addr = self.s.recvfrom(self.size*2)
                print("Otrzymalem: ", data, " od ", addr)
                if data:
                    self.sending_to_client(data.decode("utf-8"), addr)
                else:
                    continue
            except ConnectionRefusedError as err:
                print(err)
                print("Bład połączenia")
                break
            except socket.error:
                sleep(2)
                continue


    # obliczenie id gracza na podstawie adresu IP - porownanie z wartosciami w slowniku self.dict_players
    def get_player_id(self, addr):
        for key, value in self.dict_players.items():
            if(value == addr):
                print("id tego gracza to: ", key)
                return key

    # wysylanie informacji do klienta na podstawie otrzymanej wiadomosci
    def sending_to_client(self, data, addr):
        try:
            received = json.loads(data)
            print(received)
            print(type(received))
            c = (received['type'])
            lista_graczy = []

            # wyslanie informacji o planszy, jaka pozycje ma zajac gracz, o pozycjach inn
            if (c == "GET"):

                self.dict_players[self.player_nr] = addr
                if (self.player_nr == 0):
                    self.player_pos = {"x":1, "y": 1}
                elif(self.player_nr == 1):
                    self.player_pos =  {"x": 13, "y": 1}
                elif (self.player_nr == 2):
                    self.player_pos = {"x": 1, "y": 13}
                elif (self.player_nr == 3):
                    self.player_pos = {"x": 13, "y": 13}


                self.players_to_send[self.player_nr] = self.player_pos
                lista_graczy.append(self.dict_players)
                print("Gracze: " + str(lista_graczy))
                board = "WWWWWWWWWWWWWWWW    BB       WW W W WBW W W WW       B     WWBW W W W W W WW    BBB    BBWW W W W W W WBWW      BB BB  WW W W W W W W WW             WW W W W W W W WW             WW W W W W W W WW             WWWWWWWWWWWWWWWW"
                self.game_state.set_board(board)
                self.player_nr += 1
                print("player_nr ", self.player_nr)
                # ograniczenie tutaj max 1 graczy
                if(self.player_nr == 1):
                    for key, value in self.dict_players.items():
                        payload = {"type": "GET", "status": 200, key: self.players_to_send[key], "players": self.players_to_send,
                                   "board": board}
                        print("Do wyslania: ", self.players_to_send)
                        self.s.sendto((json.dumps(payload)).encode("utf-8"), value)
                        print("Wyslano")
                        x = self.players_to_send[key]["x"]
                        y = self.players_to_send[key]["y"]
                        self.game_state.update_player_position(key, (x,y))

            # wysłanie informacji o pozycji:
            #   do gracza od ktorego przyszla zwrotnej informacji ze jest ok
            #   do pozostałych informacji o tym że inny gracz wykonał ruch
            elif (c == "POS"):
                id = self.get_player_id(addr)
                print("ID GRACZA: ", id)
                # print(self.dict_players[self.player_nr] + " " + addr)
                print("Otrzymano pozycje od gracza " + str(addr[0]) + " w postaci: " + data)
                data = json.loads(data)
                x, y = int(data["ME"]["x"]), int(data["ME"]["y"])
                self.game_state.update_player_position(id, (x,y))
                print("Wysyalnie do innych graczy info o pozycji gracza " + str(data))
                self.s.sendto(json.dumps(data).encode("utf-8"), addr)
                data = {"type": "UPDATE_POS", id: {"x": int(data["ME"]["x"]), "y": int(data["ME"]["y"])}}
                for i, k in self.dict_players.items():
                    if(i != id):
                        print("Wysylam: " + str(data) + " do " + str(self.dict_players[i]))
                        self.s.sendto(json.dumps(data).encode("utf-8"), self.dict_players[i])

            # wysłanie informacji o bombie
            if (c == "BOMB"):
                print("Otrzymano info o pozostawionej bombie od " + addr[0] + " w postaci: ", data)
                self.game_state.set_bomb(addr[0], data)
                print("Lista do wybuchu: " + str(self.game_state.list_to_destroy))
                payload = {'type': 'LIST_TO_BLOW', 'LIST': self.game_state.list_to_destroy}
                self.s.sendto(json.dumps(payload).encode("utf-8"), addr)

            # prośba o sprawdzenie czy gracz zginął
            if (c == "D"):
                print("Otrzymano prosbe o sprawdzzenie czy gracz " + addr[0] + " zginal: ")
                answer = self.game_state.check_is_player_dead(addr[0])
                print("Gracz zginął: " + str(answer))
                payload = {'type': 'D', 'DEAD': False }
                self.s.sendto(json.dumps(payload).encode("utf-8"), addr)

            # aktywacja użytkownika
            if(c == "MONGO"):
                print("Otrzymano komunikat dotyczacy bazy mongo of "+ addr[0])

            # opuszczenie gry przez gracza
            if (c ==  "EXIT"):
                print("Otrzymano info o wyjsciu z gry gracza " + addr[0])
                self.game_state.kill_player(addr[0])

        except UnicodeDecodeError:
            print("Bład dekodowania")

    def stopConnection(self):
        self.stream.stop_stream()
        self.stream.close()
        self.s.close()


serwer = Server()
serwer.connectWithClient()
thread = Thread(target=serwer.listening, args=[])
thread.start()
