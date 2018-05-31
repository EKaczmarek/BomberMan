import pyaudio
import socket
#from JaroEliCall.src.validation import Validator


#class Client(Validator):
class Client:
    FORMAT = pyaudio.paInt16
    CHUNK = 1024
    WIDTH = 1
    CHANNELS = 1
    RATE = 8000
    RECORD_SECONDS = 15
    FACTOR = 2

    #def __init__(self, priv, publ):

    def __init__(self):
        print("Inicjalizacja klasy Client")


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

        print("Czekam na odpowiedź od serwera ")

    def wait4Response(self):
        while True:
            try:
                print("Oczekiwanie....")
                data, addr2 = self.s.recvfrom(self.size)
                data = data.decode("utf-8")
                print("DAne: ", data[0:3])
                if(data[0:3] == "GET"):
                    return data[4::]
                elif(data[0:1] == "P"):
                    return data[2::]

            except ConnectionRefusedError:
                print("Blad przy otrzymywaniu odp od serwera")



    def closeConnection(self):
        self.stream.stop_stream()
        self.stream.close()
        self.s.close()


