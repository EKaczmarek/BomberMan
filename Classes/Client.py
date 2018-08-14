import socket
from PyQt5 import QtCore
import json
from PyQt5.QtCore import pyqtSlot


class Client(QtCore.QObject):

    # str - packet
    # str - flag
    get_info_from_server = QtCore.pyqtSignal(bool, str, str)

    def __init__(self):
        super(Client, self).__init__()

        print("Konstruktor Klient")
        self.host = None
        self.port = None
        self.size = None
        self.server = None

    def connect_to_serwer(self, host):
        self.host = host
        self.port = 50001
        self.size = 2048

        try:
            self.server = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            self.server.connect((self.host, self.port))
        except ConnectionRefusedError:
            self.server.close()

    def sendMessage(self, data):
        try:
            self.server.send(json.dumps(data).encode("utf-8"))
            print("(*) Wyslano do serwera ", str(data))
        except ConnectionRefusedError as err:
            pass

    def send_position_update(self, player_id, player_x, player_y):
        payload = {"type": "POS", "ME": {"x": player_x, "y": player_y}}
        self.sendMessage(payload)


    # wątek umożliwiający odbieranie wiadomosci o aktualizacji pozycji gracza/ bomby
    def listening(self):
        while 1:
            try:
                print("Probuje odebrac ...")
                packet, address = self.server.recvfrom(self.size)
                if packet:
                    packet = packet.decode("utf-8")
                    packet = json.loads(packet)
                    print("Odebrałem: ", packet)
                    if packet["type"] == "GET":
                        self.get_info_from_server.emit(True, str(packet), "GET")
                    elif packet["type"] == "POS":
                        self.get_info_from_server.emit(True, str(packet), "MY_POS")
                    elif packet["type"] == "UPDATE_POS":
                        self.get_info_from_server.emit(True, str(packet), "OTHERS_POS")
            except ConnectionRefusedError:
                pass

    def close_connection(self):
        self.server.close()




