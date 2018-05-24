from PyQt5.QtWidgets import QDialog
from PyQt5.QtCore import pyqtSlot
from PyQt5 import uic
from Classes.Player import Player
from Classes.Screen_codes.Options_screen import Options
from Classes.Screen_codes.Ranking_screen import Ranking


qtCreatorFile = "Classes\GUI\game.ui"
Ui_Dialog, QtBaseClass = uic.loadUiType(qtCreatorFile)


class Game(QDialog, Ui_Dialog):
    def __init__(self, parent=None):
        QDialog.__init__(self, parent)
        self.setupUi(self)

        self.setWindowTitle('Bomberman')
        self.setStyleSheet("background: white")

        self.button_play.clicked.connect(self.on_button_play_clicked)
        self.button_ranking.clicked.connect(self.on_ranking_button_clicked)
        self.button_options.clicked.connect(self.on_options_button_clicked)
        self.button_exit.clicked.connect(self.on_exit_button_clicked)

    @pyqtSlot()
    def on_button_play_clicked(self):
        self.close()
        p = Player(500, 50)
        print("ok")

    @pyqtSlot()
    def on_ranking_button_clicked(self):
        self.rank = Ranking()
        self.rank.show()

    @pyqtSlot()
    def on_options_button_clicked(self):
        self.op = Options()
        self.op.show()

    @pyqtSlot()
    def on_exit_button_clicked(self):
        self.close()

