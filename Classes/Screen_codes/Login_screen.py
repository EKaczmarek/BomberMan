import os.path
from PyQt5.QtWidgets import QMainWindow
from PyQt5 import QtCore

from PyQt5.QtCore import pyqtSlot
from PyQt5 import uic
from pymongo import MongoClient
import http.client
import hashlib
import requests

import json
qtCreatorFile = os.path.join("Classes", "GUI", "login.ui")
Ui_MainWindow, QtBaseClass = uic.loadUiType(qtCreatorFile)


class Login_screen(QMainWindow, Ui_MainWindow):
    URL = 'http://localhost:8080/api/users/'

    logging_signal = QtCore.pyqtSignal(bool)
    activation_signal = QtCore.pyqtSignal(bool)

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

    def log_in(self, nick, password):
        sha_signature = hashlib.sha256(password.encode()).hexdigest()
        # print(sha_signature)

        client = MongoClient('localhost', 27017)
        db = client['bomberman']
        collection = db['players']
        answer = ((collection.find({"nickname": nick, "password": sha_signature}).count()) == 1)
        # print("answer: ", answer)

        if answer: return 1
        else: return 0

    def get_players(self):
        self.all_players = ''

        response = requests.get(self.URL)
        if response.ok:
            self.all_players = json.loads(response.content.decode())
            print(json.dumps(self.all_players, indent=4))
            print()

    def check_if_player_is_activated(self, player):
        print("check if player activated")
        response = requests.get(self.URL, params={'nickname': player})
        # Alternatively, more REST-like style:
        # response = requests.get(requests.compat.urljoin(URL, PLAYER))
        if response.ok:
            player = json.loads(response.content.decode())
            print(json.dumps(player, indent=4))
            print()
            return True
        else: return False

    @pyqtSlot()
    def on_button_ok_clicked(self):
        # TO DO
        # self.get_players()

        nickname = self.lineEdit_nickname.text()
        password = self.lineEdit_password.text()
        print(nickname, ", ", password)
        # print("all_player ", self.all_players)

        # TO DO
        # if self.check_if_player_is_activated(nickname):
        if True:
            if self.log_in(nickname, password):
                self.logging_signal.emit(True)
            else:
                self.logging_signal.emit(False)
        else:
            self.activation_signal.emit(True)

    @pyqtSlot()
    def on_register_button_clicked(self):
        pass
        # self.r = Register()
        # self.r.show()

    @pyqtSlot()
    def on_exit_button_clicked(self):
        pass
        # sys.exit(self.app.exec_())
