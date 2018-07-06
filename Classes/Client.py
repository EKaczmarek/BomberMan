import socket
import json
from threading import Thread
from time import sleep

class Client:

    def connectToSerwer(self, host):
        # ip adres serwera
        self.host = host
        self.port = 50001
        self.size = 2048

        try:
            self.s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            self.s.connect((self.host, self.port))
            self.s.settimeout(1000000)
        except ConnectionRefusedError as err:
            self.s.close()

    def sendMessage(self, data):
        try:
            self.s.send(json.dumps(data).encode("utf-8"))
        except ConnectionRefusedError as err:
            pass

    def get_board_player_pos(self):
        self.sendMessage({"type": "GET"})
        data = self.wait4Response()
        # zmienna data w stylu {"type": "GET", "status": 200, 0: {"x": 1, "y": 1}, board": board}
        print("Odpowiedz na GET: ", data)

        self.my_id = 0
        for key, value in data.items():
            print(type(key))
            if(key.isdigit()):
                print(key)
                self.my_id = key

        level = data["board"]
        pos = (data[self.my_id]["x"], data[self.my_id]["y"])

        list_of_players = []

        for key, value in data.items():
            print(key)
            if (key=="players"):
                for k, v in value.items():
                    if(str(k) != str(self.my_id)):
                        list_of_players.append({k: v})


        print("plansza: ", level)
        print("moja pozycja: ", pos)
        print("inni gracze: " + str(list_of_players))

        return map(''.join, zip(*[iter(level)]*15)), pos, list_of_players


    def wait4Response(self):
        while True:
            try:
                recv, addr2 = self.s.recvfrom(self.size)
                print("Dostalem: ", recv)
                data = json.loads(recv.decode("utf-8"))

                if(data["type"] == "GET"):
                    return data
                elif(data["type"] == "POS"):
                    print("DOSTALEM POZYCJE SWOJĄ ", data)
                    return data["ME"]["x"], data["ME"]["y"]
                elif (data["type"] == "UPDATE_POS"):
                    print("DOSTALEM POZYCJE INNEGO GRACZA...")
                elif(data["type"] == "BOMB"):
                    print("DOSTALEM INFORMACJĘ O BOMBIE...")
                    list_to_destroy = (data['B'])
                    return list_to_destroy
                elif(data["type"] == "D"):
                    print("DOSTALEM INFORMACJĘ O TYM ŻE GRACZ NIE ŻYJE...")
                    # print("Gracz nie żyje: ", data["DEAD"])
                    return data["DEAD"]
                elif(data["type"] == "LIST_TO_BLOW"):
                    print("DOSTALEM LISTĘ KTÓRA WYBUCHA...")
                    return data["LIST"]
            except ConnectionRefusedError:
                pass
            except socket.error:
                sleep(1)
                continue

    # wątek umożliwiający odbieranie wiadomosci o aktualizacji pozycji gracza/ bomby
    def listening(self, toThreaad):
        while 1:
            try:
                print("Probuje odebrac ...")
                packet, address = self.s.recvfrom(self.size)
                with toThreaad.lock:
                    if packet:
                        print("Jestem zablokowany :(")
                        packet = packet.decode("utf-8")
                        packet = json.loads(packet)
                        toThreaad.users = packet
                        print(toThreaad.users)
                    else:
                        continue
            except ConnectionRefusedError as err:
                print(err)
                pass
            except socket.error:
                continue
        print("Koniec słuchania...")



    def closeConnection(self):
        self.stream.stop_stream()
        self.stream.close()
        self.s.close()




