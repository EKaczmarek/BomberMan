from Classes.Screen_codes.Activation_screen import Activation
from PyQt5.QtWidgets import QDialog
from PyQt5.QtCore import pyqtSlot
from PyQt5 import uic
import http.client
import json
import requests
import time
import sys

from PyQt5 import QtCore

qtCreatorFile = "Classes/GUI/register.ui"
Ui_Dialog, QtBaseClass = uic.loadUiType(qtCreatorFile)

class Register(QDialog, Ui_Dialog):

    back_to_login_window = QtCore.pyqtSignal(bool)
    error_connection_server_logging = QtCore.pyqtSignal(bool, str)

    def __init__(self, parent = None):
        QDialog.__init__(self, parent)
        self.setupUi(self)

        self.setWindowTitle('Bomberman')
        self.setStyleSheet("background: white")

        self.url = None

        self.button_ok.clicked.connect(self.on_button_ok_clicked)
        self.button_cancel.clicked.connect(self.on_button_cancel_clicked)
        self.button_exit.clicked.connect(self.on_button_exit_clicked)

    def set_url(self, url):
        self.url = url


    @pyqtSlot()
    def on_button_ok_clicked(self):
        email = self.lineEdit_email.text()
        nickname = self.lineEdit_nickname.text()
        password = self.lineEdit_password.text()
        repassword = self.lineEdit_repassword.text()

        if password == repassword:
            try:
                URL = str(self.url) + '/api/users/'
                # Add new player(s)
                new_player = {
                    'nickname': nickname,
                    'email': email,
                    'password': password,
                }
                # new_player put into list, because POST accepts list of players
                response = requests.post(URL, json=[new_player], timeout=1)
                if response.ok:
                    print("player added: {}".format(new_player['nickname']))
                    print()

                    if self.label.text() is "":
                        self.label.setText("Player added")
                        self.label.setStyleSheet('color: green')
                else:
                    print("Player not added")
                    if self.label.text() is "":
                        self.label.setText("Player not added")
                        self.label.setStyleSheet('color: red')

            except requests.exceptions.RequestException or requests.exceptions.Timeout \
                   or requests.exceptions.HTTPError or requests.exceptions.TooManyRedirects:
                text = "Can't connect to management server"
                self.error_connection_server_logging.emit(True, text)
                print(text)

    @pyqtSlot()
    def on_button_cancel_clicked(self):
        self.back_to_login_window.emit(True)

    @pyqtSlot()
    def on_button_exit_clicked(self):
        sys.exit(0)
