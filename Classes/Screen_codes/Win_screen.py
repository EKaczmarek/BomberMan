from PyQt5.QtWidgets import QDialog
from PyQt5.QtCore import pyqtSlot
from PyQt5 import uic
import http.client
import json
from PyQt5 import QtCore
import requests
import ast

qtCreatorFile = "Classes/GUI/win.ui"
Ui_Dialog, QtBaseClass = uic.loadUiType(qtCreatorFile)


class Win(QDialog, Ui_Dialog):

    show_main_screen_signal = QtCore.pyqtSignal(bool)
    player = None

    def __init__(self, parent=None):
        QDialog.__init__(self, parent)
        self.setupUi(self)

        self.url = None

        self.setWindowTitle('Bomberman')
        self.setStyleSheet("background: white")

        self.button_main.clicked.connect(self.on_button_main_clicked)

    def set_url(self, url):
        self.url = url

    def set_login_game_over(self, player, password):
        self.player = player
        self.password = password

    def set_values_win(self, scores):
        print("answer ", scores)

        self.NAME_VALUE.setText("Ela")
        self.LEFT_BOMBS_VALUE.setText(str(scores['SCORES']['bombs']))
        self.PLACE_VALUE.setText(str(scores['SCORES']['place'] + 1))

    @pyqtSlot()
    def on_button_main_clicked(self):
        self.show_main_screen_signal.emit(True)