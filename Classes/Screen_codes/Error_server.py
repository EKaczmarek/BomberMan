from PyQt5.QtWidgets import QDialog
from PyQt5.QtCore import pyqtSlot
from PyQt5 import uic
from PyQt5 import QtCore


qtCreatorFile = "Classes/GUI/error_server.ui"
Ui_Dialog, QtBaseClass = uic.loadUiType(qtCreatorFile)

class Error_server(QDialog, Ui_Dialog):

    error_server_signal = QtCore.pyqtSignal(bool)

    def __init__(self, parent = None):
        QDialog.__init__(self, parent)
        self.setupUi(self)

        self.setWindowTitle('Bomberman')
        self.setStyleSheet("background: white")

        self.button_ok.clicked.connect(self.on_button_ok_clicked)

    def set_label(self, text):
        self.label.setText(text)

    @pyqtSlot()
    def on_button_ok_clicked(self):
        self.error_server_signal.emit(True)

