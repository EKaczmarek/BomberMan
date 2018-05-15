import socket
# from validation import Validator


class Server:

    def __init__(self):
        print("Inicjalizacja klasy Server")

    def connectWithClient(self):
        print("Nawiazanie polaczenia")
        self.host = ''
        self.port = 50001
        self.size = 2048

        try:
            self.s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            self.s.bind((self.host, self.port))
        except ConnectionRefusedError as err:
            print(err)
            self.s.close()

    def sendM(self, message):
        self.s.connect((self.host, self.port))
        self.s.send(message.encode("utf-8"))

    def listening(self):
        print("[*] Start listen")

        self.dict_players = {}
        while True:
            try:
                data, addr = self.s.recvfrom(self.size)
                if data:
                    try:
                        data = data.decode("utf-8")
                        if (data[0:3] == "GET"):
                            print("Otrzymano GET ", addr[0], " ", addr[1])
                            board = "WWWWWWWWWWWWWWWW    BB       WW W W WBW W W WW       B     WWBW W W W W W WW    BBB    BBWW W W W W W WBWW      BB BB  WW W W W W W W WW             WW W W W W W W WW             WW W W W W W W WW             WWWWWWWWWWWWWWWW"
                            self.s.sendto(("GET " + board).encode("utf-8"), addr)
                        elif (data[0:3] == "POS"):
                            frames = data.split(" ")
                            self.dict_players[addr] = (frames[1], frames[1])
                            for key, values in self.dict_players.items():
                                print("Pozycja gracza o IP " + addr[0] + ": ", frames[1], frames[2])
                                print(key, " ", values)
                                self.s.sendto((data).encode("utf-8"), key)

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
serwer.listening()
