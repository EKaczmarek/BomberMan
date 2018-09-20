from PyQt5.QtWidgets import QDialog, QTableWidgetItem
from PyQt5.QtCore import pyqtSlot
from PyQt5.QtCore import Qt
from PyQt5 import uic
from pymongo import  MongoClient
from functools import reduce
import requests
import json
from PyQt5 import QtCore

qtCreatorFile = "Classes/GUI/ranking.ui"
Ui_Dialog, QtBaseClass = uic.loadUiType(qtCreatorFile)

class Ranking(QDialog, Ui_Dialog):

    back_from_ranking_signal = QtCore.pyqtSignal(bool)
    error_connection_server_logging = QtCore.pyqtSignal(bool, str)

    def __init__(self, parent = None):
        QDialog.__init__(self, parent)
        self.setupUi(self)

        self.url = None
        self.player = None
        self.password = None

        self.setWindowTitle('Bomberman')
        self.setStyleSheet("background: white")

    def set_url(self, url):
        self.url = url

    def get_scores(self):
        print("------RANKING------")
        print(self.player)
        print(self.password)

        try:
            AUTH = requests.auth.HTTPBasicAuth(self.player, self.password)
            URL = str(self.url) + '/api/ranking/'
            print(URL)
            # response = requests.get(URL, auth=AUTH, params={'nickname': 'ela', 'scores': 'false'})
            response = requests.get(URL, auth=AUTH, params={'scores': 'true'}, timeout=1)

            if response.ok:
                self.statistics_others = {}
                self.statistics_others = json.loads(response.content.decode())
                print(json.dumps(self.statistics_others, indent=4))
                print()

        except requests.exceptions.RequestException or requests.exceptions.Timeout \
                or requests.exceptions.HTTPError or requests.exceptions.TooManyRedirects:
            text = "Can't connect to management server"
            self.error_connection_server_logging.emit(True, text)
            print(text)


    def get_left_bombs(self):
        AUTH = requests.auth.HTTPBasicAuth(self.player, self.password)

        URL = str(self.url) + '/api/ranking/'
        # response = requests.get(URL, auth=AUTH, params={'nickname': 'ela', 'scores': 'false'})
        response = requests.get(URL, auth=AUTH, params={'scores': 'false'}, timeout=1)
        try:
            if response.ok:
                statistics_others = json.loads(response.content.decode())
                print(json.dumps(statistics_others, indent=4))
                print()
                self.statistics_others = statistics_others
                self.reload_all()
            else:
                text = "Can't connect to logging server"
                self.error_connection_server_logging.emit(True, text)

        except requests.exceptions.RequestException or requests.exceptions.Timeout \
               or requests.exceptions.HTTPError or requests.exceptions.TooManyRedirects:
            text = "Can't connect to management server"
            self.error_connection_server_logging.emit(True, text)
            print(text)




    def set_login_password_ranking(self, player, password):
        self.player = player
        self.password = password

    def reload_all(self):
        row = 0
        print(self.statistics_others)
        for k, v in self.statistics_others.items():
            self.tableWidget.insertRow(row)
            self.tableWidget.setItem(row, 0, QTableWidgetItem(str(k)))
            for i in v:
                self.tableWidget.setItem(row, 1, QTableWidgetItem(str(i['players_count'])))
                self.tableWidget.setItem(row, 2, QTableWidgetItem(str(i['place'])))
            row += 1

    def check_repeated(self):
        list_keys = []
        for k, v in self.statistics_others.items():
            if list_keys is not []:
                if k in list_keys:
                    del self.statistics_others[k]
                else:
                    list_keys.append(k)
        print("po check_repeated ", self.statistics_others)

    @pyqtSlot()
    def on_button_search_clicked(self):
        self.tableWidget.setRowCount(0)

        # self.statistics_others = {}
        # self.statistics_others = {'toreno96': [{'id': 1, 'bombs': 11, 'players_count': 3, 'place': 3}], 'Ela': [{'place': 1, 'bomb_set': 2, 'players_count': 1}, {'id': 1, 'bombs': 3, 'players_count': 3, 'place': 3}, {'id': 0, 'bombs': 0, 'players_count': 3, 'place': 0}], 'Alice': [{'players_count': 3, 'place': 1}, {'players_count': 3, 'place': 1}, {'players_count': 3, 'place': 1}, {'players_count': 3, 'place': 1}], 'Bob': [{'players_count': 3, 'place': 2}, {'players_count': 3, 'place': 2}, {'players_count': 3, 'place': 2}, {'players_count': 3, 'place': 2}], 'Charlie': [{'players_count': 3, 'place': 3}, {'players_count': 3, 'place': 3}, {'players_count': 3, 'place': 3}, {'players_count': 3, 'place': 3}], 'ELaaa': []}

        self.check_repeated()
        nickname = self.lineEdit_nickname.text()
        print("self.statisctics_others ", self.statistics_others)
        if nickname != '':
            to_insert = {}
            for k, v in self.statistics_others.items():
                if k == nickname:
                    to_insert[k] = v

            row = 0
            print("to insert ", to_insert)
            if to_insert != {}:
                self.tableWidget.setRowCount(0)
                for k, v in to_insert.items():
                    print("k ", k)
                    print("v ", v)
                    self.tableWidget.insertRow(row)
                    self.tableWidget.setItem(row, 0, QTableWidgetItem(k))
                    for j in v:
                        if j is not []:
                            print("value ", j)
                            self.tableWidget.setItem(row, 1, QTableWidgetItem(str(j['players_count'])))
                            self.tableWidget.setItem(row, 2, QTableWidgetItem(str(j['place'])))
                    row += 1
        else:
            self.reload_all()

    @pyqtSlot()
    def on_button_back_clicked(self):
        self.back_from_ranking_signal.emit(True)
