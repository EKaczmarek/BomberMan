import socket
from Classes import Game_state as gs
from threading import Thread
import time
import json
import ast

class Server:

    dict_players = {}
    player_nr = 1

    def __init__(self):
        print("Inicjalizacja klasy serwer")
        self.host = ''
        self.port = 50001
        self.size = 2048

    def connectWithClient(self):
        print("Nawiazanie polaczenia")
        try:
            self.s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            self.s.bind((self.host, self.port))
            self.game_state = gs.Game_state()
        except ConnectionRefusedError as err:
            print(err)
            self.s.close()

    def listening(self):
        while True:
            try:
                print("Czekam na kolejna wiadomosc")
                data, addr = self.s.recvfrom(self.size*2)
                print("Otrzymalem: ", data, " od ", addr)
                if data:
                    self.sending_to_client(data.decode("utf-8"), addr)

            except ConnectionRefusedError as err:
                print(err)
                print("Bład połączenia")
                break

    def sending_to_client(self, data, addr):
        try:
            print(data)
            print("typek", type(data))
            received = json.loads(data)
            print(received)
            print(type(received))
            c = (received['type'])

            print(c)


            if (c == "GET"):
                self.dict_players[self.player_nr] = addr
                print("Gracze: " + str(self.dict_players))
                print("Otrzymano GET")
                board = "WWWWWWWWWWWWWWWW    BB       WW W W WBW W W WW       B     WWBW W W W W W WW    BBB    BBWW W W W W W WBWW      BB BB  WW W W W W W W WW             WW W W W W W W WW             WW W W W W W W WW             WWWWWWWWWWWWWWWW"
                self.game_state.set_board(board)

                payload = {"type": "GET", "status": 200, "YOU": {"x": 1, "y":1}, "P1": {"x":13, "y": 1}, "board": board}
                self.s.sendto((json.dumps(payload)).encode("utf-8"), addr)
                self.player_nr += 1

                print("Wyslano plansze")

            # sending data about position to all
            elif (c == "POS"):
                print("Otrzymano pozycje od gracza " + addr[0] + " w postaci: " + str(data))
                self.game_state.update_player_position(addr[0], data)
                print("Wysyalnie do innych graczy info o pozycji gracza ")
                for i in self.dict_players:
                    print(i, " ", self.dict_players[i])
                    self.s.sendto(data.encode("utf-8"), self.dict_players[i])

            # sending data about bombs to all
            if (c == "BOMB"):
                print("Otrzymano info o pozostawionej bombie od " + addr[0] + " w postaci: ", data)
                self.game_state.set_bomb(addr[0], data)
                print("Lista do wybuchu: " + str(self.game_state.list_to_destroy))
                payload = {'type': 'LIST_TO_BLOW', 'LIST': self.game_state.list_to_destroy}
                self.s.sendto(json.dumps(payload).encode("utf-8"), addr)

            # request to check if player is dead
            if (c == "D"):
                print("Otrzymano prosbe o sprawdzzenie czy gracz " + addr[0] + " zginal: ")
                answer = self.game_state.check_is_player_dead(addr[0])
                print("Gracz zginął: " + str(answer))
                payload = {'type': 'D', 'DEAD': False }
                self.s.sendto(json.dumps(payload).encode("utf-8"), addr)

            # user activation
            if(c == "MONGO"):
                print("Otrzymano komunikat dotyczacy bazy mongo of "+ addr[0])


            # player has left game
            if (c ==  "EXIT"):
                print("Otrzymano info o wyjsciu z gry gracza " + addr[0])
                self.game_state.kill_player(addr[0])

        except UnicodeDecodeError:
            print("Bład dekodowania")

    def send_players_pos(self):
        while 1:
            time.sleep(2)
            print("Slownik")
            for i in self.dict_players:
                print(i)
                for j in self.dict_players[i]:
                    print(j, ':', self.dict_players[i][j])


    def stopConnection(self):
        self.stream.stop_stream()
        self.stream.close()
        self.s.close()


serwer = Server()
serwer.connectWithClient()
thread = Thread(target=serwer.listening, args=[])
thread.start()

# thread_other_players = Thread(target=serwer.send_players_pos, args = [])
# thread_other_players.start()
