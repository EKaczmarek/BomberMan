from PyQt5.QtWidgets import QDialog, QMainWindow
from PyQt5.QtCore import pyqtSlot
from PyQt5.uic import loadUi
from PyQt5 import uic
from PyQt5.QtWidgets import QApplication
from Classes.Login_screen import Login_screen
import sys
import os


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = Login_screen()
    window.show()
    sys.exit(app.exec_())

