from PyQt5.QtWidgets import QApplication
from Classes.Screen_codes.Login_screen import Login_screen
import Classes.Player as p
import sys
from Classes.Screen_codes.Ranking_screen import Ranking

if __name__ == "__main__":

    app = QApplication(sys.argv)
    window = Login_screen()
    window.show()
    sys.exit(app.exec_())

    # powyzej do zakomentowania
    # ponizej odkomentowania
    # p.Player(500, 50)



