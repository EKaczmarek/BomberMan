from PyQt5.QtWidgets import QDialog
from PyQt5.QtCore import pyqtSlot
from PyQt5 import uic
from Classes.Player import Player

qtCreatorFile = "Classes\game.ui"
Ui_Dialog, QtBaseClass = uic.loadUiType(qtCreatorFile)

class game(QDialog, Ui_Dialog):

    def __init__(self, parent = None):
        QDialog.__init__(self, parent)
        self.setupUi(self)

        self.setWindowTitle('Bomberman')
        self.setStyleSheet("background: white")

        self.button_play.clicked.connect(self.on_button_play_clicked)
        self.button_ranking.clicked.connect(self.on_ranking_button_clicked)
        self.button_options.clicked.connect(self.on_options_button_clicked)


    @pyqtSlot()
    def on_button_play_clicked(self):
        self.close()
        p = Player(500, 50)
        print("ok")

    @pyqtSlot()
    def on_ranking_button_clicked(self):
        print("Ranking")

    @pyqtSlot()
    def on_options_button_clicked(self):
        print("Options")
        pass

