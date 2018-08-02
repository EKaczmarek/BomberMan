from PyQt5.QtWidgets import QDialog, QTableWidgetItem
from PyQt5.QtCore import pyqtSlot
from PyQt5.QtCore import Qt
from PyQt5 import uic
from pymongo import  MongoClient
from functools import reduce

qtCreatorFile = "Classes/GUI/ranking.ui"
Ui_Dialog, QtBaseClass = uic.loadUiType(qtCreatorFile)

class Ranking(QDialog, Ui_Dialog):

    def __init__(self, parent = None):
        QDialog.__init__(self, parent)
        self.setupUi(self)

        self.setWindowTitle('Bomberman')
        self.setStyleSheet("background: white")

        #self.getFromMongo()

        self.button_search.clicked.connect(self.on_button_search_clicked)
        self.button_back.clicked.connect(self.on_button_back_clicked)

    def getFromMongo(self):
        client = MongoClient('localhost', 27017)
        db = client['BomberMan']
        collection = db['Players']

        test = [list(db[collection].find({}, {"nickname": 1, "points": 1, "playedGames": 1, "_id": 0})) for collection
                in
                db.collection_names()]

        self.test = reduce(lambda x, y: x + y, test)
        row = 0
        for i in self.test:
            self.tableWidget.insertRow(row)
            self.tableWidget.setItem(row, 0, QTableWidgetItem(i['nickname']))
            self.tableWidget.setItem(row, 1, QTableWidgetItem(str(i['points'])))
            self.tableWidget.setItem(row, 2, QTableWidgetItem(str(i['playedGames'])))
            row += 1

    @pyqtSlot()
    def on_button_search_clicked(self):
        nickname = self.lineEdit_nickname.text()
        print(nickname)
        lista = list(filter(lambda x: x['nickname'] == nickname, self.test))

        for i in reversed(range(self.tableWidget.rowCount())):
            self.tableWidget.removeRow(i)

        if(nickname == ''):
            self.getFromMongo()
        else:
            row = 0
            for i in lista:
                print(i)
                self.tableWidget.insertRow(row)
                self.tableWidget.setItem(row, 0, QTableWidgetItem(i['nickname']))
                self.tableWidget.setItem(row, 1, QTableWidgetItem(str(i['points'])))
                self.tableWidget.setItem(row, 2, QTableWidgetItem(str(i['playedGames'])))
                row += 1




    @pyqtSlot()
    def on_button_back_clicked(self):
        self.close()
