import socket
from Classes import Game_state as gs
from threading import Thread
import time


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
                    self.sending_to_client(data, addr)

            except ConnectionRefusedError as err:
                print(err)
                print("Bład połączenia")
                break

    def sending_to_client(self, data, addr):

        try:
            data = data.decode("utf-8")
            # sending board to player
            if (data[0:3] == "GET"):
                self.dict_players[self.player_nr] = addr
                print("Gracze: " + str(self.dict_players))
                print("Otrzymano GET")
                board = "WWWWWWWWWWWWWWWW    BB       WW W W WBW W W WW       B     WWBW W W W W W WW    BBB    BBWW W W W W W WBWW      BB BB  WW W W W W W W WW             WW W W W W W W WW             WW W W W W W W WW             WWWWWWWWWWWWWWWW"
                self.game_state.set_board(board)
                player_position = "x1y1"
                self.s.sendto(("GET " + player_position + board).encode("utf-8"), addr)
                self.player_nr += 1

                print("Wyslano plansze")

            # sending data about position to all
            if (data[0:1] == "P"):
                print("Otrzymano pozycje od gracza " + addr[0] + " w postaci: " + data)
                self.game_state.update_player_position(addr[0], data)
                self.s.sendto(data.encode("utf-8"), addr)

            # sending data about bombs to all
            if (data[0:1] == "B"):
                print("Otrzymano info o pozostawionej bombie od " + addr[0] + " w postaci: ", data)
                self.game_state.set_bomb(addr[0], data)
                print("Lista do wybuchu: " + str(self.game_state.list_to_destroy))
                self.s.sendto((data + " l" + str(self.game_state.list_to_destroy)).encode("utf-8"), addr)
                self.game_state.list_to_destroy = []

            # request to check if player is dead
            if (data[0:1] == "D"):
                print("Otrzymano prosbe o sprawdzzenie czy gracz " + addr[0] + " zginal: ")
                answer = self.game_state.check_is_player_dead(addr[0])
                print("Gracz zginął: " + str(answer))
                self.s.sendto(("D " + str(answer)).encode("utf-8"), addr)

            # player has left game
            if (data[0:1] ==  "EXIT"):
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

#thread_other_players = Thread(target=serwer.send_players_pos, args = [])
#thread_other_players.start()
