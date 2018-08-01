
from PyQt5.QtWidgets import QApplication


class Application(QApplication):

    def __init__(self, *agrs, **kwargs):
        super(Application, self).__init__(*agrs, **kwargs)

        self.activationWindow = None
        self.badDataWindow = None
        self.gameWindow = None
        self.loginWindow = None
        self.optionWindow = None
        self.rankingWindow = None
        self.registerWindow = None

    def setupLoginWindow(self, loginWindow):
        self.loginWindow = loginWindow

    def hideLoginWindow(self):
        self.loginWindow.hide()

    def showLoginWindow(self):
        self.loginWindow.show()
