import sys
from PyQt5.QtCore import pyqtSlot
from PyQt5.QtWidgets import QApplication, QDialog
from PyQt5.uic import loadUi


class Life2Code(QDialog):
    def __init__(self):
        super(Life2Code, self).__init__()
        loadUi('game.ui',self)
        self.setWindowTitle('BomberMAN')
        self.pushButton.clicked.connect(self.on_pushButton_clicked)

    @pyqtSlot()
    def on_pushButton_clicked(self):
        self.label1.setText('Czas rozgrywki: ')


app =QApplication(sys.argv)
widget = Life2Code()
widget.show()
sys.exit(app.exec_())



