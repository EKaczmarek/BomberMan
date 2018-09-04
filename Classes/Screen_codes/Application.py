
from PyQt5.QtWidgets import QApplication

from Classes.Screen_codes.Activation_screen import Activation
from Classes.Screen_codes.Bad_data_screen import Bad_data
from Classes.Screen_codes.Game_screen import Game
from Classes.Screen_codes.Login_screen import Login_screen
from Classes.Screen_codes.Options_screen import Options
from Classes.Screen_codes.Ranking_screen import Ranking
# TO DO register
from Classes.Screen_codes.Register_screen import Register

from Classes.Play_Game import PlayGame
from PyQt5.QtCore import pyqtSlot


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

        self.play_game = None

    @pyqtSlot(bool, str)
    def logging_signal_response(self, value, login):
        if value:
            print(".... logging_signal_response ", value)
            print("with login ", login)
            self.hide_login_window()
            self.show_game_window()
        else:
            self.hide_login_window()
            self.show_bad_data_window()

    @pyqtSlot(bool)
    def activation_signal_response(self, value):
        if value:
            # print(".... activation_signal_response ", value)
            self.hide_login_window()
            self.show_activation_window()
        else:
            print(".... activation_signal_response ", value)

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

    @pyqtSlot(bool)
    def play_signal_response(self, value):
        if value:
            # print(".... play_signal_response ", value)
            self.hide_game_window()
            if self.play_game.is_running == False:
                self.play_game.run_game()
        else:
            print(".... play_signal_response ", value)

    @pyqtSlot(bool)
    def ranking_service_signal_response(self, value):
        if value:
            # print(".... ranking_service_signal_response ", value)
            self.hide_game_window()
            self.show_ranking_window()
        else:
            print(".... ranking_service_signal_response ", value)

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
            # TO DO
            # close whole application
        else:
            print(".... exit_signal_response ", value)

    def setup_all_windows(self):        
        activation_window = Activation()
        self.setup_activation_window(activation_window)
        
        bad_data_window = Bad_data()
        self.setup_bad_data_window(bad_data_window)

        game_window = Game()
        self.setup_game_window(game_window)
        
        login_window = Login_screen()
        self.setup_login_window(login_window)

        option_window = Options()
        self.setup_option_window(option_window)

        ranking_window = Ranking()
        self.setup_ranking_window(ranking_window)

        register_window = Register()
        self.setup_register_window(register_window)

        play_game = PlayGame()
        self.setup_play_game(play_game)
        self.play_game.setup_all()

    def setup_activation_window(self, activation_window):
        self.activationWindow = activation_window

    def hide_activation_window(self):
        self.activationWindow.hide()

    def show_activation_window(self):
        self.activationWindow.show()


    def setup_bad_data_window(self, bad_data_window):
        self.badDataWindow = bad_data_window

    def hide_bad_data_window(self):
        self.badDataWindow.hide()

    def show_bad_data_window(self):
        self.badDataWindow.show()


    def setup_game_window(self, game_window):
        self.gameWindow = game_window

    def hide_game_window(self):
        self.gameWindow.hide()

    def show_game_window(self):
        self.gameWindow.show()


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

    def setup_register_window(self, register_window):
        self.registerWindow = register_window

    def hide_register_window(self):
        self.registerWindow.hide()

    def show_register_window(self):
        self.registerWindow.show()

    def setup_play_game(self, play_game):
        self.play_game = play_game