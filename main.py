from PyQt5.QtWidgets import QApplication
from Classes.Login_screen import Login_screen
import sys


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = Login_screen()
    window.show()
    sys.exit(app.exec_())

    # powyzej do zakomentowania
    # ponizej odkomentowania
    # p = Player(500, 50)



