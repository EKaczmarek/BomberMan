import socket
from Classes import Game_state as gs
from threading import Thread

class Server:

    players = {}

    def __init__(self):
        print("Inicjalizacja klasy serwer")

    def connectWithClient(self):
        print("Nawiazanie polaczenia")
        self.host = ''
        self.port = 50001
        self.size = 2048
        try:
            self.s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            self.s.bind((self.host, self.port))
            self.game_state = gs.Game_state()
        except ConnectionRefusedError as err:
            print(err)
            self.s.close()

    def sendM(self, message):
        self.s.connect((self.host, self.port))
        self.s.send(message.encode("utf-8"))

    def listening(self):
        player_number = 1
        print("[*] Start listen")
        while True:
            print("Slucham")
            try:
                data, addr = self.s.recvfrom(self.size)
                print(data, " ", addr)
                if(addr not in self.players):
                    self.players[addr] = player_number
                    player_number += 1

                self.host = addr[0]
                self.port = addr[1]
                if data:
                    try:
                        data = data.decode("utf-8")
                        # sending board to player
                        if (data[0:3] == "GET"):
                            print("Otrzymano GET")
                            board = "WWWWWWWWWWWWWWWW    BB       WW W W WBW W W WW       B     WWBW W W W W W WW    BBB    BBWW W W W W W WBWW      BB BB  WW W W W W W W WW             WW W W W W W W WW             WW W W W W W W WW             WWWWWWWWWWWWWWWW"
                            self.game_state.set_board(board)
                            self.sendM("GET " + board)
                            print("Wyslano planse")

                        # sending data about position to all
                        if (data[0:1] == "P"):
                            print("Otrzymano pozycje od gracza " + addr[0] + " w postaci: " + data)
                            self.game_state.set_player_position(self.players[addr], data)
                            self.sendM(data)

                        #sending data about bombs to all
                        if(data[0:1] == "B"):
                            print("Otrzymano info o pozostawionej bombie od " + addr[0] + "w postaci: ", data)

                    except UnicodeDecodeError:
                        print("Bład dekodowania")

            except ConnectionRefusedError as err:
                print(err)
                print("Bład połączenia")
                break

        print("[*] Stop listen")

    def stopConnection(self):
        self.stream.stop_stream()
        self.stream.close()

        self.s.close()


serwer = Server()
serwer.connectWithClient()
thread = Thread(target=serwer.listening, args=[])
thread.start()

