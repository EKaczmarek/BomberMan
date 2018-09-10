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

    def __init__(self, parent = None):
        QDialog.__init__(self, parent)
        self.setupUi(self)

        self.setWindowTitle('Bomberman')
        self.setStyleSheet("background: white")

        # będzie to poniżej
        """AUTH = requests.auth.HTTPBasicAuth('ela', '12341234')

        URL = 'http://192.168.43.102:8080/api/ranking/'
        # response = requests.get(URL, auth=AUTH, params={'nickname': 'ela', 'scores': 'false'})
        response = requests.get(URL, auth=AUTH)

        if response.ok:
            statistics = json.loads(response.content.decode())
            print(json.dumps(statistics, indent=4))
            print()"""

        self.statistics = {
            'Alice': {
                'players_count': 3,
                'place': 1,
            },
            'Bob': {
                'players_count': 3,
                'place': 2,
            },
            'Charlie': {
                'players_count': 3,
                'place': 3,
            },
            'A': {
                'players_count': 3,
                'place': 3,
            },
            'B': {
                'players_count': 3,
                'place': 3,
            },
            'C': {
                'players_count': 3,
                'place': 3,
            },
            'D': {
                'players_count': 3,
                'place': 3,
            },
            'F': {
                'players_count': 3,
                'place': 3,
            },
            'g': {
                'players_count': 3,
                'place': 3,
            },
        }
        self.reload_all()

    def reload_all(self):
        row = 0
        for k, v in self.statistics.items():
            self.tableWidget.insertRow(row)
            self.tableWidget.setItem(row, 0, QTableWidgetItem(str(k)))
            self.tableWidget.setItem(row, 1, QTableWidgetItem(str(v['players_count'])))
            self.tableWidget.setItem(row, 2, QTableWidgetItem(str(v['place'])))
            row += 1

    @pyqtSlot()
    def on_button_search_clicked(self):
        nickname = self.lineEdit_nickname.text()
        # print(nickname)
        if nickname != '':
            to_insert = {}
            for k, v in self.statistics.items():
                if k == nickname:
                    to_insert[k] = v

            row = 0
            if to_insert != {}:
                self.tableWidget.setRowCount(0)
                for k, v in to_insert.items():
                    self.tableWidget.insertRow(row)
                    self.tableWidget.setItem(row, 0, QTableWidgetItem(k))
                    self.tableWidget.setItem(row, 1, QTableWidgetItem(str(v['players_count'])))
                    self.tableWidget.setItem(row, 2, QTableWidgetItem(str(v['place'])))
                    row += 1
        else:
            self.reload_all()

    @pyqtSlot()
    def on_button_back_clicked(self):
        self.back_from_ranking_signal.emit(True)
