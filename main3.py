from PyQt5.QtWidgets import QApplication
from Classes.Login_screen import Login_screen
from Classes.Player import Player
import sys


if __name__ == "__main__":
    RED = (255, 0, 0)
    GREEN = (0, 255, 0)
    BLUE = (0, 0, 255)

    """app = QApplication(sys.argv)
    window = Login_screen()
    window.show()
    sys.exit(app.exec_())"""

    # powyzej do zakomentowania
    # ponizej odkomentowania
    p = Player(50, 1000, RED)

    # p1 = Player(1000, 50, 50002)



