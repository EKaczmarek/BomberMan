from PyQt5.QtWidgets import QDialog
from PyQt5.QtCore import pyqtSlot
from PyQt5 import uic
import http.client
import json


qtCreatorFile = "Classes/GUI/activation.ui"
Ui_Dialog, QtBaseClass = uic.loadUiType(qtCreatorFile)

class Activation(QDialog, Ui_Dialog):

    def __init__(self, nickname, parent = None):
        QDialog.__init__(self, parent)
        self.setupUi(self)

        self.setWindowTitle('Bomberman')
        self.setStyleSheet("background: white")
        self.nick = nickname
        self.button_ok.clicked.connect(self.on_button_ok_clicked)
        self.button_cancel.clicked.connect(self.on_button_cancel_clicked)


    @pyqtSlot()
    def on_button_ok_clicked(self):
        code = self.lineEdit_code.text()

        params = [{'nickname': self.nick, 'activation_key': code}]
        params = json.dumps(params)
        headers = {'Content-type': 'application/json'}

        conn = http.client.HTTPConnection('localhost', 6060)
        conn.request('POST', '/', params, headers)

        r1 = (conn.getresponse())
        print("r1", r1.status)
        print("odp: ", r1.read())

    @pyqtSlot()
    def on_button_cancel_clicked(self):
        self.close()
