import socket
from PyQt5 import QtCore
import json
import datetime

class Client(QtCore.QObject):

    get_info_from_server = QtCore.pyqtSignal(bool, str, str)

    def __init__(self):
        super(Client, self).__init__()
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
            # print("(*) Wyslano do serwera ", str(data))
        except ConnectionRefusedError as err:
            pass

    def send_position_update(self, player_x, player_y):
        payload = {"type": "POS", "ME": {"x": player_x, "y": player_y}}
        self.sendMessage(payload)

    def send_info_about_bomb(self, bomb_x, bomb_y):
        payload = {"type": "BOMB", "ME": {"x": bomb_x, "y": bomb_y}}
        self.sendMessage(payload)
        print(payload)

    def set_time_ping(self):
        self.time_ping = datetime.datetime.time(datetime.datetime.now())

    # wątek umożliwiający odbieranie wiadomosci o aktualizacji pozycji gracza/ bomby
    def listening(self):
        while 1:
            try:
                packet, address = self.server.recvfrom(self.size)
                if packet:
                    packet = packet.decode("utf-8")
                    packet = json.loads(packet)
                    if packet["type"] == "GET":
                        self.get_info_from_server.emit(True, str(packet), "GET")
                    elif packet["type"] == "POS":
                        self.get_info_from_server.emit(True, str(packet), "MY_POS")
                    elif packet["type"] == "UPDATE_POS":
                        self.get_info_from_server.emit(True, str(packet), "OTHERS_POS")
                    elif packet["type"] == "BOMB":
                        self.get_info_from_server.emit(True, str(packet), "BOMB")
                    elif packet["type"] == "PLAYER_DEAD":
                        self.get_info_from_server.emit(True, str(packet), "PLAYER_DEAD")
                    elif packet["type"] == "BOMB_BLOW":
                        self.get_info_from_server.emit(True, str(packet), "BOMB_BLOW")
                    elif packet["type"] == "END_GAME":
                        self.get_info_from_server.emit(True, str(packet), "END_GAME")
                    elif packet["type"] == "WINNER":
                        self.get_info_from_server.emit(True, str(packet), "WINNER")
                    elif packet["type"] == "PING":
                        self.set_time_ping()
                        print("ping ", self.time_ping)
            except ConnectionError:
                print("Brak polaczenia z serwerem ConnectionError")
            except ConnectionAbortedError:
                print("Brak polaczenia z serwerem ConnectionAbortedError")
            except ConnectionRefusedError:
                print("Brak polaczenia z serwerem ConnectionRefusedError")
            except ConnectionResetError:
                print("Brak polaczenia z serwerem ConnectionResetError")

    def close_connection(self):
        self.server.close()




