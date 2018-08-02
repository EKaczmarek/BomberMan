import os.path
from PyQt5.QtWidgets import QDialog
from PyQt5.QtCore import pyqtSlot
from PyQt5 import uic
from PyQt5 import QtCore


qtCreatorFile = os.path.join("Classes", "GUI", "game.ui")
Ui_Dialog, QtBaseClass = uic.loadUiType(qtCreatorFile)


class Game(QDialog, Ui_Dialog):

    play_signal = QtCore.pyqtSignal(bool)
    ranking_service_signal = QtCore.pyqtSignal(bool)
    options_signal = QtCore.pyqtSignal(bool)
    exit_signal = QtCore.pyqtSignal(bool)

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
        self.play_signal.emit(True)

    @pyqtSlot()
    def on_ranking_button_clicked(self):
        self.ranking_service_signal.emit(True)

    @pyqtSlot()
    def on_options_button_clicked(self):
        self.options_signal.emit(True)

    @pyqtSlot()
    def on_exit_button_clicked(self):
        self.exit_signal.emit(True)

