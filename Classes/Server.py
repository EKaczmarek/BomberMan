import socket

class Server:
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
        except ConnectionRefusedError as err:
            print(err)
            self.s.close()

    def sendM(self, message):
        self.s.connect((self.host, self.port))
        self.s.send(message.encode("utf-8"))

    def listening(self):
        print("[*] Start listen")
        while True:
            try:
                data, addr = self.s.recvfrom(self.size)
                self.host = addr[0]
                self.port = addr[1]
                if data:
                    try:
                        data = data.decode("utf-8")
                        # sending board to player
                        if (data[0:3] == "GET"):
                            print("Otrzymano GET")
                            self.sendM("GET WWWWWWWWWWWWWWWW    BB       WW W W WBW W W WW       B     WWBW W W W W W WW    BBB    BBWW W W W W W WBWW      BB BB  WW W W W W W W WW             WW W W W W W W WW             WW W W W W W W WW             WWWWWWWWWWWWWWWW")
                            print("Wyslano planse")
                        # sending data about position to all
                        if (data[0:1] == "P"):
                            print("Otrzymano pozycje od gracza " + addr[0] + " w postaci: " + data)
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
serwer.listening()
