import socket
import json
from time import sleep
from threading import Thread
from PyQt5 import QtCore
from PyQt5.QtCore import pyqtSlot
from PyQt5.QtWidgets import QDialog
import json
import time
class Client(QtCore.QObject):

    get_map_params_from_server = QtCore.pyqtSignal(bool, str)

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


        except ConnectionRefusedError as err:
            self.server.close()

    def sendMessage(self, data):
        try:
            self.server.send(json.dumps(data).encode("utf-8"))
        except ConnectionRefusedError as err:
            pass

    """def wait4Response(self):
        while True:
            try:
                recv, addr2 = self.server.recvfrom(self.size)
                print("Dostalem: ", recv)
                data = json.loads(recv.decode("utf-8"))

                if(data["type"] == "GET"):
                    print("lololol")
                    #self.get_map_params_from_server.emit(True, str(data))
                    # return data
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
                continue"""

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
                        self.get_map_params_from_server.emit(True, str(packet))
                        time.sleep(200)
                        print("Wyemitowano sygnal")
            except ConnectionRefusedError:
                pass
        print("Koniec słuchania...")



    def closeConnection(self):
        self.server.close()




