import socket


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
            print(err)
            self.s.close()

    def sendMessage(self, data):
        print(data)
        try:
            self.s.send(data.encode("utf-8"))
        except ConnectionRefusedError as err:
            print(err)

    def get_board_player_pos(self):
        self.sendMessage("GET")
        lev = self.wait4Response()
        return lev[0:4], map(''.join, zip(*[iter(lev[4::])]*15))

    def get_position_begin(self, data):
        print("Pozycja poczatkowa gracza "+ data)

    def wait4Response(self):
        while True:
            try:
                print("Oczekiwanie....")
                data, addr2 = self.s.recvfrom(self.size)
                data = data.decode("utf-8")
                print("Dane: ", data)
                if(data[0:3] == "GET"):
                    self.get_position_begin(data[4:8])
                    return data[4::]
                elif(data[0:1] == "P"):
                    return data[2::]
                elif(data[0:1] == "B"):
                    res = data.split(" l")
                    for i in res:
                        print(i)
                    list_to_destroy = eval(res[1])
                    print("list_to_destroy " + str(list_to_destroy))
                    return list_to_destroy
                elif(data[0:1] == "D"):
                    print("dane zwrocone do klienta " + data[2::])
                    return data[2::]

            except ConnectionRefusedError:
                print("Blad przy otrzymywaniu odp od serwera")

    def listening(self):
        print("Zaczalem sluchac na wiadomosc od serwera")
        while 1:
            try:
                packet, address = self.s.recvfrom(self.size)
                if packet:
                    packet = packet.decode("utf-8")
                    print("wiadomosc odebrana", packet)

                    if packet[0:1] == "P":
                        if(packet[0:2] != "P "):
                            print("Otrzymano info o pozycji innego klienta")
                else:
                    continue
            except ConnectionRefusedError as err:
                print(err)

    def closeConnection(self):
        self.stream.stop_stream()
        self.stream.close()
        self.s.close()


