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
import sys

qtCreatorFile = os.path.join("Classes", "GUI", "login.ui")
Ui_MainWindow, QtBaseClass = uic.loadUiType(qtCreatorFile)


class Login_screen(QMainWindow, Ui_MainWindow):

    logging_signal = QtCore.pyqtSignal(bool, str, str, str)
    to_register_window_signal = QtCore.pyqtSignal(bool)
    error_connection_server_logging = QtCore.pyqtSignal(bool, str)

    def __init__(self, parent = None):
        QMainWindow.__init__(self, parent)
        self.setupUi(self)

        self.setWindowTitle('Bomberman')
        self.setStyleSheet("background: white")

        self.url = None

        self.button_ok.clicked.connect(self.on_button_ok_clicked)
        self.button_register.clicked.connect(self.on_register_button_clicked)
        self.button_exit.clicked.connect(self.on_exit_button_clicked)

    def set_url(self, url):
        self.url = url

    def log_in(self, nickname, password):
        try:
            AUTH = requests.auth.HTTPBasicAuth(nickname, password)
            URL = str(self.url) + '/api/users/'

            response = requests.get(URL, auth=AUTH, timeout=1)
            if response.ok:
                print('Request successful; cached credentials can be reused in the future requests')
                self.logging_signal.emit(True, nickname, password, 'Request successful')
            elif response.status_code == 401:
                print('Invalid username or password (for details parse response.text)')
                self.logging_signal.emit(False, nickname, password, 'Invalid username/password')
            elif response.status_code == 403:
                print('Account not activated')
                self.logging_signal.emit(False, nickname, password, 'Account not activated')
            else:
                print('Error: {} {}'.format(response.status_code, response.reason))
        except requests.exceptions.RequestException or requests.exceptions.Timeout\
                or requests.exceptions.HTTPError or requests.exceptions.TooManyRedirects:
            text = "Can't connect to management server"
            self.error_connection_server_logging.emit(True, text)
            print(text)


    @pyqtSlot()
    def on_button_ok_clicked(self):
        nickname = self.lineEdit_nickname.text()
        password = self.lineEdit_password.text()

        self.log_in(nickname, password)

    @pyqtSlot()
    def on_register_button_clicked(self):
        self.to_register_window_signal.emit(True)

    @pyqtSlot()
    def on_exit_button_clicked(self):
        sys.exit()
