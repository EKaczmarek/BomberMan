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

        params = [{'nickname': nickname, 'email': email, 'password': password}]
        params = json.dumps(params)
        print(params)
        headers = {'Content-type': 'application/json'}
        if(password == repassword):
            """url = '{0[protocol]}://{0[address]}:{0[port]}{0[process_endpoint]}'.format(
                self.config['server'])
            # logging.debug('sending to: %s', url)
            response = requests.post(url, json=processes)"""
            """
            {
                "server": {
                    "protocol": "http",
                    "address": "127.0.0.1",
                    "port": 8080,
                    "process_endpoint": "/api/process/"
                },
                "name": "name",
                "group": "group",
                "time period": {
                    "processes collecting": 30,
                    "server communication": 60
                }
            }"""
            # https://github.com/Irsutoro/Sauron/blob/nazgul/src/nazgul/config.json

            conn = http.client.HTTPConnection('localhost', 8080)
            conn.request('POST', '/users', params, headers)
            r1 = (conn.getresponse())
            print(r1.status)
            print(r1.read())
            if(r1.status == 201):
                self.activ = Activation(nickname)
                self.activ.show()
            if(r1.status == 409):
                print("Dane juz istnieja w bazie")

    @pyqtSlot()
    def on_button_cancel_clicked(self):
        self.close()

    @pyqtSlot()
    def on_button_exit_clicked(self):
        sys.exit(self.app.exec_())
