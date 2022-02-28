import sys

from PyQt5 import uic
from PyQt5.QtWidgets import QApplication, QWidget, QTableWidgetItem
from PyQt5 import QtWidgets
import sqlite3


class Coffee(QWidget):
    def __init__(self):
        super().__init__()
        uic.loadUi('main.ui', self)
        self.table.setColumnCount(7)
        self.table.setRowCount(13)
        self.table.setHorizontalHeaderLabels(
            ['ID', 'название сорта', 'степень обжарки', 'состояние', 'вкус', 'цена', 'объем'])
        self.loaddata()

    def loaddata(self):
        con = sqlite3.connect('coffee.db')
        cur = con.cursor()
        sqlquest = "SELECT * FROM coffee1"
        tablerow = 0
        for row in cur.execute(sqlquest):
            for i in range(len(row)):
                self.table.setItem(tablerow, i, QtWidgets.QTableWidgetItem(str(row[i])))
            tablerow += 1
        self.table.resizeColumnsToContents()
        self.table.resizeRowsToContents()
        self.table.repaint()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = Coffee()
    ex.show()
    sys.exit(app.exec())
