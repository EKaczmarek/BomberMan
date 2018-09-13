
from PyQt5.QtWidgets import QApplication
import sys
import pygame

from Classes.Screen_codes.Bad_data_screen import Bad_data
from Classes.Screen_codes.Game_screen import Game
from Classes.Screen_codes.Login_screen import Login_screen
from Classes.Screen_codes.Options_screen import Options
from Classes.Screen_codes.Ranking_screen import Ranking
from Classes.Screen_codes.Game_over_screen import Game_over
from Classes.Screen_codes.Error_server import Error_server

# TO DO register
from Classes.Screen_codes.Register_screen import Register

from Classes.Play_Game import PlayGame
from PyQt5.QtCore import pyqtSlot


class Application(QApplication):

    def __init__(self, *agrs, **kwargs):
        super(Application, self).__init__(*agrs, **kwargs)

        self.badDataWindow = None
        self.gameWindow = None
        self.loginWindow = None
        self.optionWindow = None
        self.rankingWindow = None
        self.registerWindow = None

        self.play_game = None
        self.game_over = None

        self.error_server = None

        self.URL = None

    @pyqtSlot(bool, str, str, str)
    def logging_signal_response(self, value, login, password, description):
        if value:
            print(".... logging_signal_response ", value)
            print("with login ", login)
            print("with password ", password)

            self.hide_login_window()

            self.gameWindow.get_servers(login, password)
            self.show_game_window()

            # GET

            self.set_login_on_game_window(login, password)
        else:
            self.hide_login_window()
            self.show_bad_data_window(description)

    @pyqtSlot(bool)
    def to_register_window_signal_response(self, value):
        if value:
            # print(".... bad_data_signal_response ", value)
            self.hide_login_window()
            self.show_register_window()
        else:
            print(".... bad_data_signal_response ", value)

    @pyqtSlot(bool)
    def bad_data_signal_response(self, value):
        if value:
            # print(".... bad_data_signal_response ", value)
            self.hide_bad_data_window()
            self.show_login_window()
        else:
            print(".... bad_data_signal_response ", value)

    @pyqtSlot(bool, str)
    def play_signal_response(self, value, login):
        if value:
            # print(".... play_signal_response ", value)
            self.hide_game_window()
            if self.play_game.is_running == False:
                self.play_game.run_game(login)
        else:
            print(".... play_signal_response ", value)

    @pyqtSlot(bool)
    def ranking_service_signal_response(self, value):
        if value:
            # print(".... ranking_service_signal_response ", value)
            self.hide_game_window()
            self.rankingWindow.get_scores()
            self.rankingWindow.get_left_bombs()
            self.show_ranking_window()
        else:
            print(".... ranking_service_signal_response ", value)

    @pyqtSlot(bool)
    def back_from_ranking_response(self, value):
        if value:
            self.hide_ranking_window()
            self.show_game_window()

    @pyqtSlot(bool, str)
    def connection_server_logging_response(self, value, response):
        if value:
            print(response)
            self.error_server.set_label(response)
            self.loginWindow.hide()
            self.show_error_server()

    @pyqtSlot(bool)
    def error_server_signal_response(self, value):
        if value:
            self.error_server.hide()
            self.loginWindow.show()

    @pyqtSlot(bool, str)
    def player_lost_game(self, value, scores):
        if value:
            print("player_lost_game_signal")
            # self.player.is_running = False
            # self.play_game.map_game.quit_game()
            self.show_game_over_window(scores)

    @pyqtSlot(bool)
    def options_signal_response(self, value):
        if value:
            # print(".... options_signal_response ", value)
            self.hide_game_window()
            self.show_option_window()
        else:
            print(".... options_signal_response ", value)

    @pyqtSlot(bool)
    def exit_signal_response(self, value):
        if value:
            # print(".... exit_signal_response ", value)
            self.closeAllWindows()
            #
            sys.exit()
        else:
            print(".... exit_signal_response ", value)

    @pyqtSlot(bool)
    def show_main_screen_response(self, value):
        if value:
            self.hide_game_over_window()
            self.show_game_window()

    @pyqtSlot(bool)
    def show_ranking_screen_response(self, value):
        if value:
            self.hide_game_over_window()
            self.show_ranking_window()

    def setup_all_windows(self, url):
        self.URL = url

        # REST Requests:
        # RANKING, REGISTER, LOGIN, GAME_OVER

        bad_data_window = Bad_data()
        self.setup_bad_data_window(bad_data_window)

        game_window = Game()
        self.setup_game_window(game_window)
        
        login_window = Login_screen()
        self.setup_login_window(login_window)
        self.loginWindow.set_url(self.URL)

        option_window = Options()
        self.setup_option_window(option_window)

        ranking_window = Ranking()
        self.setup_ranking_window(ranking_window)
        self.rankingWindow.set_url(self.URL)

        register_window = Register()
        self.setup_register_window(register_window)
        self.registerWindow.set_url(self.URL)

        play_game = PlayGame()
        self.setup_play_game(play_game)
        self.play_game.setup_all()

        game_over = Game_over()
        self.setup_game_over_window(game_over)
        self.game_over.set_url(self.URL)

        error_server = Error_server()
        self.error_server = error_server


    def setup_bad_data_window(self, bad_data_window):
        self.badDataWindow = bad_data_window

    def hide_bad_data_window(self):
        self.badDataWindow.hide()

    def show_bad_data_window(self, description):
        self.badDataWindow.show()
        self.badDataWindow.label_what_incorrect.setText(description)
        self.badDataWindow.label_what_incorrect.setStyleSheet('color: red')


    def setup_game_window(self, game_window):
        self.gameWindow = game_window

    def hide_game_window(self):
        self.gameWindow.hide()

    def show_game_window(self):
        self.gameWindow.show()

    def set_login_on_game_window(self, login, password):
        # set login in screens
        self.gameWindow.set_login(login, password)
        self.game_over.set_login_game_over(login, password)
        self.rankingWindow.set_login_password_ranking(login, password)


    def setup_login_window(self, login_window):
        self.loginWindow = login_window

    def hide_login_window(self):
        self.loginWindow.hide()

    def show_login_window(self):
        self.loginWindow.show()


    def setup_option_window(self, option_window):
        self.optionWindow = option_window

    def hide_option_window(self):
        self.optionWindow.hide()

    def show_option_window(self):
        self.optionWindow.show()


    def setup_ranking_window(self, ranking_window):
        self.rankingWindow = ranking_window

    def hide_ranking_window(self):
        self.rankingWindow.hide()

    def show_ranking_window(self):
        self.rankingWindow.show()


    def setup_error_server(self, error_server):
        self.error_server = error_server

    def hide_error_server(self):
        self.loginWindow.show()
        self.error_server.hide()

    def show_error_server(self):
        self.error_server.show()

    def setup_register_window(self, register_window):
        self.registerWindow = register_window

    def hide_register_window(self):
        self.registerWindow.hide()

    def show_register_window(self):
        self.registerWindow.show()

    def setup_game_over_window(self, game_over):
        self.game_over = game_over

    def hide_game_over_window(self):
        self.game_over.hide()

    def show_game_over_window(self, scores):
        self.game_over.set_values(scores)
        self.game_over.show()

    def setup_play_game(self, play_game):
        self.play_game = play_game