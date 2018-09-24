import sys
from Classes.Screen_codes.Application import Application
from Classes.CONFIG.config_services import services_config


if __name__ == "__main__":

    services_URL = 'http://' + str(services_config['IP'] + ':' + str(services_config['port']))
    # app = QApplication(sys.argv)
        # window = Login_screen()
        # window.show()
    # sys.exit(app.exec_())

    application = Application(sys.argv)
    application.setup_all_windows(services_URL)
    # application.show_login_window()
    # application.show_bad_data_window("Invalid username or password")
    # application.play_game.run_game("Rafał")
    application.show_ranking_window()

    # signals from interfaces
    application.loginWindow.logging_signal.connect(application.logging_signal_response)

    application.loginWindow.to_register_window_signal.connect(application.to_register_window_signal_response)

    application.badDataWindow.bad_data_signal.connect(application.bad_data_signal_response)

    application.gameWindow.play_signal.connect(application.play_signal_response)
    application.gameWindow.ranking_service_signal.connect(application.ranking_service_signal_response)
    application.gameWindow.options_signal.connect(application.options_signal_response)
    application.gameWindow.exit_signal.connect(application.exit_signal_response)

    application.game_over.show_main_screen_signal.connect(application.show_main_screen_response)

    application.rankingWindow.back_from_ranking_signal.connect(application.back_from_ranking_response)

    application.rankingWindow.error_connection_server_logging.connect(application.connection_server_logging_response)
    application.loginWindow.error_connection_server_logging.connect(application.connection_server_logging_response)
    application.registerWindow.error_connection_server_logging.connect(application.connection_server_logging_response)
    application.error_server.error_server_signal.connect(application.error_server_signal_response)

    application.registerWindow.back_to_login_window.connect(application.back_from_register_response)
    # signals from game

    # client received information from server
    # GET - map from server
    # POS - position of player
    application.play_game.player.button_clicked_on_pygame.connect(application.play_game.button_clicked_on_pygame_response)
    application.play_game.client.get_info_from_server.connect(application.play_game.have_map_params_response)

    # signal when player has moved
    application.play_game.player.player_has_moved.connect(application.play_game.player_has_moved_response)
    application.play_game.error_connection_server_logging.connect(application.error_server_signal_response)
    # signal when player has left bomb
    application.play_game.player.player_has_left_bomb.connect(application.play_game.player_has_left_bomb_response)

    application.play_game.game_over_for_player.connect(application.player_lost_game)

    application.play_game.player_win.connect(application.player_win_response)

    sys.exit(application.exec_())


