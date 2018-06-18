import os.path
from PyQt5.QtWidgets import QMainWindow
from PyQt5.QtCore import pyqtSlot
from PyQt5 import uic
from pymongo import MongoClient
from Classes.Screen_codes.Game_screen import Game
from Classes.Screen_codes.Bad_data_screen import Bad_data
from Classes.Screen_codes.Register_screen import Register
import http.client
import hashlib
import sys
from Classes.Screen_codes.Activation_screen import Activation

import json
qtCreatorFile = os.path.join("Classes", "GUI", "login.ui")
Ui_MainWindow, QtBaseClass = uic.loadUiType(qtCreatorFile)


class MyEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, (bytes, bytearray)):
            return obj.decode("ASCII") # <- or any other encoding of your choice
        # Let the base class default method raise the TypeError
        return json.JSONEncoder.default(self, obj)


class Login_screen(QMainWindow, Ui_MainWindow):
    def __init__(self, parent = None):
        QMainWindow.__init__(self, parent)
        self.setupUi(self)

        self.connectWithMongo()
        self.setWindowTitle('Bomberman')
        self.setStyleSheet("background: white")

        self.button_ok.clicked.connect(self.on_button_ok_clicked)
        self.button_register.clicked.connect(self.on_register_button_clicked)
        self.button_exit.clicked.connect(self.on_exit_button_clicked)

    def connectWithMongo(self):
        os.startfile("C:/Program Files/MongoDB/Server/3.6/bin/mongod.exe")
        # pass

    def checkWithMongo(self, nick, password):
        sha_signature = hashlib.sha256(password.encode()).hexdigest()
        print(sha_signature)

        client = MongoClient('localhost', 27017)
        db = client['BomberMan']
        collection = db['Players']
        answer = ((collection.find({"nickname": nick, "password": sha_signature}).count()) == 1)
        print("answer: ", answer)
        if (answer): return 1
        else: return 0

    def check_if_activated(self, nickname, data):
        print("typ: ", type(data))
        print(data)
        obj = json.loads(data)

        print("dla nazwy usera: ", str(nickname), obj[nickname]['activated'])
        return obj[nickname]['activated']



    @pyqtSlot()
    def on_button_ok_clicked(self):
        conn = http.client.HTTPConnection("localhost", 8080)
        conn.request("GET", "/users")
        r1 = (conn.getresponse())
        json_users = r1.read()

        nickname = self.lineEdit_nickname.text()
        password = self.lineEdit_password.text()
        print(nickname, ", ", password)

        if(self.check_if_activated(nickname, json_users)):
            if (self.checkWithMongo(nickname, password)):
                self.close()
                self.g = Game()
                self.g.show()
            else:
                self.b = Bad_data()
                self.lineEdit_nickname.setText('')
                self.lineEdit_password.setText('')
                self.b.show()
        else:
            self.activ = Activation(nickname)
            self.activ.show()

    @pyqtSlot()
    def on_register_button_clicked(self):
        self.r = Register()
        self.r.show()

    @pyqtSlot()
    def on_exit_button_clicked(self):
        sys.exit(self.app.exec_())
