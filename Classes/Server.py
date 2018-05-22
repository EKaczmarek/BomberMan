import socket
# from validation import Validator
import threading

class Server:

    def __init__(self):
        print("Inicjalizacja klasy Server")
        self.dict_players = {}

    def connectWithClient(self):
        print("Nawiazanie polaczenia")
        self.host = "192.168.43.130"
        self.port = 50001
        self.size = 2048

        try:
            self.s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            self.s.bind((self.host, self.port))

        except ConnectionRefusedError as err:
            print(err)
            self.s.close()

    def send_message_to_client(self, data, addr):
        if(str(addr[0]) != ''):
            #print("Wysylanie: " + str(addr[0]) + " " + str(addr[1]))
            self.s.sendto(data.encode("utf-8"), addr)

    def listening(self):
        print("[*] Start listen")

        while True:
            print("W petli: ")
            print(self.dict_players)
            for key, values in self.dict_players.items():
                # print("Wyslanie do ", key, " ,wartosci: ", values)
                self.send_message_to_client("POS " + values, key)
                # self.host = key[0]
                # self.port = key[1]

            try:
                data, addr = self.s.recvfrom(self.size)
                if data:
                    try:
                        data = data.decode("utf-8")
                        if (data[0:3] == "GET"):
                            print("Otrzymano GET ", addr[0], " ", addr[1])
                            board = "WWWWWWWWWWWWWWWW    BB       WW W W WBW W W WW       B     WWBW W W W W W WW    BBB    BBWW W W W W W WBWW      BB BB  WW W W W W W W WW             WW W W W W W W WW             WW W W W W W W WW             WWWWWWWWWWWWWWWW"
                            data = "GET "+board
                            print("adres IP: ", addr[0], " port: ", addr[1])
                            self.host = addr[0]
                            self.port = addr[1]
                            self.dict_players[(self.host, self.port)] = " "
                            t=threading.Thread(target=self.send_message_to_client,args=(data, addr))
                            t.start()
                        elif (data[0:3] == "POS"):
                            frames = data.split(" ")
                            self.dict_players[addr] = (frames[1], frames[1])
                            for key, values in self.dict_players.items():
                                print("Pozycja gracza o IP " + addr[0] + ": ", frames[1], frames[2])
                                print(key, " ", values)
                                t = threading.Thread(target=self.send_message_to_client, args=(data, addr))
                                t.start()

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
