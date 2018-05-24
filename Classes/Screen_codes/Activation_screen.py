from PyQt5.QtWidgets import QDialog
from PyQt5.QtCore import pyqtSlot
from PyQt5 import uic

qtCreatorFile = "Classes/GUI/activation.ui"
Ui_Dialog, QtBaseClass = uic.loadUiType(qtCreatorFile)

class Activation(QDialog, Ui_Dialog):

    def __init__(self, parent = None):
        QDialog.__init__(self, parent)
        self.setupUi(self)

        self.setWindowTitle('Bomberman')
        self.setStyleSheet("background: white")

        self.button_ok.clicked.connect(self.on_button_ok_clicked)
        self.button_cancel.clicked.connect(self.on_button_cancel_clicked)


    @pyqtSlot()
    def on_button_ok_clicked(self):
        code = self.lineEdit_code.text()
        print(code)
        #self.close()

    @pyqtSlot()
    def on_button_cancel_clicked(self):
        self.close()
