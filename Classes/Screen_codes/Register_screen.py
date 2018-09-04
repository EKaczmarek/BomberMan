from Classes.Screen_codes.Activation_screen import Activation
from PyQt5.QtWidgets import QDialog
from PyQt5.QtCore import pyqtSlot
from PyQt5 import uic
import http.client
import json
import requests

qtCreatorFile = "Classes/GUI/register.ui"
Ui_Dialog, QtBaseClass = uic.loadUiType(qtCreatorFile)

class Register(QDialog, Ui_Dialog):


    def __init__(self, parent = None):
        QDialog.__init__(self, parent)
        self.setupUi(self)

        self.setWindowTitle('Bomberman')
        self.setStyleSheet("background: white")

        self.button_ok.clicked.connect(self.on_button_ok_clicked)
        self.button_cancel.clicked.connect(self.on_button_cancel_clicked)
        self.button_exit.clicked.connect(self.on_button_exit_clicked)

    @pyqtSlot()
    def on_button_ok_clicked(self):

        email = self.lineEdit_email.text()
        nickname = self.lineEdit_nickname.text()
        password = self.lineEdit_password.text()
        repassword = self.lineEdit_repassword.text()

        if password == repassword:
            URL = 'http://192.168.43.102:8080/api/users/'
            # Add new player(s)
            new_player = {
                'nickname': nickname,
                'email': email,
                'password': password,
            }
            # new_player put into list, because POST accepts list of players
            response = requests.post(URL, json=[new_player])
            if response.ok:
                print("player added: {}".format(new_player['nickname']))
                print()
            else:
                print("Player not added")

            """conn.request('POST', '/users', params, headers)
            r1 = (conn.getresponse())
            # print(r1.status)
            # print(r1.read())
            if(r1.status == 201):
                self.activ = Activation(nickname)
                self.activ.show()
            if(r1.status == 409):
                print("Dane juz istnieja w bazie")"""

    @pyqtSlot()
    def on_button_cancel_clicked(self):
        self.close()

    @pyqtSlot()
    def on_button_exit_clicked(self):
        sys.exit(self.app.exec_())
