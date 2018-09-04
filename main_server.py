import sys
from Classes.Screen_codes.Application_server import Application_server


if __name__ == "__main__":

    # app = QApplication(sys.argv)
    # window = Login_screen()
    # window.show()
    # sys.exit(app.exec_())

    application = Application_server(sys.argv)
    print("Uruchomiono server")
    application.setup()

    application.server.set_bomb.connect(application.set_bomb_response)

    sys.exit(application.exec_())


