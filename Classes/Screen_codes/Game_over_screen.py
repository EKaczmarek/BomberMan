from PyQt5.QtWidgets import QDialog
from PyQt5.QtCore import pyqtSlot
from PyQt5 import uic
import http.client
import json
from PyQt5 import QtCore
import requests

qtCreatorFile = "Classes/GUI/game_over.ui"
Ui_Dialog, QtBaseClass = uic.loadUiType(qtCreatorFile)


class Game_over(QDialog, Ui_Dialog):

    show_main_screen_signal = QtCore.pyqtSignal(bool)
    player = None

    def __init__(self, parent=None):
        QDialog.__init__(self, parent)
        self.setupUi(self)

        URL = 'http://192.168.43.102:8080/api/users/'

        self.setWindowTitle('Bomberman')
        self.setStyleSheet("background: white")

        self.button_main.clicked.connect(self.on_button_main_clicked)

    def set_login(self, player):
        self.player = player

    def set_values(self):
        # PLAYER = 'Alice'
        PLAYER = self.player
        """response = requests.get(self.URL, params={'nickname': PLAYER})
        # Alternatively, more REST-like style:
        # response = requests.get(requests.compat.urljoin(URL, PLAYER))
        if response.ok:
            player = json.loads(response.content.decode())
            print(json.dumps(player, indent=4))
            print()"""

        self.NAME_VALUE.setText(self.player)
        self.LEFT_BOMBS_VALUE.setText("3")
        self.PLACE_VALUE.setText("2")

    @pyqtSlot()
    def on_button_main_clicked(self):
        self.show_main_screen_clicked.emit(True)