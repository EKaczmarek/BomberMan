from PyQt5.QtWidgets import QDialog
from PyQt5.QtCore import pyqtSlot
from PyQt5 import uic

qtCreatorFile = "Classes/GUI/options.ui"
Ui_Dialog, QtBaseClass = uic.loadUiType(qtCreatorFile)


class Options(QDialog, Ui_Dialog):

    def __init__(self, parent = None):
        QDialog.__init__(self, parent)
        self.setupUi(self)

        self.setWindowTitle('Bomberman')
        self.setStyleSheet("background: white")

        self.button_back.clicked.connect(self.on_button_back_clicked)
        self.button_apply.clicked.connect(self.on_button_apply_clicked)

    @pyqtSlot()
    def on_button_back_clicked(self):
        self.close()

    @pyqtSlot()
    def on_button_apply_clicked(self):
        pass