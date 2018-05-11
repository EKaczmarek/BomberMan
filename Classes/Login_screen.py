from PyQt5.QtWidgets import QMainWindow
from PyQt5.QtCore import pyqtSlot
from PyQt5 import uic
from pymongo import MongoClient
from Classes.Game_screen import game
from Classes.Bad_data_screen import bad_data
import hashlib
import sys
import os


qtCreatorFile = "Classes\login.ui"
Ui_MainWindow, QtBaseClass = uic.loadUiType(qtCreatorFile)

class Login_screen(QMainWindow, Ui_MainWindow):
    def __init__(self, parent = None):
        QMainWindow.__init__(self, parent)
        #Ui_MainWindow.__init__(self)
        self.setupUi(self)

        self.connectWithMongo()
        self.setWindowTitle('Bomberman')
        self.setStyleSheet("background: white")

        self.button_ok.clicked.connect(self.on_button_ok_clicked)
        self.button_register.clicked.connect(self.on_register_button_clicked)
        self.button_exit.clicked.connect(self.on_exit_button_clicked)

    def connectWithMongo(self):
        os.startfile("C:/Program Files/MongoDB/Server/3.6/bin/mongod.exe")

    def checkWithMongo(self, nick, password):
        print("Weszlo")
        client = MongoClient('localhost', 27017)
        db = client['BomberMan']
        collection = db['Players']

        sha_signature = hashlib.sha256(password.encode()).hexdigest()
        print(sha_signature)
        answer = 1
        answer = (collection.find({"login": nick, "password": sha_signature}).count()) == 1
        print(answer)
        print("lol")
        if (answer):
            return 1
        else:
            return 0

    @pyqtSlot()
    def on_button_ok_clicked(self):
        nickname = self.lineEdit_nickname.text()
        password = self.lineEdit_password.text()
        print(nickname, ", ", password)
        if (self.checkWithMongo(nickname, password)):
            self.close()
            self.g = game()
            self.g.show()
        else:
            self.b = bad_data()
            self.lineEdit_nickname.setText('')
            self.lineEdit_password.setText('')
            self.b.show()

    @pyqtSlot()
    def on_register_button_clicked(self):
        print("Rejestracja")

    @pyqtSlot()
    def on_exit_button_clicked(self):
        sys.exit(self.app.exec_())
