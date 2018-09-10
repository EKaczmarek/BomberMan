import sys
from Classes.Screen_codes.Application import Application

if __name__ == "__main__":

    URL = 'http://192.168.43.102:8080/api/users/'
    # app = QApplication(sys.argv)
    # window = Login_screen()
    # window.show()
    # sys.exit(app.exec_())

    application = Application(sys.argv)
    application.setup_all_windows(URL)
    application.show_login_window()
    #application.play_game.run_game("Ela")
    # application.show_ranking_window()

    # signals from interfaces
    application.loginWindow.logging_signal.connect(application.logging_signal_response)
    application.loginWindow.activation_signal.connect(application.activation_signal_response)

    application.loginWindow.to_register_window_signal.connect(application.to_register_window_signal_response)

    application.badDataWindow.bad_data_signal.connect(application.bad_data_signal_response)

    application.gameWindow.play_signal.connect(application.play_signal_response)
    application.gameWindow.ranking_service_signal.connect(application.ranking_service_signal_response)
    application.gameWindow.options_signal.connect(application.options_signal_response)
    application.gameWindow.exit_signal.connect(application.exit_signal_response)

    application.game_over.show_main_screen_signal.connect(application.show_main_screen_response)

    application.rankingWindow.back_from_ranking_signal.connect(application.back_from_ranking_response)


    # signals from game

    # client received information from server
    # GET - map from server
    # POS - position of player
    application.play_game.client.get_info_from_server.connect(application.play_game.have_map_params_response)

    # signal when player has moved
    application.play_game.player.player_has_moved.connect(application.play_game.player_has_moved_response)

    # signal when player has left bomb
    application.play_game.player.player_has_left_bomb.connect(application.play_game.player_has_left_bomb_response)

    application.play_game.game_over_for_player.connect(application.player_lost_game)


    sys.exit(application.exec_())


