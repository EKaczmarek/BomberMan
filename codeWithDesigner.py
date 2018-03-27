import sys
from PyQt5.QtCore import pyqtSlot
from PyQt5 import QtCore
from PyQt5.QtWidgets import QApplication, QDialog
from PyQt5.uic import loadUi
import pygame


class Life2Code(QDialog):
    def __init__(self):
        super(Life2Code, self).__init__()
        loadUi('game.ui',self)
        self.setWindowTitle('BomberMAN')
        self.menu_button.clicked.connect(self.menu_Button_clicked)
        self.exit_button.clicked.connect(self.exit_Button_clicked)


    @pyqtSlot()
    def menu_Button_clicked(self):
        self.time_label.setText('Czas rozgrywki: ')

    @pyqtSlot()
    def exit_Button_clicked(self):
        self.time_label.setText('Lol: ')



app = QApplication(sys.argv)
widget = Life2Code()
widget.show()
sys.exit(app.exec_())



