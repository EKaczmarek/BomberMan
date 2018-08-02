import Classes.Player as p
import sys
from Classes.Screen_codes.Application import Application

if __name__ == "__main__":

    # app = QApplication(sys.argv)
    # window = Login_screen()
    # window.show()
    # sys.exit(app.exec_())

    application = Application(sys.argv)
    application.setup_all_windows()
    application.show_login_window()


    # signals from interfaces
    application.loginWindow.logging_signal.connect(application.logging_signal_response)
    application.loginWindow.activation_signal.connect(application.activation_signal_response)

    application.badDataWindow.bad_data_signal.connect(application.bad_data_signal_response)

    application.gameWindow.play_signal.connect(application.play_signal_response)
    application.gameWindow.ranking_service_signal.connect(application.ranking_service_signal_response)
    application.gameWindow.options_signal.connect(application.options_signal_response)
    application.gameWindow.exit_signal.connect(application.exit_signal_response)


    # signals from game
    application.play_game.client.get_map_params_from_server.connect(application.play_game.have_map_params)

    # powyzej do zakomentowania

    # ponizej do odkomentowania
    # p.Player()

    sys.exit(application.exec_())


