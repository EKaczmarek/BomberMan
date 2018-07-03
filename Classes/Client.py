import socket
import json

class Client:

    def connectToSerwer(self, host):
        # ip adres serwera
        self.host = host
        self.port = 50001
        self.size = 2048

        try:
            self.s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            self.s.connect((self.host, self.port))
        except ConnectionRefusedError as err:
            # print(err)
            self.s.close()

    def sendMessage(self, data):
        # print(data)
        try:
            self.s.send(json.dumps(data).encode("utf-8"))
        except ConnectionRefusedError as err:
            pass
            # print(err)

    def get_board_player_pos(self):
        self.sendMessage({"type": "GET"})
        level, pos = self.wait4Response()
        print("level", level)
        print("pos", pos)
        return map(''.join, zip(*[iter(level)]*15)), pos

    def get_position_begin(self, data):
        pass
        # print("Pozycja poczatkowa gracza "+"x " + str(data["x"]) + "y "+str(data["y"]))


    def wait4Response(self):
        while True:
            try:
                # print("Oczekiwanie....")
                data, addr2 = self.s.recvfrom(self.size)
                print("Dostalem: ", data)

                data = data.decode("utf-8")
                # print(data)
                data = json.loads(data)
                # print("Dane: ", data)
                """  if(data["type"] == "GET"):
                    list_of_players = []
                    self.get_position_begin(data["YOU"])
                    for key, value in data.items():
                        print(key)
                        if(key.isdigit()):
                            print("JEST INT!")
                            list_of_players.append({key: value})"""
                if(data["type"] == "GET"):
                    return data["board"], (data["YOU"]["x"], data["YOU"]["y"])
                elif(data["type"] == "POS"):
                    print("DOSTALEM POZYCJE GRACZAAAAAAAAAAAAAAAAAAAAA ", data)
                    return data["ME"]["x"], data["ME"]["y"]
                elif(data["type"] == "BOMB"):
                    list_to_destroy = (data['B'])
                    return list_to_destroy
                elif(data["type"] == "DATA"):
                    # print("dane zwrocone do klienta " + data[2::])
                    return data[2::]

                elif(data["type"] == "D"):
                    # print("Gracz nie żyje: ", data["DEAD"])
                    return data["DEAD"]
                elif(data["type"] == "LIST_TO_BLOW"):
                    return data["LIST"]
            except ConnectionRefusedError:
                pass
                # print("Blad przy otrzymywaniu odp od serwera")


    def listening(self):
        while 1:
            try:
                packet, address = self.s.recvfrom(self.size)
                if packet:
                    packet = packet.decode("utf-8")
                    packet = json.loads(packet)
                    # print("wiadomosc odebrana", packet)

                    if packet["type"]== "POS":
                        pass
                        # print("Otrzymano info o pozycji innego klienta")
                else:
                    continue
            except ConnectionRefusedError as err:
                pass
                # print(err)

    def closeConnection(self):
        self.stream.stop_stream()
        self.stream.close()
        self.s.close()


