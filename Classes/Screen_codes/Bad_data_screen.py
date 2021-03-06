from PyQt5.QtWidgets import QDialog
from PyQt5.QtCore import pyqtSlot
from PyQt5 import uic
from PyQt5 import QtCore


qtCreatorFile = "Classes/GUI/bad_data.ui"
Ui_Dialog, QtBaseClass = uic.loadUiType(qtCreatorFile)

class Bad_data(QDialog, Ui_Dialog):

    bad_data_signal = QtCore.pyqtSignal(bool)

    def __init__(self, parent = None):
        QDialog.__init__(self, parent)
        self.setupUi(self)

        self.setWindowTitle('Bomberman')
        self.setStyleSheet("background: white")

        self.button_ok.clicked.connect(self.on_button_ok_clicked)

    @pyqtSlot()
    def on_button_ok_clicked(self):
        self.bad_data_signal.emit(True)

