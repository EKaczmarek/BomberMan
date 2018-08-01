from Classes.Screen_codes.Login_screen import Login_screen
import Classes.Player as p
import sys
from Classes.Screen_codes.Application import Application

if __name__ == "__main__":

    # app = QApplication(sys.argv)
    # window = Login_screen()
    # window.show()
    # sys.exit(app.exec_())

    application = Application(sys.argv)

    loginWindow = Login_screen()
    application.setupLoginWindow(loginWindow)

    application.showLoginWindow()


    # powyzej do zakomentowania

    # ponizej do odkomentowania
    # p.Player()

    sys.exit(application.exec_())


