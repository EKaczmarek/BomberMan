import pyaudio
import socket
#from JaroEliCall.src.validation import Validator
import threading

class Client:
    def __init__(self):
        print("Inicjalizacja klasy Client")


    def connectToSerwer(self, host):
        # ipadres serwera
        self.host = "10.160.34.83"
        self.port = 50001
        self.size = 2048

        try:
            self.s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            self.s.connect((self.host, self.port))
            self.sendMessage("GET")

        except ConnectionRefusedError as err:
            print(err)
            self.s.close()

    def sendMessage(self, data):
        print(data)
        try:
            self.s.send(data.encode("utf-8"))
            print("Wyslano: ", data)
            ans, addr = self.s.recvfrom(self.size)
            data = ans.decode("utf-8")
            print("Dane: ", data[0:3])
            if (data[0:3] == "GET"):
                return data[4::]
            elif (data[0:3] == "POS"):
                print("Dostalem komunikat: ", data)
                return data
            else:
                return data
        except ConnectionRefusedError as err:
            print(err)
        print("Czekam na odpowiedź od serwera ")

    def listening(self):
        print("[*] Start listening")

        while True:
            print("W petli: ")
            try:
                data, addr = self.s.recvfrom(self.size)
                if data:
                  print("Dostalem: ", data)

            except ConnectionRefusedError as err:
                print(err)
                print("Bład połączenia")
                break

        print("[*] Stop listen")

    def closeConnection(self):
        self.stream.stop_stream()
        self.stream.close()
        self.s.close()


